import io
import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app
from prompts.document_prompts import get_document_combine_prompt

client = TestClient(app)

def test_document_prompts():
    for mode in ["quick", "detailed", "study_notes", "executive"]:
        prompt = get_document_combine_prompt(mode)
        assert prompt is not None
        assert "text" in prompt.input_variables

def test_document_non_pdf_upload():
    # Non-pdf file rejection test
    fake_txt_file = io.BytesIO(b"Hello world this is a test text file.")
    res = client.post(
        "/api/summarize/document",
        files={"file": ("sample.txt", fake_txt_file, "text/plain")},
        data={"summary_type": "quick"}
    )
    assert res.status_code == 400
    assert "Only PDF documents are currently supported" in res.json()["detail"]
