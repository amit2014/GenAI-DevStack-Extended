# GenAI / LLM / RAG / ML Dev Stack (Windows 10 via WSL2)

This repo is a batteries-included template for building GenAI + RAG + ML apps in Python.
It includes:
- **FastAPI** service for inference & RAG endpoints
- **LangChain + FAISS** for local vector search (with optional **Qdrant** via Docker)
- **PostgreSQL + pgvector** (optional) and **Redis**
- **MLflow** for experiment tracking (optional)
- **Prefect** for lightweight orchestration
- **Docker** & **docker-compose** for local stack
- **GitHub Actions** CI (lint, tests, build/push Docker image)
- **Pre-commit** hooks (ruff, black, isort), **mypy** type checking
- **Jupyter** dev container

> Recommended: run in **WSL2 (Ubuntu 22.04)** with **Docker Desktop** using the WSL2 backend.

---

## Quick Start (WSL2)

```bash
# 0) In Windows PowerShell (admin), enable WSL & install Ubuntu (one-time):
#    wsl --install -d Ubuntu-22.04
#    Reboot if prompted, then open Ubuntu terminal.

# 1) Update & basics (inside Ubuntu):
sudo apt update && sudo apt -y upgrade
sudo apt -y install build-essential git curl unzip pkg-config python3.10-venv python3-pip

# 2) (Optional but recommended) Install uv for fast Python envs:
curl -LsSf https://astral.sh/uv/install.sh | sh
# then re-open shell or source ~/.profile

# 3) Clone this repo into WSL home and enter:
git clone <your-fork-or-download> genai-devstack
cd genai-devstack

# 4) Create env and install deps (choose ONE):
# Using uv (recommended):
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# OR classic venv + pip:
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt

# 5) Pre-commit hooks (format/lint on commit):
pre-commit install

# 6) Launch services with Docker:
docker compose up -d
# This brings up: qdrant, redis, postgres (with pgvector), mlflow, and jupyter

# 7) Run the API locally:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 8) Try the docs:
# http://localhost:8000/docs
```

### GPU (NVIDIA) in WSL2
- Install latest **NVIDIA Windows driver**.
- Install **Docker Desktop** with WSL2 backend and **enable GPU** in settings.
- Inside WSL, verify: `nvidia-smi`.
- Choose appropriate **PyTorch** CUDA wheels if using GPU.

---

## RAG Demo

The API exposes `/ingest` to index sample docs into FAISS (local) and `/rag` to answer questions.
You can also switch to **Qdrant** by setting `RAG_BACKEND=qdrant` env var.

```bash
# Ingest small sample files to FAISS store
python -m app.rag.ingest --source data/sample_docs --store .cache/faiss

# Ask a question via API
curl -X POST http://localhost:8000/rag -H "Content-Type: application/json"   -d '{"query": "What is RAG?", "k": 3}'
```

---

## Project Structure

```
app/
  __init__.py
  main.py            # FastAPI app
  config.py          # Settings via pydantic
  deps.py            # Shared dependencies
  models/            # Pydantic DTOs
  rag/
    pipeline.py      # RAG pipeline (LangChain + FAISS/Qdrant)
    ingest.py        # CLI to build index
    store.py         # Vector store abstraction
  ml/
    train.py         # Example training script
    predict.py       # Batch/inference example
  workers/
    tasks.py         # Prefect/Celery-style tasks (example uses Prefect)
data/
  sample_docs/       # Small demo docs
tests/
  test_api.py
docker/
  Dockerfile.api
  Dockerfile.jobs
.github/workflows/ci.yml
docker-compose.yml
Makefile
requirements.txt
.pre-commit-config.yaml
pyproject.toml       # Tooling config (ruff/black/isort/mypy)
.env.example
.devcontainer/devcontainer.json
```

---

## CI/CD

- GitHub Actions runs lint, tests, and builds Docker image.
- To push to GHCR, set repository secrets: `CR_PAT` (classic token with `write:packages`).

---

## Common Commands

```bash
make fmt    # format (ruff/black/isort)
make lint   # lint + types
make test   # run pytest
make up     # docker compose up -d
make down   # docker compose down -v
make api    # run uvicorn dev server
```

---

## Notes

- For Windows-only (no WSL), install Python 3.10+, Git, Docker Desktop, and run `pip install -r requirements.txt` in a PowerShell terminal. Some libraries (faiss, bitsandbytes) work best in WSL/Linux.


# This extended environment supports:

- **RAG & LLM frameworks**: Haystack, LlamaIndex, LangChain
- **Providers**: OpenAI, Anthropic, Meta (HuggingFace Transformers), Mistral
- **Vector DBs**: Pinecone, FAISS, Weaviate, Qdrant
- **Embeddings**: OpenAI, HuggingFace Transformers, SentenceTransformers
- **MLOps**: MLflow, Docker, Kubernetes client

## Usage Examples

### OpenAI & Anthropic

```python
from openai import OpenAI
import anthropic

client = OpenAI(api_key="sk-...")
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello from GenAI dev stack"}]
)
print(resp.choices[0].message.content)

a_client = anthropic.Anthropic(api_key="sk-ant-...")
msg = a_client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=200,
    messages=[{"role": "user", "content": "Hello from Anthropic"}]
)
print(msg.content[0].text)
```

### Pinecone & Weaviate

```python
import pinecone, weaviate

pinecone.init(api_key="pc-...")
pc_index = pinecone.Index("genai")

client = weaviate.Client("http://localhost:8080")
print(client.is_ready())
```

### K8s Client

```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
print([ns.metadata.name for ns in v1.list_namespace().items])
```
