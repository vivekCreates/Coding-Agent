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


@tool
def write_file(data: str) -> str:
    """
    Create or overwrite a file.
    Input must be: path|||content
    """
    try:
        path, content = data.split("|||")
        with open(path.strip(), "w") as f:
            f.write(content.strip())
        return f"File {path} written successfully."
    except Exception as e:
        return str(e)

