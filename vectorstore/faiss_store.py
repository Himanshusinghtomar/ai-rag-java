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

    @classmethod
    def load(cls, index_path: str):
        """Load an existing index from disk"""
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index not found at {index_path}")
        
        meta_path = index_path + ".meta.json"
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata not found at {meta_path}")
        
        # Read index to get dimension
        index = faiss.read_index(index_path)
        dim = index.d
        
        # Create instance and load data
        store = cls.__new__(cls)
        store.dim = dim
        store.index_path = index_path
        store.meta_path = meta_path
        store.index = index
        
        with open(meta_path) as f:
            store.metadata = json.load(f)
        
        return store

    def add(self, text: str, meta: dict):
        vector = embed_text(text)
        self.index.add(vector.reshape(1, -1))
        self.metadata.append(meta)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        """Search using a pre-computed query vector"""
        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)
        
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                meta = self.metadata[idx]
                results.append({
                    "text": meta.get("content", ""),
                    "metadata": meta
                })
        return results