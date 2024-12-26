from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from functools import wraps
import time

# Flask app initialization
app = Flask(__name__)

# Simple in-memory rate limiting
rate_limit_data = {}
RATE_LIMIT = 10  # requests
RATE_LIMIT_WINDOW = 60  # seconds

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean up old entries
        rate_limit_data.clear()
        
        # Initialize or update client's request data
        if client_ip not in rate_limit_data:
            rate_limit_data[client_ip] = {"count": 0, "window_start": current_time}
        
        # Reset if window has expired
        if current_time - rate_limit_data[client_ip]["window_start"] >= RATE_LIMIT_WINDOW:
            rate_limit_data[client_ip] = {"count": 0, "window_start": current_time}
        
        # Check rate limit
        if rate_limit_data[client_ip]["count"] >= RATE_LIMIT:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        
        # Increment request count
        rate_limit_data[client_ip]["count"] += 1
        
        return func(*args, **kwargs)
    return wrapper

def validate_question(question):
    """Validate the input question."""
    if not isinstance(question, str):
        return False, "Question must be a string"
    if len(question.strip()) < 5:
        return False, "Question is too short"
    if len(question) > 1000:
        return False, "Question is too long (max 1000 characters)"
    return True, None

@app.route("/solve_question", methods=["POST"])
@rate_limit
def solve_question():
    """Solve a math or logic question provided by the user."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        question = data.get("question")
        groq_api_key = request.args.get("groq_api_key")

        if not groq_api_key:
            return jsonify({"error": "Groq API Key is required"}), 400

        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Validate question
        is_valid, error_message = validate_question(question)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Initialize LLM
        try:
            llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
        except Exception as e:
            return jsonify({"error": f"Failed to initialize LLM: {str(e)}"}), 500

        # Initialize tools
        wikipedia_wrapper = WikipediaAPIWrapper()
        wikipedia_tool = Tool(
            name="Wikipedia",
            func=wikipedia_wrapper.run,
            description="A tool for searching the Internet to find various information on the topics mentioned"
        )

        math_chain = LLMMathChain.from_llm(llm=llm)
        calculator = Tool(
            name="Calculator",
            func=math_chain.run,
            description="A tool for answering math-related questions. Only input mathematical expressions need to be provided."
        )

        prompt = """
        You're an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation, displaying it pointwise for the question below.
        Question: {question}
        Answer:
        """

        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=prompt
        )

        # Combine all tools into a chain
        chain = prompt_template | llm

        reasoning_tool = Tool(
            name="Reasoning tool",
            func=chain.invoke,
            description="A tool for answering logic-based and reasoning questions."
        )

        # Initialize agent
        assistant_agent = initialize_agent(
            tools=[wikipedia_tool, calculator, reasoning_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            handle_parsing_errors=True
        )

        try:
            # Get response from the agent
            response = assistant_agent.run(question)
            return jsonify({"answer": response})
        except Exception as e:
            return jsonify({"error": f"Error processing question: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "Welcome to the Text to Math Problem Solver API"
    })

if __name__ == "__main__":
    # In production, debug should be False
    app.run(host="0.0.0.0", port=5000, debug=False)
