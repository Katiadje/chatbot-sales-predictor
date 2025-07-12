from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot import ChatbotEngine
from src.ml_engine import MLEngine
from src.config import config

app = FastAPI(
    title="Chatbot Prédictif API",
    description="API pour chatbot avec ML temps réel",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance globale du chatbot
chatbot = ChatbotEngine()
ml_engine = MLEngine()

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🤖 Chatbot Prédictif API",
        "version": "1.0.0",
        "status": "✅ running",
        "mode": "🆓 GRATUIT",
        "endpoints": {
            "chat": "/chat",
            "predict": "/predict", 
            "train": "/train",
            "analyze": "/analyze",
            "health": "/health"
        }
    }

@app.post("/chat")
async def chat_endpoint(data: dict):
    """Endpoint principal pour le chat - VERSION RAPIDE"""
    try:
        message = data.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message requis")
        
        # Pas de délai artificiel - réponse immédiate !
        response = await chatbot.process_message(message)
        return {
            "response": response,
            "conversation_id": "default",
            "processing_time": "⚡ Instant"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de chat: {str(e)}")

@app.get("/conversation")
async def get_conversation():
    """Récupère l'historique de conversation"""
    try:
        history = chatbot.get_conversation_history()
        return {"conversation": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.delete("/conversation")
async def clear_conversation():
    """Efface l'historique de conversation"""
    try:
        chatbot.clear_conversation()
        return {"message": "✅ Conversation effacée"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/predict")
async def predict_endpoint(data: dict = None):
    """Endpoint pour les prédictions"""
    try:
        days = 7
        if data:
            days = data.get("days", 7)
            
        prediction = ml_engine.predict_next_values(days)
        return {
            "status": "success",
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@app.post("/train")
async def train_endpoint(data: dict = None):
    """Endpoint pour l'entraînement"""
    try:
        result = ml_engine.train_model()
        return {
            "status": "success",
            "training_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'entraînement: {str(e)}")

@app.get("/analyze")
async def analyze_endpoint():
    """Endpoint pour l'analyse des données"""
    try:
        analysis = ml_engine.analyze_data()
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Informations sur le modèle"""
    try:
        info = ml_engine.get_model_info()
        return {
            "status": "success",
            "model_info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    try:
        model_info = ml_engine.get_model_info()
        return {
            "status": "🟢 healthy",
            "api_version": "1.0.0",
            "mode": "🆓 FREE",
            "model_ready": model_info["is_trained"],
            "data_points": model_info.get("data_points", 0),
            "message": "API fonctionnelle en mode gratuit !"
        }
    except Exception as e:
        return {
            "status": "🔴 unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    print("🚀 Lancement de l'API Chatbot Prédictif...")
    print("📍 URL: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🆓 Mode: GRATUIT")
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )