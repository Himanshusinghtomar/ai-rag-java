# mcp/server.py
from fastapi import FastAPI
from mcp.tools import ask_codebase
from mcp.schemas import ASK_CODEBASE_SCHEMA

app = FastAPI()

@app.get("/mcp/tools")
def list_tools():
    return {
        "tools": [ASK_CODEBASE_SCHEMA]
    }

@app.post("/mcp/ask_codebase")
def handle_ask(payload: dict):
    question = payload.get("question")
    if not question:
        return {"error": "question is required"}

    return ask_codebase(question)
