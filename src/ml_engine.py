import random
import os
import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List
from src.config import config

class MLEngine:
    def __init__(self):
        self.model_name = "SimulatedML_v1"
        self.is_trained = False
        self.last_training_time = None
        self.model_data = {}
        
        # Simule des données d'entraînement
        self.historical_data = self.generate_sample_data()
        
    def generate_sample_data(self):
        """Génère des données d'exemple simulées"""
        print("🔄 Génération des données d'exemple...")
        
        # Génère 365 jours de données fictives
        data = []
        base_value = 100
        
        for i in range(365):
            # Tendance + saisonnalité + bruit
            trend = i * 0.1
            seasonal = 20 * math.sin(2 * math.pi * i / 365)
            noise = random.uniform(-10, 10)
            
            value = base_value + trend + seasonal + noise
            
            data.append({
                'day': i,
                'value': max(0, value),  # Pas de valeurs négatives
                'day_of_week': i % 7,
                'month': ((i // 30) % 12) + 1,
                'is_weekend': 1 if (i % 7) in [5, 6] else 0
            })
        
        print("✅ Données générées (365 jours)")
        return data
    
    def train_model(self) -> Dict[str, Any]:
        """Simule l'entraînement d'un modèle"""
        start_time = datetime.now()
        print("🤖 Entraînement du modèle simulé...")
        
        # Simule un délai d'entraînement - VERSION RAPIDE
        import time
        time.sleep(random.uniform(0.2, 0.8))  # Beaucoup plus rapide !
        
        # Calcule des "métriques" simulées
        self.model_data = {
            'mean_value': sum(d['value'] for d in self.historical_data) / len(self.historical_data),
            'trend_slope': random.uniform(0.05, 0.15),
            'seasonal_amplitude': random.uniform(15, 25),
            'noise_level': random.uniform(5, 15)
        }
        
        self.is_trained = True
        self.last_training_time = datetime.now()
        training_time = (datetime.now() - start_time).total_seconds()
        
        score = random.uniform(0.85, 0.95)  # Score simulé
        
        print(f"✅ Modèle simulé entraîné ! Score: {score:.3f}")
        
        return {
            "model_name": self.model_name,
            "score": score,
            "mae": random.uniform(8, 15),
            "training_time": training_time,
            "improvement": random.uniform(0.02, 0.08)
        }
    
    def predict_next_values(self, n_days: int = 7) -> Dict[str, Any]:
        """Simule des prédictions"""
        if not self.is_trained:
            self.train_model()
        
        print(f"🔮 Prédiction simulée des {n_days} prochains jours...")
        
        # Simule des prédictions basées sur les données historiques
        last_value = self.historical_data[-1]['value']
        predictions = []
        
        for i in range(n_days):
            # Prédiction simulée avec tendance et variation
            trend = self.model_data['trend_slope'] * i
            variation = random.uniform(-5, 5)
            predicted_value = last_value + trend + variation
            predictions.append(max(0, predicted_value))
        
        avg_prediction = sum(predictions) / len(predictions)
        confidence = random.uniform(0.85, 0.95)
        
        return {
            "prediction": avg_prediction,
            "predictions_detail": predictions,
            "confidence": confidence,
            "model_name": self.model_name,
            "accuracy": random.uniform(0.92, 0.98),
            "mae": random.uniform(5, 12),
            "dates": [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, n_days+1)]
        }
    
    def analyze_data(self) -> Dict[str, Any]:
        """Simule l'analyse des données"""
        print("📊 Analyse simulée des données...")
        
        # Calcule des statistiques réelles sur les données simulées
        values = [d['value'] for d in self.historical_data]
        recent_values = values[-30:]  # 30 derniers jours
        
        # Tendance
        if recent_values[-1] > recent_values[0]:
            trend = "Increasing"
        else:
            trend = "Decreasing"
        
        # Corrélations simulées
        correlations = [
            "day_of_week (0.45)",
            "month (0.38)",
            "is_weekend (0.32)"
        ]
        
        # Anomalies simulées
        anomalies = random.randint(2, 8)
        
        # Insights
        avg_value = sum(values) / len(values)
        max_value = max(values)
        min_value = min(values)
        
        insights = f"""
        • Average value: {avg_value:.1f}
        • Peak maximum: {max_value:.1f}
        • Minimum value: {min_value:.1f}
        • Volatility: {'High' if (max_value - min_value) > 50 else 'Moderate'}
        • Seasonal pattern detected with amplitude ~{self.model_data.get('seasonal_amplitude', 20):.1f}
        """
        
        return {
            "trend": trend,
            "correlations": correlations,
            "anomalies": anomalies,
            "insights": insights.strip(),
            "data_points": len(self.historical_data),
            "date_range": f"365 simulated days"
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les infos du modèle"""
        return {
            "model_name": self.model_name,
            "is_trained": self.is_trained,
            "last_training": self.last_training_time.isoformat() if self.last_training_time else None,
            "model_exists": self.is_trained,
            "data_points": len(self.historical_data)
        }