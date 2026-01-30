# query/generate.py
import requests
from query.search import retrieve_context
from query.prompt_loader import load_prompt

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"  # Changed to match your model

def ask(question: str):
    system_prompt = load_prompt(
        "system.txt",
        "java.txt",
        "response.txt",
        "orchestration.txt"  # optional
    )

    context = retrieve_context(question)

    user_prompt = f"""
### PROJECT CONTEXT
{context}

### QUESTION
{question}

### ANSWER
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "stream": False  # This is important!
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["message"]["content"]