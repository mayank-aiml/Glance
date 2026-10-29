import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from prompts.website_prompts import get_website_combine_prompt

client = TestClient(app)

def test_website_prompts():
    for mode in ["quick", "detailed", "study_notes", "executive"]:
        prompt = get_website_combine_prompt(mode)
        assert prompt is not None
        assert "text" in prompt.input_variables

def test_website_invalid_url_handling():
    res = client.post("/api/summarize/website", json={"url": "http://invalid-non-existent-site-xyz-1234.org", "summary_type": "detailed"})
    assert res.status_code == 500
    assert "detail" in res.json()
