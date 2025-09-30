import os
import uuid
import logging
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

STATIC_AUDIO_DIR = "static/audio"
os.makedirs(STATIC_AUDIO_DIR, exist_ok=True)

def test_ollama_models():
    models_to_test = ["llama3.2"]
    
    for model_name in models_to_test:
        try:
            print(f"\n🧪 Testing Ollama model: {model_name}")
            llm = ChatOllama(
                model=model_name,
                temperature=0.7
            )
            response = llm.invoke("Hello! Can you respond with 'Ollama working'?")
            print(f"✅ {model_name} is working! Response: {response.content}")
            return model_name
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)}")
            continue
    
    print("\n❌ None of the models worked. Please check:")
    print("1. Ollama server is running: 'ollama serve'")
    print("2. Model is pulled: 'ollama pull llama3.2'")
    print("3. langchain-ollama is installed: 'pip install langchain-ollama'")
    return None

class InterviewAgent:
    def __init__(self, resume_text: str, model_name: str = None):
        # Auto-detect working model if not specified
        if model_name is None:
            print("🔍 Auto-detecting working Ollama model...")
            model_name = test_ollama_models()
            if model_name is None:
                raise ValueError("No working Ollama model found")
        
        try:
            self.llm = ChatOllama(
                model=model_name,
                temperature=0.7
            )
            print(f"✅ Using Ollama model: {model_name}")
            self.model_name = model_name
        except Exception as e:
            raise ValueError(f"Failed to initialize Ollama model {model_name}: {str(e)}")

        # Initialize TTS engine
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 200)
            self.tts_engine.setProperty('volume', 0.9)
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if "Zira" in voice.name or "David" in voice.name:
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_available = True
            logger.info("✅ TTS engine initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ TTS initialization failed: {str(e)}. Audio responses will be disabled.")
            self.tts_available = False
            self.tts_engine = None

        # Resume context
        self.resume_context = f"Candidate Resume:\n{resume_text}\n\n"
        
        # Conversation history
        self.conversation_history = []
        
        # Updated base prompt with dynamic difficulty, ending, and feedback instructions
        self.base_prompt = """
You are an AI Interviewer conducting a technical interview. 
Act like a friendly, experienced human interviewer, using natural, conversational language. 
You will interview the candidate based on:
1. Their resume (skills, projects, experience).
2. Object-Oriented Programming (OOP) concepts.
3. Software Development Lifecycle (SDLC).

Interview Guidelines:
- Start by asking for a brief self-introduction.
- Ask questions about their resume, projects, and experience.
- Include OOP concepts (inheritance, encapsulation, polymorphism, abstraction).
- Cover SDLC phases (planning, analysis, design, implementation, testing, deployment).
- Ask one question at a time and wait for their answer.
- Use a warm, encouraging tone with phrases like "That's great!" or "Can you tell me more?".
- Provide brief, positive feedback when appropriate.
- Progress from general to specific technical questions.
- If the candidate's answers are detailed, accurate, and show strong understanding, make subsequent questions more advanced or challenging to test deeper knowledge.
- Avoid overly technical jargon unless asking about specific concepts.
- After covering the key areas (resume, OOP, SDLC) sufficiently (aim for 8-12 questions total), conclude the interview by providing comprehensive feedback instead of asking another question.
- In the feedback, highlight strengths, areas for improvement, and specific suggestions on how to improve (e.g., resources, practice areas). Be encouraging and constructive.

Keep responses concise, clear, and human-like, as if speaking aloud.
"""
        
        self.interview_started = False
        self.question_count = 0
        self.session_id = str(uuid.uuid4())

        # New: Separate folder for AI response audio
        self.audio_dir = os.path.join("static", "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

    def text_to_speech(self, text: str) -> str:
        """Convert text to speech and save in static/audio folder"""
        logger.info(f"[TTS] Starting text-to-speech conversion...")
        
        if not self.tts_available or self.tts_engine is None:
            logger.warning("[TTS] TTS not available, skipping audio generation")
            return None
        
        try:
            audio_path = os.path.join(self.audio_dir, f"{self.session_id}_q{self.question_count}.mp3")
            logger.info(f"[TTS] Saving audio to: {audio_path}")
            
            self.tts_engine.save_to_file(text, audio_path)
            
            import threading
            
            def run_tts():
                try:
                    self.tts_engine.runAndWait()
                except Exception as e:
                    logger.error(f"[TTS] Error in runAndWait: {str(e)}")
            
            tts_thread = threading.Thread(target=run_tts, daemon=True)
            tts_thread.start()
            tts_thread.join(timeout=10)
            
            if tts_thread.is_alive():
                logger.error("[TTS] TTS timeout - taking too long!")
                return None
            
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                logger.info(f"[TTS] ✅ Audio file created successfully: {audio_path}")
                return audio_path
            else:
                logger.error(f"[TTS] Audio file not created or empty: {audio_path}")
                return None
                
        except Exception as e:
            logger.error(f"[TTS] ❌ TTS Error: {str(e)}", exc_info=True)
            return None

    def interview_turn(self, user_input: str = None) -> tuple:
        """Main interview logic"""
        logger.info(f"[AGENT] interview_turn called. Started: {self.interview_started}, Input: {user_input[:50] if user_input else 'None'}...")
        
        try:
            if not self.interview_started:
                # First turn
                self.interview_started = True
                prompt = f"{self.resume_context}\n{self.base_prompt}\n\nStart the interview by asking the candidate for a brief self-introduction."
                response = self.llm.invoke(prompt)
                self.conversation_history.append(("assistant", response.content))
                self.question_count += 1
                audio_path = self.text_to_speech(response.content)
                return response.content, audio_path
                
            else:
                # Subsequent turns
                if user_input is None:
                    raise ValueError("User input is required for continuing the interview")
                
                context = f"{self.resume_context}\n{self.base_prompt}\n\n"
                context += f"This is question #{self.question_count + 1} of the interview.\n\n"
                context += "Recent conversation:\n"
                for role, message in self.conversation_history[-6:]:
                    context += f"{role}: {message}\n"
                context += f"human: {user_input}\n\n"
                context += "Based on the candidate's response and the interview progress, either: 1) provide brief feedback and ask the next appropriate (and potentially harder) interview question, or 2) if the interview is complete after covering all key areas, provide comprehensive feedback on the candidate's performance (strengths, improvements, suggestions) and end the interview without asking another question.\n\nassistant:"
                
                response = self.llm.invoke(context)
                self.conversation_history.append(("human", user_input))
                self.conversation_history.append(("assistant", response.content))
                self.question_count += 1
                audio_path = self.text_to_speech(response.content)
                return response.content, audio_path
                
        except Exception as e:
            logger.error(f"[AGENT] ❌ Error in interview_turn: {str(e)}", exc_info=True)
            error_msg = f"I apologize, but I encountered an error. Could you please repeat your last response?"
            return error_msg, None