from langchain.tools import tool
import os

@tool
def read_file(path: str) -> str:
    """Read a file and return its content."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

