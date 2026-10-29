# Glance — Universal Content Summarization Platform

<p align="center">
  <strong>Everything important, at a glance.</strong>
</p>

<p align="center">
  <a href="https://glance-demo.yourdomain.com"><strong>🌐 Live Application Demo</strong></a> &nbsp;|&nbsp;
  <a href="http://localhost:8000/docs"><strong>📖 API Documentation</strong></a> &nbsp;|&nbsp;
  <a href="https://github.com/mayank-aiml/Glance"><strong>💻 GitHub Repository</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-18-blue?logo=react&logoColor=white" alt="React 18" />
  <img src="https://img.shields.io/badge/Vite-6.0-646CFF?logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/LLM-Groq%20Cloud-F55036?logo=groq&logoColor=white" alt="Groq" />
  <img src="https://img.shields.io/badge/LangChain-1.4+-1C3C3C?logo=langchain&logoColor=white" alt="LangChain" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
</p>

---

## 🔗 Live Link Placeholder

> **Live Deployment:**  
> 🔗 `https://your-glance-deployment-url.vercel.app` *(Replace with your production deployment URL)*  
> 🔗 API Base URL: `https://your-glance-backend.onrender.com`

---

## 📌 Overview

**Glance** is a modern, minimalist, unified content summarization platform. It eliminates information overload by transforming lengthy YouTube videos, PDF documents, web pages, and raw text into concise, high-value summaries through a single, frictionless interface.

Whether you are a student preparing revision notes, a researcher analyzing dense papers, or an executive reviewing briefings, Glance delivers exactly what matters without fluff or hallucination.

---

## ✨ Features

- 🎥 **YouTube Video Summarizer**
  - Instant transcript retrieval using `youtube-transcript-api` and `yt-dlp`.
  - Extracts rich video metadata (title, channel, duration, view count).
  - Handles videos and YouTube Shorts seamlessly.

- 📄 **PDF & Document Summarizer**
  - Drag-and-drop document upload with client-side file validation (up to 20MB).
  - Multi-page extraction via `pypdf`.
  - Automatically isolates and merges dense sections into structured reports.

- 🌐 **Website & Article Summarizer**
  - High-speed content extraction via `BeautifulSoup` and browser-mimicking headers.
  - Automatically strips away ads, navigation bars, footers, and tracking scripts.
  - Robust SSL fallback handling for diverse web sources.

- ✍️ **Plain Text Summarizer**
  - Live character counter (50,000 char capacity) and word counter.
  - Custom title labeling and quick-clear functionality.

- 🎯 **Four Tailored Summary Formats**
  - **Quick Summary**: Crisp overview with 5–7 high-impact takeaways.
  - **Detailed Summary**: Structured multi-section report with in-depth narrative and facts.
  - **Study Notes**: Key concepts, definitions, breakdowns, and 5 revision self-test questions.
  - **Executive Brief**: Strategic high-level summary, key metrics, and actionable recommendations.

- 🎨 **Design & User Experience**
  - Minimalist, distraction-free aesthetic with smooth micro-animations.
  - Seamless Light / Dark / System theme switching (stored in `localStorage` without flash).
  - One-click copy to clipboard and `.txt` file download.
  - Safe, custom-built markdown rendering with section hierarchy and code styling.

---

## 🏗️ Architecture & Technology Stack

```
Glance/
├── backend/                  # FastAPI Application & AI Engine
│   ├── api/                  # Modular route controllers
│   ├── extractors/           # YouTube, PDF, Webpage & Text content extractors
│   ├── prompts/              # Multi-format LangChain PromptTemplates
│   ├── schemas/              # Pydantic validation models
│   ├── services/             # Core Map-Reduce summarization chains & LLM service
│   ├── tests/                # Automated pytest test suite
│   ├── utils/                # Token reduction & text preprocessing
│   ├── main.py               # Application entrypoint & CORS middleware
│   └── requirements.txt      # Pinned Python dependencies
│
└── frontend/                 # React 18 + Vite SPA
    ├── src/
    │   ├── components/       # Reusable UI components (Navbar, Footer, FileUpload, etc.)
    │   ├── config/           # Social links & app constants
    │   ├── hooks/            # Custom hooks (theme switcher)
    │   ├── pages/            # View pages (Home, YouTube, Document, Website, Text)
    │   ├── services/         # Centralized API client layer
    │   └── styles/           # Theme tokens and global CSS variables
    └── package.json
```

### AI Pipeline & Token Optimization
1. **Extraction**: Raw content is extracted via specialized parsers.
2. **Preprocessing**: In `preprocess.py`, content is cleansed of boilerplate, excessive whitespace, and noise, then chunked within strict token boundaries using `tiktoken`.
3. **Map Phase**: Each chunk is independently distilled by Groq LLMs using domain-tailored prompts.
4. **Reduce Phase**: Section summaries are synthesized into the user's requested output format.

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**
- **Groq Cloud API Key** (obtainable free at [console.groq.com](https://console.groq.com))

---

### 1. Clone the Repository
```bash
git clone https://github.com/mayank-aiml/Glance.git
cd Glance
```

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `backend/.env` with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=Glance
```

Start the backend development server:
```bash
python main.py
```
> The API will be available at `http://127.0.0.1:8000` (Interactive docs at `http://127.0.0.1:8000/docs`).

---

### 3. Frontend Setup

Open a new terminal tab:
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
> The web application will launch at `http://localhost:5173`.

---

## 🧪 Running Tests

The backend includes a comprehensive test suite covering data preprocessing, route validation, prompt templates, and error handling.

```bash
cd backend
pytest -v
```

---

## 📡 API Reference

| Method | Endpoint | Description | Payload |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/summarize/youtube` | Summarize a YouTube video or short | `{"url": "...", "summary_type": "detailed"}` |
| `POST` | `/api/summarize/document` | Summarize an uploaded PDF | Multipart `file`, `summary_type` |
| `POST` | `/api/summarize/website` | Summarize an online article/webpage | `{"url": "...", "summary_type": "quick"}` |
| `POST` | `/api/summarize/text` | Summarize raw text content | `{"text": "...", "summary_type": "study_notes"}` |
| `GET` | `/api/health` | Service health status check | None |

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Crafted with care by <strong>Mayank Tiwari</strong><br />
  <a href="https://www.linkedin.com/in/mayank-kailas-tiwari/">LinkedIn</a> &nbsp;•&nbsp;
  <a href="https://github.com/mayank-aiml">GitHub</a> &nbsp;•&nbsp;
  <a href="https://mayankt.tech">Portfolio</a>
</p>

