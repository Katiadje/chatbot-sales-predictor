"""
Migration Simple - Sans dépendances complexes
"""

import mysql.connector
from mysql.connector import Error
import random
import math
from datetime import datetime, date, timedelta

def create_tables():
    """Crée toutes les tables nécessaires"""
    
    connection = None
    cursor = None
    
    try:
        # Connexion à MySQL
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='chatbot_predictive',
            user='root',
            password=''
        )
        
        cursor = connection.cursor()
        
        print("🔨 Création des tables...")
        
        # Table sales_data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                sales_amount DECIMAL(10,2) NOT NULL,
                quantity INTEGER NOT NULL,
                product_category VARCHAR(100),
                region VARCHAR(50),
                day_of_week INT,
                month INT,
                is_weekend BOOLEAN DEFAULT FALSE,
                temperature DECIMAL(5,2),
                marketing_spend DECIMAL(8,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                INDEX idx_date (date),
                INDEX idx_category (product_category),
                INDEX idx_region (region)
            )
        """)
        
        # Table ml_models
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ml_models (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                version VARCHAR(20) NOT NULL,
                algorithm VARCHAR(50) NOT NULL,
                performance_score DECIMAL(5,4),
                training_date TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                hyperparameters JSON,
                feature_columns JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                UNIQUE KEY unique_model_version (name, version),
                INDEX idx_active (is_active)
            )
        """)
        
        # Table predictions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                model_id INT,
                prediction_date DATE NOT NULL,
                target_date DATE NOT NULL,
                predicted_value DECIMAL(10,2) NOT NULL,
                confidence_score DECIMAL(5,4) DEFAULT 0.95,
                actual_value DECIMAL(10,2) NULL,
                accuracy_error DECIMAL(8,4) NULL,
                feature_values JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (model_id) REFERENCES ml_models(id),
                INDEX idx_model_date (model_id, target_date),
                INDEX idx_prediction_date (prediction_date)
            )
        """)
        
        # Table conversations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(100) NOT NULL,
                message_type ENUM('user', 'assistant') NOT NULL,
                message_content TEXT NOT NULL,
                intent_detected VARCHAR(100),
                confidence_score DECIMAL(5,4),
                processing_time_ms INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                INDEX idx_session (session_id),
                INDEX idx_type (message_type),
                INDEX idx_intent (intent_detected)
            )
        """)
        
        # Table business_metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_metrics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                metric_name VARCHAR(100) NOT NULL,
                metric_value DECIMAL(15,6) NOT NULL,
                metric_date DATE NOT NULL,
                category ENUM('sales', 'marketing', 'ml', 'system') NOT NULL,
                target_value DECIMAL(15,6),
                variance_percentage DECIMAL(8,4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                INDEX idx_metric_date (metric_name, metric_date),
                INDEX idx_category (category)
            )
        """)
        
        connection.commit()
        print("✅ Toutes les tables créées avec succès !")
        
        return True
        
    except Error as e:
        print(f"❌ Erreur MySQL : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def generate_sample_data():
    """Génère des données d'exemple"""
    
    connection = None
    cursor = None
    
    try:
        # Connexion à MySQL
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='chatbot_predictive',
            user='root',
            password=''
        )
        
        cursor = connection.cursor()
        
        print("📊 Génération des données d'exemple...")
        
        # Vérifier si des données existent déjà
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        existing_sales = cursor.fetchone()[0]
        
        if existing_sales > 0:
            print(f"Données existantes trouvées ({existing_sales} records), skip génération")
            return True
        
        # 1. Créer un modèle ML
        cursor.execute("""
            INSERT INTO ml_models (name, version, algorithm, performance_score, hyperparameters, feature_columns)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            'SalesPredictor',
            'v1.0', 
            'RandomForest',
            0.8950,
            '{"n_estimators": 100, "max_depth": 10, "random_state": 42}',
            '["day_of_week", "month", "is_weekend", "temperature", "marketing_spend"]'
        ))
        
        model_id = cursor.lastrowid
        
        # 2. Générer des données de vente (365 jours)
        print("Génération des données de vente...")
        
        sales_data = []
        current_date = date.today() - timedelta(days=365)
        base_sales = 150.0
        
        product_categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        for i in range(365):
            # Calcul des ventes réalistes
            trend_factor = i * 0.05
            seasonal_factor = 30 * math.sin(2 * math.pi * i / 365.25)
            weekly_factor = 15 * math.sin(2 * math.pi * i / 7)
            noise_factor = random.uniform(-25, 25)
            
            daily_sales = max(50, base_sales + trend_factor + seasonal_factor + weekly_factor + noise_factor)
            
            # Générer plusieurs transactions par jour
            num_transactions = random.randint(5, 15)
            
            for _ in range(num_transactions):
                transaction_amount = daily_sales / num_transactions * random.uniform(0.5, 2.0)
                quantity = random.randint(1, 8)
                
                day_of_week = current_date.weekday()
                is_weekend = day_of_week >= 5
                
                # Température saisonnière
                base_temp = 15 + 10 * math.sin(2 * math.pi * i / 365.25)
                temperature = base_temp + random.uniform(-5, 5)
                
                # Marketing spend
                base_marketing = 200
                weekend_boost = 100 if is_weekend else 0
                marketing_spend = base_marketing + weekend_boost + random.uniform(-50, 100)
                
                sales_data.append((
                    current_date,
                    round(transaction_amount, 2),
                    quantity,
                    random.choice(product_categories),
                    random.choice(regions),
                    day_of_week,
                    current_date.month,
                    is_weekend,
                    round(temperature, 2),
                    round(marketing_spend, 2)
                ))
            
            current_date += timedelta(days=1)
        
        # Insertion par batch
        cursor.executemany("""
            INSERT INTO sales_data 
            (date, sales_amount, quantity, product_category, region, day_of_week, month, is_weekend, temperature, marketing_spend)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, sales_data)
        
        print(f"✅ {len(sales_data)} enregistrements de vente créés")
        
        # 3. Générer quelques prédictions
        print("Génération des prédictions...")
        
        predictions_data = []
        for i in range(30):  # 30 derniers jours
            prediction_date = date.today() - timedelta(days=30-i)
            target_date = prediction_date + timedelta(days=1)
            
            # Prédiction réaliste
            base_prediction = 150 + (i * 0.5)
            seasonal_factor = 20 * math.sin(2 * math.pi * i / 365)
            noise = random.uniform(-15, 15)
            predicted_value = max(50, base_prediction + seasonal_factor + noise)
            
            confidence_score = random.uniform(0.85, 0.95)
            
            # Valeur réelle (pour les prédictions passées)
            if target_date < date.today():
                error_percentage = random.uniform(-10, 10)
                actual_value = predicted_value * (1 + error_percentage/100)
            else:
                actual_value = None
            
            predictions_data.append((
                model_id,
                prediction_date,
                target_date,
                round(predicted_value, 2),
                round(confidence_score, 4),
                round(actual_value, 2) if actual_value else None,
                f'{{"day_of_week": {target_date.weekday()}, "month": {target_date.month}}}'
            ))
        
        cursor.executemany("""
            INSERT INTO predictions 
            (model_id, prediction_date, target_date, predicted_value, confidence_score, actual_value, feature_values)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, predictions_data)
        
        print(f"✅ {len(predictions_data)} prédictions créées")
        
        # 4. Générer quelques conversations
        print("Génération des conversations...")
        
        sample_conversations = [
            ("user", "Hello! How are you?", "greeting"),
            ("assistant", "Hello! I'm your AI-powered predictive assistant! How can I help you today?", None),
            ("user", "Predict tomorrow's sales", "prediction"), 
            ("assistant", "🔮 Prediction Generated Successfully! Average Forecast: 156.23, Confidence Level: 94.2%", None),
            ("user", "Train a new model", "training"),
            ("assistant", "🤖 Model Training Completed Successfully! Performance Score: 91.8%", None),
            ("user", "Analyze current trends", "analysis"),
            ("assistant", "📈 Analysis Complete. Overall Trend: Increasing, Strong Correlations detected.", None)
        ]
        
        session_id = f"demo_session_{datetime.now().strftime('%Y%m%d')}"
        conversations_data = []
        
        for i, (msg_type, content, intent) in enumerate(sample_conversations):
            conversations_data.append((
                session_id,
                msg_type,
                content,
                intent,
                random.uniform(0.85, 0.95) if intent else None,
                random.randint(100, 2000) if msg_type == "assistant" else random.randint(50, 200)
            ))
        
        cursor.executemany("""
            INSERT INTO conversations 
            (session_id, message_type, message_content, intent_detected, confidence_score, processing_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, conversations_data)
        
        print(f"✅ {len(conversations_data)} messages de conversation créés")
        
        connection.commit()
        print("🎉 Génération des données terminée avec succès !")
        
        return True
        
    except Error as e:
        print(f"❌ Erreur MySQL : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def main():
    """Fonction principale"""
    print("🚀 Initialisation de la base de données...")
    
    # Étape 1: Créer les tables
    if not create_tables():
        print("❌ Échec de la création des tables")
        return False
    
    # Étape 2: Générer les données d'exemple
    if not generate_sample_data():
        print("❌ Échec de la génération des données")
        return False
    
    print("✅ Initialisation complète réussie !")
    return True

if __name__ == "__main__":
    main()