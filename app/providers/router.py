import os
from .openai_client import call_openai
from .anthropic_client import call_anthropic
from .hf_infer import call_hf

def call_llm(prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if provider == "openai":
        return call_openai(prompt, model)
    elif provider == "anthropic":
        return call_anthropic(prompt, model)
    elif provider == "hf":
        return call_hf(model, prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")
