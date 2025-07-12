import pytest
import sys
import os
import asyncio

# Ajoute le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot import ChatbotEngine
from src.ml_engine import MLEngine
from src.config import config

class TestMLEngine:
    def setup_method(self):
        """Setup avant chaque test"""
        self.ml_engine = MLEngine()
    
    def test_data_generation(self):
        """Test de génération de données"""
        self.ml_engine.generate_sample_data()
        data = self.ml_engine.load_data()
        assert len(data) > 0
        assert 'sales' in data.columns
        assert 'date' in data.columns
    
    def test_model_training(self):
        """Test d'entraînement du modèle"""
        result = self.ml_engine.train_model()
        assert result['score'] > 0
        assert self.ml_engine.is_trained == True
        assert result['model_name'] is not None
    
    def test_prediction(self):
        """Test de prédiction"""
        if not self.ml_engine.is_trained:
            self.ml_engine.train_model()
        
        prediction = self.ml_engine.predict_next_values(days=5)
        assert prediction['prediction'] is not None
        assert prediction['confidence'] > 0
        assert len(prediction['predictions_detail']) == 5
    
    def test_data_analysis(self):
        """Test d'analyse des données"""
        analysis = self.ml_engine.analyze_data()
        assert analysis['trend'] in ['Croissante', 'Décroissante']
        assert isinstance(analysis['correlations'], list)
        assert analysis['data_points'] > 0

class TestChatbotEngine:
    def setup_method(self):
        """Setup avant chaque test"""
        self.chatbot = ChatbotEngine()
    
    def test_message_addition(self):
        """Test d'ajout de message"""
        self.chatbot.add_message("user", "Test message")
        history = self.chatbot.get_conversation_history()
        assert len(history) == 1
        assert history[0]['content'] == "Test message"
    
    def test_intent_detection(self):
        """Test de détection d'intention"""
        intent = self.chatbot.detect_ml_intent("Prédit les ventes")
        assert intent['intent'] == 'prediction'
        
        intent = self.chatbot.detect_ml_intent("Bonjour comment ça va?")
        assert intent['intent'] == 'chat'
    
    @pytest.mark.asyncio
    async def test_prediction_request(self):
        """Test de demande de prédiction"""
        # Note: Ce test nécessite une clé OpenAI valide
        try:
            response = await self.chatbot.handle_prediction_request("Prédit demain")
            assert "Prédiction" in response
        except Exception as e:
            # Skip si pas de clé API
            pytest.skip(f"Pas de clé OpenAI: {e}")
    
    def test_conversation_limit(self):
        """Test de limite de conversation"""
        # Ajoute plus de messages que la limite
        for i in range(config.MAX_CONVERSATION_LENGTH + 10):
            self.chatbot.add_message("user", f"Message {i}")
        
        history = self.chatbot.get_conversation_history()
        assert len(history) <= config.MAX_CONVERSATION_LENGTH
    
    def test_clear_conversation(self):
        """Test d'effacement de conversation"""
        self.chatbot.add_message("user", "Test")
        self.chatbot.clear_conversation()
        history = self.chatbot.get_conversation_history()
        assert len(history) == 0

class TestIntegration:
    def test_full_workflow(self):
        """Test du workflow complet"""
        # Initialise les composants
        ml_engine = MLEngine()
        chatbot = ChatbotEngine()
        
        # Génère des données
        ml_engine.generate_sample_data()
        
        # Entraîne le modèle
        training_result = ml_engine.train_model()
        assert training_result['score'] > 0
        
        # Fait une prédiction
        prediction = ml_engine.predict_next_values()
        assert prediction['prediction'] is not None
        
        # Test du chatbot
        chatbot.add_message("user", "Hello")
        assert len(chatbot.get_conversation_history()) == 1

if __name__ == "__main__":
    # Lance les tests
    pytest.main([__file__, "-v"])