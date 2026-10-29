import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from prompts.youtube_prompts import get_youtube_combine_prompt

client = TestClient(app)

def test_youtube_prompts():
    for mode in ["quick", "detailed", "study_notes", "executive"]:
        prompt = get_youtube_combine_prompt(mode)
        assert prompt is not None
        assert "text" in prompt.input_variables

def test_youtube_invalid_url_handling():
    res = client.post("/api/summarize/youtube", json={"url": "https://not-youtube.com/something", "summary_type": "detailed"})
    # Should catch error gracefully and return 500 with detail
    assert res.status_code == 500
    assert "detail" in res.json()
