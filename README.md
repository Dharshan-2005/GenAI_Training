# 🚀 Career Copilot

<div align="center">

![Career Copilot Banner](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge\&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge\&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge\&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

# Career Copilot

**AI-Powered Resume Optimization & Interview Preparation Platform**

> Transform your job search with intelligent resume analysis, ATS optimization, and realistic AI-guided mock interviews.

---

## 📋 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [Technology Stack](#-technology-stack)
* [Architecture](#-architecture)
* [Quick Start (Dev)](#-quick-start-dev)
* [Installation](#-installation)
* [Usage](#-usage)
* [API Documentation](#-api-documentation)
* [Project Structure](#-project-structure)
* [Development](#-development)
* [Known Issues & Suggested Fixes](#-known-issues--suggested-fixes)
* [Contributing](#-contributing)
* [License](#-license)
* [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

Career Copilot is an AI-driven platform that helps users optimize resumes for ATS, perform skill-gap analysis, and practice realistic mock interviews (including speech-based interactions).

It combines LLMs, vector search for skills, and audio processing to create a feedback loop for continuous improvement.

---

## ✨ Features

* **Resume Management**

  * Upload PDFs/DOCX/TXT and parse sections (skills, experience, education).
  * ATS-aware rewrites with keyword highlighting and action-verb suggestions.
* **AI Interview System**

  * Dynamic mock interviews generated from the candidate's resume.
  * Speech-to-text (STT) and text-to-speech (TTS) support for natural practice.
  * Session tracking, scoring, and analytics.
* **Skill Gap & Learning Roadmap**

  * Vector-based skill comparison and personalized learning suggestions.
* **Security & Reliability**

  * CORS, security headers, robust logging, and session management.

---

## 🛠 Technology Stack

| Area       | Technology                                                        |
| ---------- | ----------------------------------------------------------------- |
| Frontend   | HTML, Jinja2 Templates (optionally React + Vite/Tailwind for SPA) |
| Backend    | FastAPI, Python 3.11                                              |
| Database   | MongoDB                                                           |
| Deployment | Uvicorn, Docker                                                   |
| AI / LLM   | Ollama (LLama 3.2), OpenAI GPT-4 (optional)                       |
| Speech     | Google STT, TTS models                                            |
| Vector DB  | embeddings + similarity search                                    |

---

## 🏗 Architecture

```
User Input (Resume / Audio)
        |
    FastAPI Backend
    |  - resume parsing
    |  - interview agent
    |  - audio processing
    |
  --------------------------
  |                        |
MongoDB                 LLM Engine (Ollama / OpenAI)
  |                        |
Uploads (resumes/audio)  Vector DB (embeddings / search)
```

---

## ✅ Quick Start (Dev)

**Unix / macOS**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# If main.py is at repo root:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# If you moved entrypoint to app/main.py:
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit [http://localhost:8000](http://localhost:8000) or [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## 🛠 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/career-copilot.git
cd career-copilot
```

2. Create `.env` (example)

```env
MONGODB_URI=mongodb://localhost:27017/career_copilot
OPENAI_API_KEY=your_openai_api_key_here  # optional
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
SECRET_KEY=your_random_secret
```

3. Install dependencies and run (see Quick Start above).

4. (Optional) Docker

```bash
# Build
docker build -t career-copilot:latest .
# Run (example)
docker run --env-file .env -p 8000:8000 career-copilot:latest
```

---

## 🧾 Usage (API Examples)

**Upload Resume**

```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@resume.pdf"
```

**Start Interview Session**

```bash
curl -X POST "http://localhost:8000/upload_resume/" \
  -F "resume=@resume.pdf" \
  -F "model_choice=llama3.2"
```

**Submit Audio Answer**

```bash
curl -X POST "http://localhost:8000/ask/" \
  -F "session_id=your-session-id" \
  -F "audio=@answer.wav"
```

---

## 📚 API Documentation

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

**Key Endpoints (examples)**

| Method | Endpoint                                | Description                  |
| -----: | --------------------------------------- | ---------------------------- |
|    GET | `/health`                               | Server health check          |
|   POST | `/api/upload-resume`                    | Upload and parse resume      |
|   POST | `/upload_resume/`                       | Initialize interview session |
|   POST | `/ask/`                                 | Submit audio answer          |
|    GET | `/audio/{session_id}/{question_number}` | Retrieve recorded answer     |
| DELETE | `/session/{session_id}`                 | End interview session        |
|    GET | `/session/{session_id}/status`          | Session progress             |

---

## 📁 Project Structure 

> **Note:** your original structure mixes files at root and inside `app/`. I recommend a single entrypoint (either `main.py` at root or `app/main.py`) and `app/` containing package code.

```
career-copilot/
├── Dockerfile
├── README.md  # this file
├── requirements.txt
├── .env.example
├── main.py                # optional root entrypoint (or use app/main.py)
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app factory (recommended)
│   ├── routers/           # API route handlers
│   │   ├── resume.py
│   │   ├── interview.py
│   │   └── audio.py
│   ├── models/
│   │   ├── resume.py
│   │   ├── session.py
│   │   └── user.py
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── interview_agent.py
│   │   ├── audio_processor.py
│   │   └── llm_service.py
│   └── utils/
│       ├── file_handler.py
│       ├── validators.py
│       └── logger.py
├── templates/             # Jinja2 templates (if used)
│   ├── index.html
│   ├── dashboard.html
│   └── interview.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── uploads/
│   ├── resumes/
│   └── audio/
└── tests/
    ├── test_resume.py
    ├── test_interview.py
    └── test_api.py
```

**Entrypoint guidance**

* If you keep `main.py` at repo root, use: `uvicorn main:app`.
* If you move to `app/main.py`, use: `uvicorn app.main:app`.

**Why reorganize?**

* Keeps package imports predictable (use `from app.services import ...`).
* Simplifies Dockerfile and module resolution.
* Makes tests and CI easier to configure.

---

## 🐞 Known Issues & Suggested Fixes

1. **"Project structure is not proper"**

   * Move all application code under `app/` and make `main.py` an entrypoint that imports from `app`.
   * Update `PYTHONPATH` or use `pip install -e .` during development to avoid relative import issues.
2. **Git submodule warning**

   * If you accidentally added a nested Git repo (e.g., `interviewbot_backend`), either remove it from the parent repo or properly add it as a submodule: `git submodule add <url> path`.
3. **Static files & templates**

   * Ensure `templates/` and `static/` are referenced correctly when using `FastAPI`'s `Jinja2Templates` and `StaticFiles`.
4. **Environment management in Docker**

   * Use an `.env` file or pass environment variables at runtime; don't hardcode secrets.

---

## 🧑‍💻 Development

Recommended developer workflow:

```bash
# create editable install so imports resolve
python -m pip install -e .
# run tests
pytest -q
# run linting
flake8 app
# run the server (see Quick Start)
```

Consider adding `pre-commit` hooks for formatting and linting (black, isort, flake8).

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/Awesome`
3. Commit your changes: `git commit -m "Add awesome feature"`
4. Push and open a Pull Request

Please follow the code style and include tests for new features.

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

* OpenAI for GPT models
* Meta for LLAMA models
* FastAPI community
* All contributors

---



