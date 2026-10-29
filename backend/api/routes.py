from fastapi import APIRouter
from api.youtube_routes import router as youtube_router
from api.document_routes import router as document_router
from api.website_routes import router as website_router
from api.text_routes import router as text_router

api_router = APIRouter(prefix="/api")

api_router.include_router(youtube_router)
api_router.include_router(document_router)
api_router.include_router(website_router)
api_router.include_router(text_router)

@api_router.get("/health")
async def health_check():
    return {"status": "ok", "service": "Glance API"}
