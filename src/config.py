import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Mode gratuit - pas besoin de clé OpenAI !
    SIMULATION_MODE = True  # 🆓 MODE GRATUIT
    OPENAI_API_KEY = "simulation_mode"  # Fake key pour éviter les erreurs
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # ML Config
    MODEL_SAVE_PATH = "data/models/"
    DATA_PATH = "data/"
    MAX_TRAINING_TIME = 300  # 5 minutes
    
    # Chat Config
    MAX_CONVERSATION_LENGTH = 50
    SYSTEM_PROMPT = """Tu es un assistant IA spécialisé dans les prédictions temps réel.
    Tu peux analyser des données, entraîner des modèles et faire des prédictions.
    Réponds de manière concise et technique."""

config = Config()