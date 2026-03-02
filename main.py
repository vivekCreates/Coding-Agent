import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")



def main():
    print("Hello from coding-agent!")


if __name__ == "__main__":
    main()
