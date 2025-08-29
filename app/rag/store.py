import os
from typing import List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Qdrant as QdrantVS
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class FaissStore:
    def __init__(self, model_name: str, faiss_dir: str):
        self.embedder = SentenceTransformer(model_name)
        self.faiss_dir = faiss_dir
        os.makedirs(self.faiss_dir, exist_ok=True)
        self.vs = None

    def load(self):
        if os.path.exists(os.path.join(self.faiss_dir, "index.faiss")):
            self.vs = FAISS.load_local(self.faiss_dir, self.embedder, allow_dangerous_deserialization=True)
        else:
            self.vs = FAISS.from_texts(["RAG template initialized."], self.embedder)
            self.vs.save_local(self.faiss_dir)

    def add_texts(self, texts: List[str], metadatas=None):
        self.vs.add_texts(texts=texts, metadatas=metadatas or [{}])
        self.vs.save_local(self.faiss_dir)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        docs = self.vs.similarity_search_with_score(query, k=k)
        return [(d.page_content, float(s)) for d, s in docs]


class QdrantStore:
    def __init__(self, model_name: str, url: str, collection: str = "docs"):
        self.embedder = SentenceTransformer(model_name)
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.vs = QdrantVS(client=self.client, collection_name=self.collection, embeddings=self.embedder)

    def load(self):
        # Qdrant is schema-less via LangChain; ensure client is reachable by a simple call
        self.client.get_collections()

    def add_texts(self, texts: List[str], metadatas=None):
        self.vs.add_texts(texts=texts, metadatas=metadatas or [{}])

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        docs = self.vs.similarity_search_with_score(query, k=k)
        return [(d.page_content, float(s)) for d, s in docs]
