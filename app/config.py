from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "dev"
    log_level: str = "INFO"

    # RAG
    rag_backend: str = "faiss"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    faiss_dir: str = ".cache/faiss"
    qdrant_url: str = "http://localhost:6333"

    # Databases
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    redis_url: str = "redis://localhost:6379/0"

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
