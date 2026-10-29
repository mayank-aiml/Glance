import asyncio
import logging
from fastapi import APIRouter, HTTPException, status
from schemas.request_models import WebsiteSummarizeRequest
from schemas.response_models import SummaryResponse
from services.website_summarizer import summarize_website

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarize", tags=["Website Summarization"])

@router.post("/website", response_model=SummaryResponse)
async def api_summarize_website(payload: WebsiteSummarizeRequest):
    try:
        result = await asyncio.to_thread(
            summarize_website,
            str(payload.url),
            payload.summary_type
        )
        return SummaryResponse(
            summary=result["summary"],
            metadata=result.get("metadata", {})
        )
    except Exception as exc:
        logger.exception("Error during website summarization: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc) or "Failed to summarize website."
        )
