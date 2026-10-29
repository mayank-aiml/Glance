import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from utils.preprocess import preprocess_text
from prompts.text_prompts import get_text_combine_prompt

client = TestClient(app)

def test_preprocess_text_clean():
    sample = "Hello world! This is a test.   \n\n\n  Multiple spaces   and newlines."
    result = preprocess_text(sample)
    assert isinstance(result, str)
    assert "Hello world!" in result
    assert "  " not in result

def test_text_prompts():
    for mode in ["quick", "detailed", "study_notes", "executive"]:
        prompt = get_text_combine_prompt(mode)
        assert prompt is not None
        assert "text" in prompt.input_variables

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "Glance API"}

def test_text_summarize_validation_error():
    # Less than 10 characters should fail validation
    res = client.post("/api/summarize/text", json={"text": "Short", "summary_type": "quick"})
    assert res.status_code == 422
