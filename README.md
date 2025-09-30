# 🚀 Career Copilot

<div align="center">

![Career Copilot Banner](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

*AI-Powered Resume Optimization & Interview Preparation Platform*

Transform your job search with intelligent resume analysis, ATS optimization, and realistic AI-guided mock interviews.

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

*Career Copilot* is an advanced AI-driven platform that revolutionizes job preparation by combining cutting-edge language models, vector-based skill analysis, and speech recognition technologies. Whether you're optimizing your resume for ATS systems or preparing for technical interviews, Career Copilot provides personalized, intelligent assistance every step of the way.

### Why Career Copilot?

- *End-to-End Solution*: From resume parsing to mock interviews, everything in one platform
- *AI-Powered Intelligence*: Leverages GPT-4 and LLAMA 3.2 for human-like interactions
- *Real-Time Feedback*: Get instant analysis and improvement suggestions
- *Voice-Based Interviews*: Practice with realistic audio-based mock interviews
- *ATS Optimization*: Ensure your resume passes automated screening systems

---

## ✨ Features

### 📄 Resume Management

- *Smart Upload & Parsing*
  - Support for PDF, DOCX, and TXT formats
  - Automatic extraction of skills, experience, and education
  - Secure file handling with UUID-based storage

- *AI Resume Optimization*
  - LLM-powered resume rewriting aligned with job descriptions
  - Keyword analysis and ATS-friendly formatting
  - Action verb suggestions and content enhancement

- *Skill Gap Analysis*
  - Vector-based skill benchmarking
  - Personalized learning roadmap generation
  - Industry-standard competency mapping

### 🎤 AI Interview System

- *Interactive Mock Interviews*
  - Speech-to-text conversion for natural responses
  - Text-to-speech AI interviewer
  - Dynamic question generation based on your resume

- *Session Management*
  - Track interview progress and question count
  - Save and retrieve interview sessions
  - Real-time feedback and performance analytics

- *Audio Processing*
  - High-quality speech recognition via Google STT
  - Natural-sounding TTS responses
  - Automatic audio file management

### 🔒 Security & Performance

- CORS middleware for secure cross-origin requests
- Custom security headers (X-Content-Type-Options, X-Frame-Options)
- Robust error handling and logging
- Efficient concurrent session management

---

## 🛠 Technology Stack

<table>
<tr>
<td align="center" width="25%">
<b>Frontend</b><br>
HTML<br>
Jinja2 Templates
</td>
<td align="center" width="25%">
<b>Backend</b><br>
FastAPI<br>
Python 3.11
</td>
<td align="center" width="25%">
<b>Database</b><br>
MongoDB
</td>
<td align="center" width="25%">
<b>Deployment</b><br>
Uvicorn<br>
Docker
</td>
</tr>
<tr>
<td align="center" width="25%">
<b>AI/LLM</b><br>
LLAMA 3.2<br>
OpenAI GPT-4<br>
Ollama
</td>
<td align="center" width="25%">
<b>Speech</b><br>
Google STT<br>
TTS Models
</td>
<td align="center" width="25%">
<b>Vector DB</b><br>
Embeddings<br>
Similarity Search
</td>
<td align="center" width="25%">
<b>Tools</b><br>
Docker<br>
Git
</td>
</tr>
</table>

---

## 🏗 Architecture


┌─────────────────┐
│   User Input    │
│  (Resume/Audio) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
├─────────────────┤
│ • Resume Parser │
│ • Session Mgmt  │
│ • API Routes    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ MongoDB│ │  AI/LLM  │
│        │ │  Engine  │
│ • User │ │ • GPT-4  │
│ • Data │ │ • LLAMA  │
└────────┘ └──────────┘
              │
         ┌────┴────┐
         │         │
         ▼         ▼
    ┌─────────┐ ┌──────┐
    │ STT/TTS │ │Vector│
    │ Audio   │ │  DB  │
    └─────────┘ └──────┘


---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- MongoDB instance
- Ollama (for LLAMA models)
- OpenAI API key (optional, for GPT-4)

### Step 1: Clone the Repository

bash
git clone https://github.com/yourusername/career-copilot.git
cd career-copilot


### Step 2: Create Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### Step 3: Install Dependencies

bash
pip install -r requirements.txt


### Step 4: Set Up Environment Variables

Create a .env file in the root directory:

env
MONGODB_URI=mongodb://localhost:27017/
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here


### Step 5: Install and Start Ollama

bash
# Install Ollama (visit https://ollama.ai for instructions)
# Pull required models
ollama pull llama3.2


### Step 6: Run the Application

bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Visit http://localhost:8000 in your browser!

---

## 🎮 Usage

### Upload and Optimize Resume

1. Navigate to the dashboard
2. Upload your resume (PDF, DOCX, or TXT)
3. Receive AI-powered optimization suggestions
4. Download your enhanced resume

### Start Mock Interview

1. Upload your resume
2. Click "Start Interview"
3. Answer questions using your microphone
4. Receive real-time feedback and follow-up questions
5. Review session analytics and performance

### API Examples

#### Upload Resume
bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@resume.pdf"


#### Start Interview Session
bash
curl -X POST "http://localhost:8000/upload_resume/" \
  -F "resume=@resume.pdf" \
  -F "model_choice=llama3.2"


#### Submit Audio Answer
bash
curl -X POST "http://localhost:8000/ask/" \
  -F "session_id=your-session-id" \
  -F "audio=@answer.wav"


---

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- *Swagger UI*: http://localhost:8000/docs
- *ReDoc*: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Check server status |
| POST | /api/upload-resume | Upload and parse resume |
| POST | /upload_resume/ | Initialize interview session |
| POST | /ask/ | Submit audio answer |
| GET | /audio/{session_id}/{question_number} | Retrieve audio response |
| DELETE | /session/{session_id} | End interview session |
| GET | /session/{session_id}/status | Check session progress |

---

## 📁 Project Structure


career-copilot/
│
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── Dockerfile             # Docker configuration
│
├── app/
│   ├── routers/           # API route handlers
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic
│   │   ├── resume_parser.py
│   │   ├── interview_agent.py
│   │   └── audio_processor.py
│   └── utils/             # Helper functions
│
├── templates/             # Jinja2 HTML templates
├── static/                # CSS, JS, images
├── uploads/               # Temporary file storage
└── tests/                 # Unit and integration tests


---

## 👥 Team

<table>
<tr>
<td align="center">
<b>Karunyan V T</b><br>
</td>
<td align="center">
<b>Jaya Jayanthan S</b><br>
</td>
<td align="center">
<b>Naveen G G</b><br>
</td>
</tr>
<tr>
<td align="center">
<b>Dharshan H</b><br>
</td>
<td align="center">
<b>Keerthi Selvan S</b><br>
</td>
<td align="center">
<b>Hari K</b><br>
</td>
</tr>
</table>

---

## 🗺 Roadmap

### Phase 1 (Current)
- ✅ Resume upload and parsing
- ✅ AI-powered resume optimization
- ✅ Voice-based mock interviews
- ✅ Session management

### Phase 2 (Upcoming)
- 🔄 Job recommendation engine
- 🔄 Industry trends dashboard
- 🔄 Advanced analytics and insights
- 🔄 Multi-language support

### Phase 3 (Future)
- 📋 Company-specific interview preparation
- 📋 Salary negotiation assistant
- 📋 Career path visualization
- 📋 Integration with job boards

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. *Fork the repository*
2. *Create your feature branch*
   bash
   git checkout -b feature/AmazingFeature
   
3. *Commit your changes*
   bash
   git commit -m 'Add some AmazingFeature'
   
4. *Push to the branch*
   bash
   git push origin feature/AmazingFeature
   
5. *Open a Pull Request*

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Meta for LLAMA models
- FastAPI community
- All our contributors and supporters

---

## 📞 Contact & Support

- *Issues*: [GitHub Issues](https://github.com/yourusername/career-copilot/issues)
- *Discussions*: [GitHub Discussions](https://github.com/yourusername/career-copilot/discussions)
- *Email*: support@careercopilot.ai

---

<div align="center">

*Made with ❤ by the Career Copilot Team*

⭐ Star us on GitHub — it motivates us a lot!

[Back to Top](#-career-copilot)

</div>
