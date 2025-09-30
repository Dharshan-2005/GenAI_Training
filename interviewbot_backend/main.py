import os
import uuid
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from interview_agent import InterviewAgent, test_ollama_models
from resume_parser import parse_resume
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Interview System", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

STATIC_AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(STATIC_AUDIO_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Active sessions
sessions = {}

@app.get("/")
async def root():
    return {"message": "AI Interview System API", "status": "running"}

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {allowed_extensions}")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    resume_text = parse_resume(file_path)
    if not resume_text or len(resume_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume content too short")

    session_id = str(uuid.uuid4())
    agent = InterviewAgent(resume_text)
    sessions[session_id] = {'agent': agent, 'file_path': file_path}

    first_question, audio_path = agent.interview_turn()
    return {
        "status": "success",
        "session_id": session_id,
        "first_question": first_question,
        "audio_path": audio_path
    }

@app.post("/ask/")
async def ask_question(session_id: str = Form(...), user_answer_audio: UploadFile = File(...)):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Invalid session ID")
    session = sessions[session_id]
    agent = session['agent']

    # Save user audio temporarily
    user_audio_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{user_answer_audio.filename}")
    with open(user_audio_path, "wb") as f:
        f.write(await user_answer_audio.read())

    # Transcribe
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(user_audio_path) as source:
            audio_data = recognizer.record(source)
            user_answer = recognizer.recognize_google(audio_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"STT failed: {str(e)}")
    finally:
        if os.path.exists(user_audio_path):
            os.remove(user_audio_path)

    ai_response, audio_path = agent.interview_turn(user_answer.strip())
    return {
        "status": "success",
        "transcribed_answer": user_answer,
        "ai_response": ai_response,
        "audio_path": audio_path,
        "question_number": agent.question_count
    }

@app.get("/audio/{session_id}/{question_number}")
async def get_audio(session_id: str, question_number: int):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Use STATIC_AUDIO_DIR instead of uploads
    audio_path = os.path.join(STATIC_AUDIO_DIR, f"{session['agent'].session_id}_q{question_number}.mp3")
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # Serve as MP3
    return FileResponse(audio_path, media_type="audio/mpeg")


@app.delete("/session/{session_id}")
async def end_session(session_id: str):
    session = sessions.get(session_id)
    if session:
        # Remove resume
        if os.path.exists(session['file_path']):
            os.remove(session['file_path'])
        # Remove AI audio
        agent = session['agent']
        for i in range(1, agent.question_count + 1):
            audio_file = os.path.join(STATIC_AUDIO_DIR, f"{agent.session_id}_q{i}.mp3")
            if os.path.exists(audio_file):
                os.remove(audio_file)
        del sessions[session_id]
        return {"status": "success", "message": "Session ended"}
    raise HTTPException(status_code=404, detail="Session not found")

@app.get("/session/{session_id}/status")
async def get_session_status(session_id: str):
    session = sessions.get(session_id)
    if session:
        agent = session['agent']
        return {
            "status": "active",
            "question_count": agent.question_count,
            "model_used": agent.model_name
        }
    raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Interview System...")
    working_model = test_ollama_models()
    if working_model:
        server = uvicorn.Server(
            uvicorn.Config(app=app, host="0.0.0.0", port=8000)
        )
        try:
            server.run()
        except KeyboardInterrupt:
            print("Shutting down server...")
            asyncio.run(server.shutdown())  # Graceful shutdown
    else:
        print("❌ No working Ollama model found. Check 'ollama serve' and model pull")
