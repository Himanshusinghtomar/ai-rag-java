import json
from vectorstore.faiss_store import FaissVectorStore

INDEX_PATH = "vectorstore/codebase.index"
CHUNKS_PATH = "index/code_chunks.json"

def build():
    with open(CHUNKS_PATH) as f:
        chunks = json.load(f)

    # Temporary embed to get vector dimension
    from vectorstore.embedder import embed_text
    dim = len(embed_text("test"))

    store = FaissVectorStore(dim, INDEX_PATH)

    for chunk in chunks:
        store.add(chunk["content"], chunk)

    store.save()
    print(f"Indexed {len(chunks)} chunks")

if __name__ == "__main__":
    build()
