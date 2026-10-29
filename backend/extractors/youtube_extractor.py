import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def extract_youtube(youtube_url: str):
    """
    Extract video metadata and clean transcript from a YouTube URL.

    Args:
        youtube_url: Full YouTube video URL.

    Returns:
        Dictionary containing video metadata, transcript, and video ID.
    """
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
    }

    video_id = info.get("id")

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    formatter = TextFormatter()
    clean_text = formatter.format_transcript(transcript)

    return {
        "metadata": metadata,
        "transcript": clean_text,
        "video_id": video_id
    }
