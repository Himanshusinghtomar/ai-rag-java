import requests
import numpy as np

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"

def embed_text(text: str) -> np.ndarray:
    payload = {
        "model": MODEL_NAME,
        "input": text
    }

    response = requests.post(OLLAMA_URL, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Include response body for easier debugging
        raise RuntimeError(f"Embeddings request failed: {response.status_code} {response.text}") from e

    embedding = response.json()["embedding"]
    return np.array(embedding, dtype=np.float32)
