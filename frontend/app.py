"""
🚀 AI Predictive Assistant - Frontend
Structure organisée et professionnelle
"""

import streamlit as st
import requests
import json
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================================
# CONFIGURATION
# ================================

# Configuration de la page
st.set_page_config(
    page_title="AI Predictive Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"

# ================================
# STYLES CSS
# ================================

def load_custom_css():
    """Charge les styles CSS personnalisés"""
    st.markdown("""
    <style>
        /* Variables CSS */
        :root {
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --accent-color: #10b981;
            --danger-color: #ef4444;
            --warning-color: #f59e0b;
            --dark-bg: #0f172a;
            --light-bg: #f8fafc;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
        }
        
        /* Configuration générale */
        .main {
            padding-top: 2rem;
        }
        
        /* Header principal */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.2);
        }
        
        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-align: center;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header p {
            color: rgba(255,255,255,0.9);
            text-align: center;
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
        }
        
        /* Conteneur de chat */
        .chat-container {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            max-height: 500px;
            overflow-y: auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        /* Messages */
        .user-message {
            background: linear-gradient(135deg, var(--secondary-color), #60a5fa);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 20px 20px 5px 20px;
            margin: 1rem 0;
            margin-left: 20%;
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3);
            font-weight: 500;
        }
        
        .bot-message {
            background: linear-gradient(135deg, var(--accent-color), #34d399);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 20px 20px 20px 5px;
            margin: 1rem 0;
            margin-right: 20%;
            box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
            font-weight: 500;
        }
        
        /* Cartes de métriques */
        .metric-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--accent-color);
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        
        /* Status badges */
        .status-success {
            background: var(--accent-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .status-error {
            background: var(--danger-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .status-warning {
            background: var(--warning-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        /* Boutons personnalisés */
        .stButton > button {
            background: linear-gradient(135deg, var(--secondary-color), #60a5fa);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fade-in {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .user-message, .bot-message {
                margin-left: 5%;
                margin-right: 5%;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ================================
# UTILITAIRES API
# ================================

def call_api(endpoint, method="GET", data=None):
    """
    Fonction utilitaire pour appeler l'API - VERSION RAPIDE
    
    Args:
        endpoint (str): Point de terminaison de l'API
        method (str): Méthode HTTP (GET, POST, DELETE)
        data (dict): Données à envoyer
    
    Returns:
        dict: Réponse de l'API ou None en cas d'erreur
    """
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=3)  # Timeout réduit !
        elif method == "POST":
            response = requests.post(url, json=data, timeout=3)  # Timeout réduit !
        elif method == "DELETE":
            response = requests.delete(url, timeout=3)  # Timeout réduit !
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Erreur API: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ **API non démarrée !** Lance d'abord: `python -m src.api`")
        return None
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        return None

def get_api_health():
    """Récupère le statut de santé de l'API"""
    return call_api("/health")

def get_conversation_history():
    """Récupère l'historique de conversation"""
    return call_api("/conversation")

def send_message(message):
    """Envoie un message au chatbot"""
    return call_api("/chat", "POST", {"message": message})

def clear_conversation():
    """Efface l'historique de conversation"""
    return call_api("/conversation", "DELETE")

# ================================
# COMPOSANTS UI
# ================================

def render_header():
    """Affiche l'en-tête principal"""
    st.markdown("""
    <div class="main-header animate-fade-in">
        <h1>🚀 AI Predictive Assistant</h1>
        <p>Machine Learning • Real-time Predictions • Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

def render_api_status():
    """Affiche le statut de l'API"""
    health = get_api_health()
    
    if health:
        if "healthy" in health.get("status", ""):
            st.markdown(f"""
            <div class="status-success">
                ✅ System Operational | Model: {'Ready' if health.get('model_ready') else 'Standby'} | Data: {health.get('data_points', 0)} points
            </div>
            """, unsafe_allow_html=True)
            return True
        else:
            st.markdown('<div class="status-error">❌ System Error</div>', unsafe_allow_html=True)
            return False
    else:
        st.markdown('<div class="status-warning">⚠️ API Connection Required</div>', unsafe_allow_html=True)
        return False

def render_chat_interface():
    """Affiche l'interface de chat"""
    st.markdown("### 💬 Conversation Interface")
    
    # Statut API
    api_status = render_api_status()
    
    # Zone de conversation
    st.markdown("#### 💭 Live Conversation")
    
    conversation = get_conversation_history()
    
    # Conteneur pour les messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if conversation and conversation.get("conversation"):
        for msg in conversation["conversation"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #64748b;">
            <h4>🎯 Ready for your first query!</h4>
            <p>Try: "Predict tomorrow's sales" or "Train a new model"</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return conversation

def render_message_input():
    """Affiche la zone de saisie de message"""
    st.markdown("#### ✍️ Send Message")
    
    user_input = st.text_area(
        "Message:",
        placeholder="Ask me to predict sales, train models, or analyze trends...",
        height=80,
        label_visibility="collapsed"
    )
    
    col_send, col_clear, col_refresh = st.columns(3)
    
    with col_send:
        if st.button("🚀 Send", use_container_width=True):
            if user_input.strip():
                with st.spinner("⚡ Processing..."):  # Message plus court
                    response = send_message(user_input)
                    if response:
                        st.success("✅ Sent!")  # Message plus court
                        st.rerun()
                    else:
                        st.error("❌ Failed")
            else:
                st.warning("⚠️ Enter message")
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            result = clear_conversation()
            if result:
                st.success("✅ Chat cleared!")
                st.rerun()
    
    with col_refresh:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

def render_model_info():
    """Affiche les informations du modèle"""
    model_info = call_api("/model/info")
    
    if model_info and model_info.get("status") == "success":
        info = model_info["model_info"]
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 Model Status</h4>
            <p><strong>Engine:</strong> {info["model_name"]}</p>
            <p><strong>Status:</strong> {'🟢 Ready' if info["is_trained"] else '🟡 Standby'}</p>
            <p><strong>Dataset:</strong> {info.get("data_points", "N/A")} samples</p>
        </div>
        """, unsafe_allow_html=True)
        
        return info
    return None

def render_ml_actions():
    """Affiche les actions ML"""
    st.markdown("#### 🚀 Quick Actions")
    
    # Action d'entraînement
    if st.button("🧠 Train Model", use_container_width=True, key="train"):
        with st.spinner("🤖 Training in progress..."):
            result = call_api("/train", "POST", {})
            if result and result.get("status") == "success":
                train_result = result["training_result"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4>✅ Training Complete!</h4>
                    <p><strong>Score:</strong> {train_result['score']:.1%}</p>
                    <p><strong>Time:</strong> {train_result['training_time']:.1f}s</p>
                    <p><strong>Improvement:</strong> +{train_result['improvement']:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Action de prédiction
    if st.button("🔮 Generate Prediction", use_container_width=True, key="predict"):
        days = st.selectbox("Forecast period:", [1, 3, 7, 14, 30], index=2)
        with st.spinner("🔮 Generating forecast..."):
            result = call_api("/predict", "POST", {"days": days})
            if result and result.get("status") == "success":
                pred = result["prediction"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🎯 Forecast Results</h4>
                    <p><strong>Prediction:</strong> {pred['prediction']:.2f}</p>
                    <p><strong>Confidence:</strong> {pred['confidence']:.1%}</p>
                    <p><strong>Accuracy:</strong> {pred['accuracy']:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Action d'analyse
    if st.button("📊 Data Analysis", use_container_width=True, key="analyze"):
        with st.spinner("📊 Analyzing patterns..."):
            result = call_api("/analyze")
            if result and result.get("status") == "success":
                analysis = result["analysis"]
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📈 Analysis Report</h4>
                    <p><strong>Trend:</strong> {analysis['trend']}</p>
                    <p><strong>Anomalies:</strong> {analysis['anomalies']} detected</p>
                    <p><strong>Data Quality:</strong> {analysis['data_points']} points</p>
                </div>
                """, unsafe_allow_html=True)

def render_session_stats(conversation):
    """Affiche les statistiques de session"""
    st.markdown("#### 📊 Session Stats")
    
    if conversation and conversation.get("conversation"):
        total_msgs = len(conversation["conversation"])
        user_msgs = len([m for m in conversation["conversation"] if m["role"] == "user"])
        bot_msgs = total_msgs - user_msgs
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>💬 Conversation Metrics</h4>
            <p><strong>Total Messages:</strong> {total_msgs}</p>
            <p><strong>Your Messages:</strong> {user_msgs}</p>
            <p><strong>AI Responses:</strong> {bot_msgs}</p>
            <p><strong>Engagement:</strong> {'High' if total_msgs > 10 else 'Growing'}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <h4>🎯 Ready to Start</h4>
            <p>Begin your conversation to see metrics</p>
        </div>
        """, unsafe_allow_html=True)

def render_command_examples():
    """Affiche les exemples de commandes"""
    with st.expander("💡 **Professional Command Examples**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔮 Prediction Queries:**
            - "Forecast tomorrow's revenue"
            - "Predict next week's performance"
            - "What's the trend analysis?"
            
            **🤖 Model Operations:**
            - "Train a new prediction model"
            - "Optimize model parameters"
            - "Update training dataset"
            """)
        
        with col2:
            st.markdown("""
            **📊 Data Analysis:**
            - "Analyze current data patterns"
            - "Show correlation insights"
            - "Detect anomalies in dataset"
            
            **💬 General Assistance:**
            - "Explain your methodology"
            - "How accurate are predictions?"
            - "What data do you use?"
            """)

def render_footer():
    """Affiche le footer"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 10px; margin-top: 2rem;">
        <p style="margin: 0; color: #64748b; font-weight: 500;">
            🚀 <strong>AI Predictive Assistant</strong> | Powered by Advanced ML Algorithms | 
            <span style="color: #10b981;">●</span> Production Ready
        </p>
    </div>
    """, unsafe_allow_html=True)

# ================================
# APPLICATION PRINCIPALE
# ================================

def main():
    """Fonction principale de l'application"""
    
    # Chargement des styles
    load_custom_css()
    
    # En-tête
    render_header()
    
    # Layout principal en colonnes
    col1, col2 = st.columns([2, 1])
    
    # Colonne principale - Chat
    with col1:
        conversation = render_chat_interface()
        render_message_input()
    
    # Colonne latérale - Contrôles
    with col2:
        st.markdown("### 🎛️ ML Control Panel")
        render_model_info()
        st.markdown("---")
        render_ml_actions()
        st.markdown("---")
        render_session_stats(conversation)
    
    # Séparateur
    st.markdown("---")
    
    # Exemples de commandes
    render_command_examples()
    
    # Footer
    render_footer()

# ================================
# POINT D'ENTRÉE
# ================================

if __name__ == "__main__":
    main()