import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_classic.chains.summarize import load_summarize_chain

import sys

# Ensure backend directory is in sys.path for direct script execution and package imports
_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

load_dotenv(_backend_dir / ".env")
load_dotenv()

from utils.preprocess import preprocess_text
from prompts.text_prompts import TEXT_MAP_PROMPT_TEMPLATE, get_text_combine_prompt
from services.llm_service import get_llm


def summarize_text(text: str, title: str = "Raw Text", summary_type: str = "detailed", token_limit: int = 4000):
    """
    Preprocess and summarize raw text using Map-Reduce summarization chain.

    Args:
        text: Input raw text string to summarize.
        title: Optional title label for the text.
        summary_type: Target summary format (quick, detailed, study_notes, executive).
        token_limit: Maximum tokens per chunk during preprocessing.

    Returns:
        Dictionary with metadata, summary, and original text.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    metadata = {
        "title": title,
        "character_count": len(text),
        "word_count": len(text.split()),
        "summary_type": summary_type,
    }

    # --------------------------------------------------
    # 1. Preprocess text to reduce token count
    # --------------------------------------------------
    result = preprocess_text(
        text,
        token_limit=token_limit
    )

    if not result:
        raise ValueError("Text contains no meaningful content after preprocessing.")

    # --------------------------------------------------
    # 2. Convert chunks into LangChain Documents
    # --------------------------------------------------
    if isinstance(result, str):
        documents = [
            Document(
                page_content=result,
                metadata=metadata
            )
        ]
    else:
        documents = [
            Document(
                page_content=chunk,
                metadata=metadata
            )
            for chunk in result
        ]

    # --------------------------------------------------
    # 3. Initialize Groq LLM
    # --------------------------------------------------
    llm = get_llm()

    # --------------------------------------------------
    # 4. Create Map-Reduce summarization chain
    # --------------------------------------------------
    combine_prompt = get_text_combine_prompt(summary_type)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=TEXT_MAP_PROMPT_TEMPLATE,
        combine_prompt=combine_prompt
    )

    # --------------------------------------------------
    # 5. Generate summary
    # --------------------------------------------------
    output = summary_chain.invoke({
        "input_documents": documents
    })

    summary = output["output_text"]

    # --------------------------------------------------
    # 6. Return everything
    # --------------------------------------------------
    return {
        "metadata": metadata,
        "summary": summary,
        "text": text
    }


# --------------------------------------------------
# Example
# --------------------------------------------------
if __name__ == "__main__":
    sample_text = """
    Artificial Intelligence has made dramatic leaps in recent years, transforming industries from healthcare
    to financial services. In particular, large language models (LLMs) allow systems to analyze, understand,
    and generate human-like text across multiple languages and complex reasoning tasks. Techniques like
    Retrieval-Augmented Generation (RAG) and Map-Reduce summarization enable models to process lengthy documents,
    videos, and web articles while significantly reducing context noise and hallucination risks.
    """

    result = summarize_text(sample_text, title="AI Overview")

    print("\nTITLE:", result["metadata"]["title"])
    print("\nWORD COUNT:", result["metadata"]["word_count"])
    print("\nSUMMARY:\n", result["summary"])
