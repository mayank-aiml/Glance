import asyncio
import logging
from fastapi import APIRouter, HTTPException, status
from schemas.request_models import TextSummarizeRequest
from schemas.response_models import SummaryResponse
from services.text_summarizer import summarize_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarize", tags=["Text Summarization"])

@router.post("/text", response_model=SummaryResponse)
async def api_summarize_text(payload: TextSummarizeRequest):
    try:
        result = await asyncio.to_thread(
            summarize_text,
            payload.text,
            payload.title or "Raw Text",
            payload.summary_type
        )
        return SummaryResponse(
            summary=result["summary"],
            metadata=result.get("metadata", {})
        )
    except Exception as exc:
        logger.exception("Error during text summarization: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or "Failed to summarize text."
        )
