
from pathlib import Path
from dotenv import load_dotenv
import os
# Define base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)
# Application configuration variables
# General settings
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
# Paths and files
DATA_DIR = BASE_DIR / "backend" / "data"
PATIENT_DB = os.getenv("PATIENT_DB", str(DATA_DIR / "patients_data.json"))
REF_PDF = os.getenv("REF_PDF", str(DATA_DIR / "nephrology_refs" / "comprehensive-clinical-nephrology.pdf"))
LOG_FILE = os.getenv("LOG_PATH", str(BASE_DIR / "backend" / "logs" / "chat_memory.json"))
CHROMA_PATH = os.getenv("CHROMA_PATH", str(DATA_DIR / "chroma_db"))
# LLM and embedding model settings
MODEL_RUNTIME = os.getenv("MODEL_RUNTIME", "ollama")  
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", 0.7))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))
# Embedding model settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = 4  
# Server settings
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))

#   Additional settings
DISCLAIMER = os.getenv(
    "DISCLAIMER",
    "This is an AI assistant for educational purposes only. Always consult a healthcare professional."
)
# Web search settings
WEB_SEARCH_PROVIDER = os.getenv("WEB_SEARCH_PROVIDER", "ddgs")

# Ensure necessary directories exist
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
