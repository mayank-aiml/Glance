import logging
import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress insecure request warnings if fallback verify=False is needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
}


def clean_html_content(html: str) -> tuple[str, str]:
    """Extract page title and clean article/body text from raw HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Get page title
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Remove non-content tags
    for tag in soup([
        "script",
        "style",
        "noscript",
        "iframe",
        "svg",
        "canvas",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
        "button",
        "input",
    ]):
        tag.decompose()

    # Look for main semantic content blocks first
    main_node = (
        soup.find("article")
        or soup.find("main")
        or soup.find(id="content")
        or soup.find(class_="post-content")
        or soup.find("body")
        or soup
    )

    # Extract text with newlines
    content = main_node.get_text(separator="\n", strip=True)

    return title, content


def fetch_website(url: str) -> dict:
    """
    Fetch and extract readable content from a website using standard HTTP requests.
    Compatible with asyncio event loops and avoids Playwright Sync API errors.

    Args:
        url: Full website URL.

    Returns:
        Dictionary containing url, title, and cleaned content text.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    session = requests.Session()
    session.headers.update(BROWSER_HEADERS)

    html = ""
    # 1. Primary attempt with strict SSL verification
    try:
        response = session.get(url, timeout=20, allow_redirects=True)
        response.raise_for_status()
        html = response.text
    except Exception as err:
        logger.warning("Primary fetch failed for %s (%s). Retrying with permissive SSL.", url, err)
        try:
            # 2. Fallback attempt for self-signed or legacy SSL sites
            response = session.get(url, timeout=25, verify=False, allow_redirects=True)
            response.raise_for_status()
            html = response.text
        except Exception as fallback_err:
            raise ValueError(f"Failed to fetch content from {url}: {fallback_err}")

    if not html or not html.strip():
        raise ValueError(f"Empty response received from: {url}")

    title, content = clean_html_content(html)

    if not content or len(content.strip()) < 40:
        raise ValueError(f"Could not extract sufficient text content from: {url}")

    return {
        "url": url,
        "title": title or url,
        "content": content
    }


# Example / Manual verification
if __name__ == "__main__":
    sample_url = "https://en.wikipedia.org/wiki/Earth"
    result = fetch_website(sample_url)
    print("TITLE:", result["title"])
    print("LENGTH:", len(result["content"]))
    print("PREVIEW:\n", result["content"][:300])
