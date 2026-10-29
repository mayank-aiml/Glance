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

from extractors.webpage_extractor import fetch_website
from utils.preprocess import preprocess_text
from prompts.website_prompts import WEB_MAP_PROMPT_TEMPLATE, get_website_combine_prompt
from services.llm_service import get_llm


def summarize_website(url: str, summary_type: str = "detailed", token_limit: int = 4500):
    """
    Fetch, preprocess, and summarize website content using Map-Reduce chain.

    Args:
        url: Webpage URL to scrape and summarize.
        summary_type: Target summary format (quick, detailed, study_notes, executive).
        token_limit: Maximum tokens per chunk during preprocessing.

    Returns:
        Dictionary with metadata, summary text, and cleaned webpage content.
    """
    # --------------------------------------------------
    # 1. Fetch website content
    # --------------------------------------------------
    website_data = fetch_website(url)

    title = website_data.get("title", "")
    clean_text = website_data.get("content", "")

    if not clean_text or not clean_text.strip():
        raise ValueError(f"Could not extract any readable content from: {url}")

    metadata = {
        "url": url,
        "title": title,
        "summary_type": summary_type,
    }

    # --------------------------------------------------
    # 2. Preprocess text to reduce token count
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
    combine_prompt = get_website_combine_prompt(summary_type)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=WEB_MAP_PROMPT_TEMPLATE,
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
        "content": clean_text
    }


# --------------------------------------------------
# Example
# --------------------------------------------------
if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Earth"

    result = summarize_website(test_url)

    print("\nTITLE:")
    print(result["metadata"]["title"])

    print("\nSUMMARY:")
    print(result["summary"])
