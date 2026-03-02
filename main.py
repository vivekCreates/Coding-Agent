import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from tools import tools
from system_prompt import system_prompt
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
    system_prompt=system_prompt
)


query = input("Enter the prompt: ")

response = agent.invoke({"messages":[HumanMessage(content=query)]})

print(response)



