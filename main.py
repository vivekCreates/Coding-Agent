import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools import tools
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")


model = ChatGroq(
    model=model_name,
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=tools,
)


