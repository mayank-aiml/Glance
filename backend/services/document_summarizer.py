import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
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
from prompts.document_prompts import map_prompt_template, get_document_combine_prompt
from services.llm_service import get_llm


def summarize_pdf(file_path: str, summary_type: str = "detailed", token_limit: int = 4000):
    """
    Summarize a PDF document using preprocessing and Map-Reduce summarization chain.

    Args:
        file_path: Path to the PDF file.
        summary_type: Summary format type (quick, detailed, study_notes, executive).
        token_limit: Maximum tokens per chunk during preprocessing.

    Returns:
        Dictionary with metadata, summary, and extracted document text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    # --------------------------------------------------
    # 1. Load document content and metadata
    # --------------------------------------------------
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()

    if not documents:
        raise ValueError("The PDF contains no readable content.")

    raw_text = "\n\n".join(doc.page_content for doc in documents if doc.page_content).strip()

    if not raw_text:
        raise ValueError("The PDF contains no readable text content.")

    metadata = {
        "title": os.path.basename(file_path),
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "page_count": len(documents),
        "summary_type": summary_type,
    }

    # --------------------------------------------------
    # 2. Preprocess text to reduce token count
    # --------------------------------------------------
    result = preprocess_text(
        raw_text,
        token_limit=token_limit
    )

    # --------------------------------------------------
    # 3. Convert chunks into LangChain Documents
    # --------------------------------------------------
    if isinstance(result, str):
        docs = [
            Document(
                page_content=result,
                metadata=metadata
            )
        ]
    else:
        docs = [
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
    combine_prompt = get_document_combine_prompt(summary_type)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=map_prompt_template,
        combine_prompt=combine_prompt
    )

    # --------------------------------------------------
    # 6. Generate summary
    # --------------------------------------------------
    output = summary_chain.invoke({
        "input_documents": docs
    })

    summary = output["output_text"]

    # --------------------------------------------------
    # 7. Return everything
    # --------------------------------------------------
    return {
        "metadata": metadata,
        "summary": summary,
        "text": raw_text
    }


summarize_document = summarize_pdf


# --------------------------------------------------
# Example
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        result = summarize_pdf(test_file)
        print("\nTITLE:", result["metadata"]["title"])
        print("\nPAGES:", result["metadata"]["page_count"])
        print("\nSUMMARY:\n", result["summary"])
