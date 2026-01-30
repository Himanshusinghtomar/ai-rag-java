import faiss
import json
import numpy as np
import os

from vectorstore.embedder import embed_text

class FaissVectorStore:
    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = index_path + ".meta.json"

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(self.meta_path) as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.metadata = []

    def add(self, text: str, meta: dict):
        vector = embed_text(text)
        self.index.add(vector.reshape(1, -1))
        self.metadata.append(meta)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def search(self, query: str, top_k: int = 3):
        q_vector = embed_text(query).reshape(1, -1)
        distances, indices = self.index.search(q_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
