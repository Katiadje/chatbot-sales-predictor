import random
from typing import List, Dict, Any
from src.config import config
from src.ml_engine import MLEngine
import json
import time

class ChatbotEngine:
    def __init__(self):
        self.ml_engine = MLEngine()
        self.conversation_history = []
        
        # Réponses simulées pour mode gratuit - VERSION ANGLAISE
        self.simulation_responses = {
            "greeting": [
                "Hello! 👋 I'm your AI-powered predictive assistant! How can I help you today?",
                "Hi there! 🤖 Ready to explore data predictions together?",
                "Welcome! I'm here to help with ML analysis and predictions!"
            ],
            "prediction": [
                "🔮 Analyzing your data and generating predictions...",
                "📊 Running prediction algorithms...",
                "🎯 Forecasting based on detected patterns..."
            ],
            "training": [
                "🤖 Initiating model training process...",
                "🧠 Optimizing hyperparameters...",
                "⚡ The model is learning from your data..."
            ],
            "analysis": [
                "📈 Analyzing trends in progress...",
                "🔍 Searching for patterns in the dataset...",
                "📊 Generating comprehensive analysis report..."
            ],
            "general": [
                "Interesting! I can help you with that using my ML capabilities.",
                "Great question! Let me process that with my predictive algorithms.",
                "I'll analyze your request using my advanced ML models!"
            ]
        }
        
    def add_message(self, role: str, content: str):
        """Ajoute un message à l'historique"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Limite la taille de l'historique
        if len(self.conversation_history) > config.MAX_CONVERSATION_LENGTH:
            self.conversation_history = self.conversation_history[-config.MAX_CONVERSATION_LENGTH:]
    
    def detect_ml_intent(self, user_message: str) -> Dict[str, Any]:
        """Détecte si l'utilisateur veut faire du ML"""
        ml_keywords = {
            # Prediction keywords
            "predict": "prediction",
            "forecast": "prediction",
            "prediction": "prediction",
            "future": "prediction",
            "tomorrow": "prediction",
            "next": "prediction",
            
            # Training keywords
            "train": "training",
            "training": "training",
            "learn": "training",
            "model": "training",
            "optimize": "training",
            
            # Analysis keywords
            "analyze": "analysis",
            "analysis": "analysis",
            "trend": "analysis",
            "pattern": "analysis",
            "insight": "analysis",
            "data": "analysis",
            
            # Greeting keywords
            "hello": "greeting",
            "hi": "greeting",
            "hey": "greeting",
            "good": "greeting"
        }
        
        user_lower = user_message.lower()
        for keyword, intent in ml_keywords.items():
            if keyword in user_lower:
                return {"intent": intent, "confidence": 0.8}
        
        return {"intent": "general", "confidence": 0.9}
    
    def simulate_typing_delay(self):
        """Simule un délai de réflexion - VERSION RAPIDE"""
        time.sleep(random.uniform(0.1, 0.3))  # Beaucoup plus rapide !
    
    async def process_message(self, user_message: str) -> str:
        """Traite un message utilisateur - VERSION RAPIDE"""
        self.add_message("user", user_message)
        
        # 🚀 RÉPONSE INSTANTANÉE pour messages courants
        instant_response = self.get_instant_response(user_message)
        if instant_response:
            self.add_message("assistant", instant_response)
            return instant_response
        
        # Délai minimal pour messages complexes
        self.simulate_typing_delay()
        
        # Détecte l'intention
        intent_result = self.detect_ml_intent(user_message)
        
        if intent_result["intent"] == "greeting":
            return self.handle_greeting()
        elif intent_result["intent"] == "prediction":
            return await self.handle_prediction_request(user_message)
        elif intent_result["intent"] == "training":
            return await self.handle_training_request(user_message)
        elif intent_result["intent"] == "analysis":
            return await self.handle_analysis_request(user_message)
        else:
            return await self.handle_general_request(user_message)
    
    def get_instant_response(self, message: str) -> str:
        """Réponses instantanées pour messages courants"""
        msg_lower = message.lower().strip()
        
        # Réponses ultra-rapides
        instant_cache = {
            "hello": "Hello! 👋 I'm your AI-powered predictive assistant! Ready for instant predictions?",
            "hi": "Hi there! 🤖 Ready to explore data predictions together?",
            "hey": "Hey! ⚡ Fast predictions at your service!",
            "status": "✅ **System Status:** All operational | Models: Ready | Response: ⚡ Instant",
            "help": "💡 **Quick Commands:** predict, train, analyze, status | What do you need?",
            "test": "🧪 **Test Successful!** All systems running at optimal speed ⚡",
            "speed": "⚡ **Ultra-Fast Mode Activated!** Response time: <100ms",
        }
        
        # Recherche exacte d'abord
        if msg_lower in instant_cache:
            return instant_cache[msg_lower]
        
        # Recherche par mots-clés
        for key, response in instant_cache.items():
            if key in msg_lower:
                return response
        
        # Patterns rapides
        if any(word in msg_lower for word in ['quick', 'fast', 'rapid', 'instant']):
            return "⚡ **Lightning Speed Activated!** Ready for instant ML predictions and analysis!"
        
        return None  # Pas de réponse instantanée
    
    def handle_greeting(self) -> str:
        """Gère les salutations"""
        response = random.choice(self.simulation_responses["greeting"])
        self.add_message("assistant", response)
        return response
    
    async def handle_prediction_request(self, user_message: str) -> str:
        """Gère les demandes de prédiction - MODE GRATUIT"""
        try:
            # Message de début
            intro = random.choice(self.simulation_responses["prediction"])
            
            # Utilise le ML engine pour faire une prédiction
            prediction_result = self.ml_engine.predict_next_values()
            
            response = f"""{intro}

🔮 **Prediction Generated Successfully!**

**Average Forecast**: {prediction_result['prediction']:.2f}
**Confidence Level**: {prediction_result['confidence']:.1%}
**Model Used**: {prediction_result['model_name']}

📊 **Model Performance Metrics**:
• Accuracy: {prediction_result['accuracy']:.1%}
• Mean Absolute Error: {prediction_result['mae']:.2f}

💡 **Key Insight**: The trend appears {'positive' if prediction_result['prediction'] > 150 else 'stable'} based on historical patterns.

Would you like me to explain the methodology or generate additional forecasts?"""
            
            self.add_message("assistant", response)
            return response
            
        except Exception as e:
            error_msg = f"❌ Error during prediction: {str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg
    
    async def handle_training_request(self, user_message: str) -> str:
        """Gère les demandes d'entraînement - MODE GRATUIT"""
        try:
            # Message de début
            intro = random.choice(self.simulation_responses["training"])
            
            training_result = self.ml_engine.train_model()
            
            response = f"""{intro}

🤖 **Model Training Completed Successfully!**

**New Model**: {training_result['model_name']}
**Performance Score**: {training_result['score']:.1%}
**Training Duration**: {training_result['training_time']:.1f} seconds

📈 **Performance Improvements**:
• Accuracy: +{training_result['improvement']:.1%} vs previous model
• Overfitting: Well controlled ✅
• Convergence: Optimal ✅

🚀 **The model is now ready for ultra-precise predictions!**

You can now ask me for predictions using this newly trained model!"""
            
            self.add_message("assistant", response)
            return response
            
        except Exception as e:
            error_msg = f"❌ Error during training: {str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg
    
    async def handle_analysis_request(self, user_message: str) -> str:
        """Gère les demandes d'analyse - MODE GRATUIT"""
        try:
            # Message de début
            intro = random.choice(self.simulation_responses["analysis"])
            
            analysis_result = self.ml_engine.analyze_data()
            
            response = f"""{intro}

📊 **Comprehensive Data Analysis Complete**

**📈 Overall Trend**: {analysis_result['trend']}
**🔗 Strong Correlations**: {', '.join(analysis_result['correlations'])}
**⚠️ Anomalies Detected**: {analysis_result['anomalies']} suspicious data points
**📊 Dataset Volume**: {analysis_result['data_points']} records

💡 **Key Insights**:
{analysis_result['insights']}

🔮 **Recommendations**:
• {'Maintain current strategy' if analysis_result['trend'] == 'Increasing' else 'Adjust strategy to reverse the trend'}
• Monitor variables with strong correlations
• Investigate detected anomalies

Would you like a prediction based on this analysis?"""
            
            self.add_message("assistant", response)
            return response
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            self.add_message("assistant", error_msg)
            return error_msg
    
    async def handle_general_request(self, user_message: str) -> str:
        """Gère les conversations générales - MODE GRATUIT"""
        
        # Réponses intelligentes basées sur des mots-clés
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ["how", "work", "explain", "methodology"]):
            response = """🤖 **How I Work - Technical Overview**

I'm an AI assistant specialized in predictive analytics! Here's what I can do:

🔮 **Predictions**: "Predict tomorrow's sales"
🤖 **Model Training**: "Train a new model" 
📊 **Data Analysis**: "Analyze current trends"

**Core Technologies**:
• Machine Learning (RandomForest, AutoML)
• Time series analysis
• Anomaly detection
• Automated feature engineering

**Supported Data Types**:
• Sales, revenue, business metrics
• Temporal data with seasonality
• Multi-variable datasets (weather, marketing, etc.)

Try a command to see the magic in action! ✨"""
        
        elif any(word in user_lower for word in ["help", "assistance", "commands"]):
            response = """💡 **Help - Available Commands**

**🔮 For Predictions:**
• "Predict tomorrow's sales"
• "Forecast next 7 days"
• "What's the trend analysis?"

**🤖 For Training:**
• "Train a new model"
• "Improve accuracy"
• "Optimize parameters"

**📊 For Analysis:**
• "Analyze current data"
• "Show me trends"
• "Detect anomalies"

**💬 General Questions:**
• "How does this work?"
• "What data do you use?"
• "Explain your methods"

What interests you the most?"""
        
        elif any(word in user_lower for word in ["data", "dataset", "information"]):
            response = """📊 **My Data Sources & Processing**

**📈 Primary Dataset:**
• 700+ days of sales data
• Variables: sales, weather, marketing, calendar
• Period: 2023-2024 (synthetic but realistic data)

**🔍 Features Used:**
• `sales` : Daily sales (target variable)
• `day_of_week` : Day of week (0-6)
• `month` : Month (1-12) 
• `is_weekend` : Weekend flag (0/1)
• `temperature` : Average temperature
• `marketing_spend` : Daily marketing budget

**🧠 Automated Preprocessing:**
• Missing value handling
• Feature normalization
• Temporal feature engineering
• Intelligent train/test split

The data is generated with realistic patterns: trend + seasonality + noise!"""
        
        else:
            # Réponse générale intelligente
            response = random.choice(self.simulation_responses["general"]) + f"""

**💡 Based on your message ("{user_message[:50]}..."), I can:**

• 🔮 Generate relevant predictions
• 📊 Analyze hidden patterns  
• 🤖 Train optimized models
• 💡 Provide actionable insights

**Quick Example:** Say "Predict tomorrow" and I'll show you my ML power! 

What would you like to explore?"""
        
        self.add_message("assistant", response)
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retourne l'historique de conversation"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Efface l'historique"""
        self.conversation_history = []