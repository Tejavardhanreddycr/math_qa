import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Set up the Streamlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

try:
    llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
except Exception as e:
    st.error(f"Failed to initialize LLM: {str(e)}")
    st.stop()

# Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned"
)

# Initialize the Math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expressions need to be provided"
)

prompt = """
You're an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below.
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

# Combine all tools into chain
chain = prompt_template | llm 

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.invoke,
    description="A tool for answering logic-based and reasoning questions."
)

# Initialize the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User interaction
question = st.text_area("Enter your question:")

if st.button("Find my answer"):
    if not question:
        st.warning("Please enter a question")
        st.stop()
    
    if len(question.strip()) < 5:
        st.warning("Please enter a more detailed question")
        st.stop()

    try:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container())
            response = assistant_agent.run(question, callbacks=[st_cb])
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write("### Response:")
            st.success(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
