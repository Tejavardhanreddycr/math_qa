from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent

# Flask app initialization
app = Flask(__name__)

@app.route("/solve_question", methods=["POST"])
def solve_question():
    """Solve a math or logic question provided by the user."""
    data = request.get_json()
    question = data.get("question")
    groq_api_key = request.args.get("groq_api_key")

    if not groq_api_key:
        return jsonify({"error": "Groq API Key is required."}), 400

    if not question:
        return jsonify({"error": "Question is required."}), 400

    # Initialize LLM
    llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
    # Initializing tools
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
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the Text to Math Problem Solver API."})

if __name__ == "__main__":
    app.run(debug=True)

# Command to test with curl
# curl -X POST "http://127.0.0.1:5000/solve_question?groq_api_key=<your_api_key>" -H "Content-Type: application/json" -d '{
#   "question": "What is the sum of 123 and 456?"
# }'

