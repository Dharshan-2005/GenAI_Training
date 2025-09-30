# 🚀 Career Copilot

<div align="center">

![Career Copilot Banner](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge\&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge\&logo=python)
![FastAPI](https://img.shields.io/badge/Streamlit-Latest-red?style=for-the-badge\&logo=streamlit)
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
* [Project Structure](#-project-structure)
* [Development](#-development)
* [Known Issues & Suggested Fixes](#-known-issues--suggested-fixes)
* [Contributing](#-contributing)
* [License](#-license)
* [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

Career Copilot is an AI-driven platform that helps users optimize resumes for ATS, perform skill-gap analysis, and practice realistic mock interviews (including speech-based interactions).

The **resume analyzer tool** is deployed via **Streamlit**, providing a simple, interactive dashboard for uploading resumes and viewing AI-powered analysis in real-time.

Unlike earlier versions, **no MongoDB database is required** — all operations are file/session-based and run in memory or via local file storage.

---

## ✨ Features

* **Resume Analyzer (Streamlit App)**

  * Upload PDF/DOCX/TXT resumes directly in the browser.
  * Extracts skills, education, and experience sections.
  * AI-enhanced optimization with ATS keyword alignment.
* **AI Interview System (optional FastAPI backend)**

  * Mock interview question generation.
  * Option for speech-to-text and text-to-speech.
  * Real-time scoring and analytics.
* **Skill Gap & Learning Roadmap**

  * Vector-based skill matching and learning recommendations.

---

## 🛠 Technology Stack

| Area       | Technology                                             |
| ---------- | ------------------------------------------------------ |
| Frontend   | Streamlit (for resume analyzer)                        |
| Backend    | FastAPI (for optional interview features)              |
| AI / LLM   | Ollama (LLama 3.2), OpenAI GPT-4 (optional)            |
| Deployment | Streamlit Cloud / Docker                               |
| Speech     | Google STT, TTS models                                 |
| Vector DB  | embeddings + similarity search (in-memory or external) |

---

## 🏗 Architecture

```
User Input (Resume / Audio)
        |
    Streamlit (resume analyzer UI)
        |
      FastAPI (optional for interviews)
        |
  --------------------------
  |                        |
Uploads (resumes/audio)  LLM Engine (Ollama / OpenAI)
```

---

## ✅ Quick Start (Dev)

**Streamlit Resume Analyzer**

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501) for the UI.

**FastAPI Interview Service (optional)**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🛠 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/career-copilot.git
cd career-copilot
```

2. Create `.env` (example)

```env
OPENAI_API_KEY=your_openai_api_key_here  # optional
OLLAMA_ENABLED=true
OLLAMA_HOST=http://localhost:11434
SECRET_KEY=your_random_secret
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

---

## 🧾 Usage (Streamlit)

* Go to [http://localhost:8501](http://localhost:8501)
* Upload your resume (PDF/DOCX/TXT)
* View parsed results, ATS keyword suggestions, and optimization tips

**Optional (FastAPI Interview Mode)**

* Upload resume via `/upload_resume/`
* Start mock interview session
* Submit answers (text or audio)
* Get real-time feedback

---

## 📚 API Documentation (FastAPI only)

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

---

## 📁 Project Structure (updated for Streamlit)

```
career-copilot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI (optional)
│   ├── streamlit_app.py     # Streamlit entrypoint (resume analyzer)
│   ├── routers/             # (only if FastAPI enabled)
│   ├── services/
│   └── utils/
├── uploads/                 # Resume/audio uploads
├── requirements.txt
├── Dockerfile
├── README.md
└── tests/
```

---

## 🧑‍💻 Development

Run Streamlit in watch mode:

```bash
streamlit run app/streamlit_app.py --server.runOnSave true
```

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

* Streamlit community
* OpenAI for GPT models
* Meta for LLAMA models
* FastAPI (for optional interview mode)
