from fastapi import FastAPI
from app.providers.router import call_llm
from .models.rag import RagQuery
from .rag import pipeline

app = FastAPI(title="GenAI/RAG API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rag")
def rag(q: RagQuery):
    hits = pipeline.answer(q.query, k=q.k)
    return {"query": q.query, "results": [{"text": t, "score": s} for t, s in hits]}
