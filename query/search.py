# query/search.py
from vectorstore.faiss_store import FaissVectorStore
from vectorstore.embedder import embed_text

INDEX_PATH = "vectorstore/codebase.index"

def retrieve_context(question: str, top_k: int = 5):
    store = FaissVectorStore.load(INDEX_PATH)
    q_vector = embed_text(question)

    results = store.search(q_vector, top_k=top_k)

    context_blocks = []
    for r in results:
        meta = r["metadata"]
        context_blocks.append(
            f"FILE: {meta.get('file')}\n"
            f"TYPE: {meta.get('type')}\n"
            f"CONTENT:\n{r['text']}"
        )

    return "\n\n---\n\n".join(context_blocks)
