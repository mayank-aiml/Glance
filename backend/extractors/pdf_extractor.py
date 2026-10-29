import os
from langchain_community.document_loaders import PyPDFLoader


def extract_pdf(file_path: str):
    """
    Extract text and metadata from a PDF file.

    Args:
        file_path: Path to the target PDF file.

    Returns:
        Dictionary containing raw text, metadata, and raw document pages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

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
    }

    return {
        "text": raw_text,
        "metadata": metadata,
        "documents": documents
    }
