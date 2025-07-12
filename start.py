import subprocess
import sys
import time
import threading
import webbrowser

def start_api():
    """Lance l'API en arrière-plan"""
    print("🚀 Démarrage de l'API...")
    subprocess.run([sys.executable, "-m", "src.api"])

def start_frontend():
    """Lance le frontend après un délai"""
    print("⏳ Attente de l'API (3 secondes)...")
    time.sleep(3)
    
    print("🎨 Démarrage du frontend...")
    time.sleep(2)
    
    # Ouvre le navigateur
    print("🌐 Ouverture du navigateur...")
    webbrowser.open("http://localhost:8501")
    
    # Lance Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])

def main():
    print("🤖 CHATBOT PRÉDICTIF - DÉMARRAGE COMPLET")
    print("=" * 50)
    
    # Lance l'API en thread séparé
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Lance le frontend
    start_frontend()

if __name__ == "__main__":
    main()