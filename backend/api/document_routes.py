import os
import shutil
import tempfile
import asyncio
import logging
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, status
from schemas.response_models import SummaryResponse
from services.document_summarizer import summarize_document

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarize", tags=["Document Summarization"])

@router.post("/document", response_model=SummaryResponse)
async def api_summarize_document(
    file: UploadFile = File(...),
    summary_type: str = Form(default="detailed")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are currently supported."
        )

    # Save uploaded file safely to a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = await asyncio.to_thread(
            summarize_document,
            temp_file_path,
            summary_type
        )
        return SummaryResponse(
            summary=result["summary"],
            metadata=result.get("metadata", {})
        )
    except Exception as exc:
        logger.exception("Error during document summarization: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or "Failed to summarize PDF document."
        )
    finally:
        # Clean up temporary directory and file
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
