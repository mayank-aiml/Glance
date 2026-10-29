import asyncio
import logging
from fastapi import APIRouter, HTTPException, status
from schemas.request_models import YoutubeSummarizeRequest
from schemas.response_models import SummaryResponse
from services.youtube_summarizer import summarize_youtube

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarize", tags=["YouTube Summarization"])

@router.post("/youtube", response_model=SummaryResponse)
async def api_summarize_youtube(payload: YoutubeSummarizeRequest):
    try:
        result = await asyncio.to_thread(
            summarize_youtube,
            str(payload.url),
            payload.summary_type
        )
        return SummaryResponse(
            summary=result["summary"],
            metadata=result.get("metadata", {})
        )
    except Exception as exc:
        logger.exception("Error during YouTube summarization: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or "Failed to summarize YouTube video."
        )
