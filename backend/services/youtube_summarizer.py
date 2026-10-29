import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_classic.chains.summarize import load_summarize_chain

# Ensure backend directory is in sys.path for direct script execution and package imports
_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

load_dotenv(_backend_dir / ".env")
load_dotenv()

from extractors.youtube_extractor import extract_youtube
from utils.preprocess import preprocess_text
from prompts.youtube_prompts import YT_MAP_PROMPT, get_youtube_combine_prompt
from services.llm_service import get_llm

logger = logging.getLogger(__name__)


def summarize_youtube(youtube_url, summary_type="detailed", token_limit=4500):
    """
    Summarize a YouTube video transcript without triggering bot-detection / cookie errors on cloud hosting.

    Args:
        youtube_url: Full YouTube video or Shorts URL.
        summary_type: Target summary format (quick, detailed, study_notes, executive).
        token_limit: Maximum tokens per chunk during preprocessing.

    Returns:
        Dictionary with metadata, summary, and clean transcript.
    """
    # --------------------------------------------------
    # 1. Extract metadata and transcript (via oEmbed & transcript-api)
    # --------------------------------------------------
    extracted = extract_youtube(youtube_url)
    metadata = extracted["metadata"]
    metadata["summary_type"] = summary_type
    clean_text = extracted["transcript"]

    # --------------------------------------------------
    # 2. Preprocess transcript to reduce token count
    # --------------------------------------------------
    result = preprocess_text(
        clean_text,
        token_limit=token_limit
    )

    # --------------------------------------------------
    # 3. Convert chunks into LangChain Documents
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
    # 4. Initialize Groq LLM
    # --------------------------------------------------
    llm = get_llm()

    # --------------------------------------------------
    # 5. Create Map-Reduce summarization chain
    # --------------------------------------------------
    combine_prompt = get_youtube_combine_prompt(summary_type)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=YT_MAP_PROMPT,
        combine_prompt=combine_prompt
    )

    # --------------------------------------------------
    # 6. Generate summary
    # --------------------------------------------------
    output = summary_chain.invoke({
        "input_documents": documents
    })

    summary = output["output_text"]

    # --------------------------------------------------
    # 7. Return everything
    # --------------------------------------------------
    return {
        "metadata": metadata,
        "summary": summary,
        "transcript": clean_text
    }


# --------------------------------------------------
# Example
# --------------------------------------------------
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=fuhE6PYnRMc"
    result = summarize_youtube(test_url, summary_type="quick")
    print("\nTITLE:", result["metadata"]["title"])
    print("\nCHANNEL:", result["metadata"]["channel"])
    print("\nSUMMARY:\n", result["summary"])
