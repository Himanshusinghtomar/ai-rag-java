# query/prompt_loader.py
from pathlib import Path

PROMPT_DIR = Path("prompt")

def load_prompt(*files):
    parts = []
    for f in files:
        path = PROMPT_DIR / f
        if path.exists():
            parts.append(path.read_text())
    return "\n\n".join(parts)
