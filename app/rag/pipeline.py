from typing import List, Tuple
from .store import FaissStore, QdrantStore
from ..config import settings

def get_store():
    if settings.rag_backend.lower() == "qdrant":
        store = QdrantStore(settings.embedding_model, settings.qdrant_url)
    else:
        store = FaissStore(settings.embedding_model, settings.faiss_dir)
    store.load()
    return store

def answer(query: str, k: int = 3) -> List[Tuple[str, float]]:
    store = get_store()
    return store.search(query, k=k)
