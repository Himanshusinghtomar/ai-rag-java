# query/search.py
from vectorstore.faiss_store import FaissVectorStore
from vectorstore.embedder import embed_text
import json

INDEX_PATH = "vectorstore/codebase.index"
CHUNKS_PATH = "index/code_chunks.json"

def retrieve_context(question: str, top_k: int = 15):
    # Load all chunks for keyword search
    with open(CHUNKS_PATH) as f:
        all_chunks = json.load(f)
    
    # Extract keywords from question
    keywords = [w.lower() for w in question.split() if len(w) > 3]
    
    # Keyword search: find chunks that contain question keywords
    keyword_matches = []
    for chunk in all_chunks:
        content = chunk.get('content', '').lower()
        file_path = chunk.get('file', '').lower()
        
        # Count keyword matches
        match_score = sum(1 for kw in keywords if kw in content or kw in file_path)
        
        if match_score > 0:
            keyword_matches.append({
                'chunk': chunk,
                'score': match_score
            })
    
    # Sort by keyword match score
    keyword_matches.sort(key=lambda x: x['score'], reverse=True)
    
    # If we have good keyword matches, use those
    if keyword_matches and keyword_matches[0]['score'] >= 2:
        # Take top keyword matches
        results = [m['chunk'] for m in keyword_matches[:top_k]]
    else:
        # Fall back to vector search
        store = FaissVectorStore.load(INDEX_PATH)
        q_vector = embed_text(question)
        results = store.search(q_vector, top_k=top_k)
        results = [r['metadata'] for r in results]
    
    # Format context
    context_blocks = []
    for meta in results:
        context_blocks.append(
            f"FILE: {meta.get('file', 'unknown')}\n"
            f"TYPE: {meta.get('type', 'unknown')}\n"
            f"NAME: {meta.get('name', 'N/A')}\n"
            f"CONTENT:\n{meta.get('content', '')}"
        )

    return "\n\n---\n\n".join(context_blocks)