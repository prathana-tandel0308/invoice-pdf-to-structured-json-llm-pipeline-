
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# Local LLM configuration (Ollama)
LOCAL_LLM_PROVIDER = "ollama"
LOCAL_LLM_MODEL = "llama3.2"
OLLAMA_HOST = "http://localhost:11434"


# Cloud LLM configuration (Google Gemini)
CLOUD_LLM_PROVIDER = "gemini"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash"
