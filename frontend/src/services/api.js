const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function handleResponse(res) {
  if (!res.ok) {
    let message = `Server error: ${res.status}`;
    try {
      const data = await res.json();
      message = data.detail || data.message || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}

export async function summarizeYoutube({ url, summary_type }) {
  const res = await fetch(`${BASE_URL}/api/summarize/youtube`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, summary_type }),
  });
  return handleResponse(res);
}

export async function summarizeDocument({ file, summary_type }) {
  const form = new FormData();
  form.append('file', file);
  form.append('summary_type', summary_type);
  const res = await fetch(`${BASE_URL}/api/summarize/document`, {
    method: 'POST',
    body: form,
    // Do NOT set Content-Type — browser sets multipart boundary automatically
  });
  return handleResponse(res);
}

export async function summarizeWebsite({ url, summary_type }) {
  const res = await fetch(`${BASE_URL}/api/summarize/website`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, summary_type }),
  });
  return handleResponse(res);
}

export async function summarizeText({ text, summary_type }) {
  const res = await fetch(`${BASE_URL}/api/summarize/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, summary_type }),
  });
  return handleResponse(res);
}
