import os
from pathlib import Path
from dotenv import load_dotenv
import tiktoken
from langchain_groq import ChatGroq

# Look for .env in backend directory and root directory
_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env")
load_dotenv()

try:
    _enc = tiktoken.get_encoding("cl100k_base")
except Exception:
    _enc = None


class EfficientChatGroq(ChatGroq):
    """
    Subclass of ChatGroq that uses tiktoken for fast, lightweight token counting
    preventing missing transformers dependency errors during Map-Reduce collapse.
    """
    def get_num_tokens(self, text: str) -> int:
        if _enc:
            return len(_enc.encode(text, disallowed_special=()))
        return int(len(text) / 3.5) + 1


def get_llm(model: str = "openai/gpt-oss-120b", temperature: float = 0.2):
    """
    Initialize and return a ChatGroq LLM instance.

    Args:
        model: Model identifier on Groq.
        temperature: Temperature setting for generation.

    Returns:
        EfficientChatGroq instance.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    return EfficientChatGroq(
        model=model,
        temperature=temperature,
        api_key=api_key
    )
