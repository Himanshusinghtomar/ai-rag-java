# query/generate.py
import requests
from query.search import retrieve_context
from query.prompt_loader import load_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"

def ask(question: str):
    system_prompt = load_prompt(
        "system.txt",
        "java.txt",
        "response.txt",
        "orchestration.txt"  # optional
    )

    context = retrieve_context(question)

    prompt = f"""
{system_prompt}

### PROJECT CONTEXT
{context}

### QUESTION
{question}

### ANSWER
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"]
