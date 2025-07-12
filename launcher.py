#!/usr/bin/env python3
"""
🚀 Launcher pour Chatbot Prédictif
Lance l'API et le frontend automatiquement
"""

import subprocess
import sys
import time
import webbrowser
from threading import Thread

def install_requirements():
    """Installe les dépendances minimales"""
    packages = [
        "fastapi", 
        "uvicorn", 
        "streamlit", 
        "python-dotenv", 
        "requests"
    ]
    
    print("📦 Installation des dépendances...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installé")
        except Exception as e:
            print(f"❌ Erreur avec {package}: {e}")

def start_api():
    """Lance l'API FastAPI"""
    print("🚀 Lancement de l'API...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except Exception as e:
        print(f"❌ Erreur API: {e}")

def start_frontend():
    """Lance le frontend Streamlit"""
    print("🎨 Lancement du frontend...")
    time.sleep(3)  # Attend que l'API démarre
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/app.py", 
            "--server.port", "8501"
        ])
    except Exception as e:
        print(f"❌ Erreur Frontend: {e}")

def main():
    print("🤖 CHATBOT PRÉDICTIF - LAUNCHER")
    print("=" * 40)
    
    # Installation
    install_requirements()
    
    print("\n🚀 Lancement des services...")
    
    # Lance l'API en arrière-plan
    api_thread = Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Attend un peu
    time.sleep(5)
    
    # Ouvre le navigateur
    print("🌐 Ouverture du navigateur...")
    webbrowser.open("http://localhost:8501")
    
    # Lance le frontend
    start_frontend()

if __name__ == "__main__":
    main()