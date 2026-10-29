from typing import Optional, Literal
from pydantic import BaseModel, Field, HttpUrl

SummaryType = Literal["quick", "detailed", "study_notes", "executive"]

class YoutubeSummarizeRequest(BaseModel):
    url: str = Field(..., description="Valid YouTube video or shorts URL")
    summary_type: SummaryType = Field(default="detailed", description="Target summary format")

class WebsiteSummarizeRequest(BaseModel):
    url: str = Field(..., description="Target webpage URL to summarize")
    summary_type: SummaryType = Field(default="detailed", description="Target summary format")

class TextSummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Raw text content to summarize")
    title: Optional[str] = Field(default="Raw Text", description="Optional title label for the text")
    summary_type: SummaryType = Field(default="detailed", description="Target summary format")
