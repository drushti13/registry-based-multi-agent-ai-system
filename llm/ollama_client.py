from ollama import chat
import logging
from config import OLLAMA_MODEL

logger = logging.getLogger("ollama")
logger.setLevel(logging.INFO)

def run_llm(system_prompt: str, user_input: str) -> str:
    logger.info(f"[LLM] Calling model={OLLAMA_MODEL}")

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_input.strip()},
        ],
    )

    logger.info(f"[LLM] Model={OLLAMA_MODEL} completed")

    return response["message"]["content"].strip()