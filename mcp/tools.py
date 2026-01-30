# mcp/tools.py
from query.generate import ask

def ask_codebase(question: str):
    answer = ask(question)
    return {
        "answer": answer
    }
