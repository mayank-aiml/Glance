import os
from pathlib import Path
from dotenv import load_dotenv
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
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
from prompts.youtube_prompts import YT_MAP_PROMPT, get_youtube_combine_prompt
from services.llm_service import get_llm


def summarize_youtube(youtube_url, summary_type="detailed", token_limit=4500):

    # --------------------------------------------------
    # 1. Get video metadata
    # --------------------------------------------------

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)

    metadata = {
        "title": info.get("title"),
        "channel": info.get("channel"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "summary_type": summary_type,
    }


    # --------------------------------------------------
    # 2. Extract video ID
    # --------------------------------------------------

    video_id = info.get("id")


    # --------------------------------------------------
    # 3. Get transcript
    # --------------------------------------------------

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(video_id)

    formatter = TextFormatter()

    clean_text = formatter.format_transcript(transcript)


    # --------------------------------------------------
    # 4. Preprocess transcript
    # --------------------------------------------------

    result = preprocess_text(
        clean_text,
        token_limit=token_limit
    )


    # --------------------------------------------------
    # 5. Convert chunks into LangChain Documents
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
    # 6. Initialize Groq LLM
    # --------------------------------------------------

    llm = get_llm()


    # --------------------------------------------------
    # 7. Create Map-Reduce summarization chain
    # --------------------------------------------------

    combine_prompt = get_youtube_combine_prompt(summary_type)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=YT_MAP_PROMPT,
        combine_prompt=combine_prompt
    )


    # --------------------------------------------------
    # 8. Generate summary
    # --------------------------------------------------

    output = summary_chain.invoke({
        "input_documents": documents
    })

    summary = output["output_text"]


    # --------------------------------------------------
    # 9. Return everything
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
    youtube_url = "https://youtu.be/WT2bjBAdYYU?si=FRH14QKLBdGbIaY0"

    result = summarize_youtube(youtube_url)

    print("\nTITLE:")
    print(result["metadata"]["title"])

    print("\nCHANNEL:")
    print(result["metadata"]["channel"])

    print("\nSUMMARY:")
    print(result["summary"])
