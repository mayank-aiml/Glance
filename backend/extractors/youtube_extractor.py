import re
import logging
import requests
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

logger = logging.getLogger(__name__)


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats without making network requests.
    Supports standard watch URLs, youtu.be, shorts, and embed URLs.
    """
    if not url:
        return ""

    patterns = [
        r"(?:v=|\/v\/|embed\/|shorts\/|youtu\.be\/|\/e\/)([a-zA-Z0-9_-]{11})",
        r"(?:[\?&]v=)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    try:
        parsed = urlparse(url)
        if "youtube.com" in parsed.netloc:
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]
        elif "youtu.be" in parsed.netloc:
            return parsed.path.lstrip("/").split("/")[0]
    except Exception:
        pass

    return ""


def get_video_metadata(video_id: str, youtube_url: str) -> dict:
    """
    Fetch video metadata using YouTube's official public oEmbed API.
    Does NOT require authentication or cookies and avoids bot-detection blocks on cloud hosts.
    """
    metadata = {
        "title": f"YouTube Video ({video_id})",
        "channel": "YouTube Creator",
        "duration": None,
        "view_count": None,
        "like_count": None,
    }

    # 1. Primary: YouTube official oEmbed API (fast, unauthenticated, never blocked on Render/AWS)
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        res = requests.get(oembed_url, timeout=8)
        if res.status_code == 200:
            data = res.json()
            metadata["title"] = data.get("title", metadata["title"])
            metadata["channel"] = data.get("author_name", metadata["channel"])
            metadata["author_url"] = data.get("author_url")
            return metadata
    except Exception as exc:
        logger.debug("oEmbed metadata fetch failed for %s: %s", video_id, exc)

    # 2. Secondary fallback: yt-dlp (optional best-effort if available and unblocked)
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
            "socket_timeout": 5,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            metadata["title"] = info.get("title") or metadata["title"]
            metadata["channel"] = info.get("channel") or metadata["channel"]
            metadata["duration"] = info.get("duration")
            metadata["view_count"] = info.get("view_count")
            metadata["like_count"] = info.get("like_count")
    except Exception as exc:
        logger.debug("yt-dlp fallback skipped: %s", exc)

    return metadata


def get_video_transcript(video_id: str) -> str:
    """
    Fetch and format transcript using YouTubeTranscriptApi.
    """
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
    except AttributeError:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

    formatter = TextFormatter()
    return formatter.format_transcript(transcript)


def extract_youtube(youtube_url: str) -> dict:
    """
    Extract video metadata and clean transcript from a YouTube URL.

    Args:
        youtube_url: Full YouTube video URL.

    Returns:
        Dictionary containing video metadata, transcript, and video ID.
    """
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError(f"Could not extract a valid YouTube video ID from: {youtube_url}")

    metadata = get_video_metadata(video_id, youtube_url)
    clean_text = get_video_transcript(video_id)

    if not clean_text or not clean_text.strip():
        raise ValueError("Could not extract any transcript text from this video.")

    return {
        "metadata": metadata,
        "transcript": clean_text,
        "video_id": video_id,
    }
