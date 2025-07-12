"""
Test simple de connexion MySQL
"""

import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    """Test basique de connexion MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='chatbot_predictive',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            print("✅ Connexion MySQL réussie !")
            
            cursor = connection.cursor()
            
            # Test création d'une table simple
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    value DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Test insertion
            cursor.execute("""
                INSERT INTO test_table (name, value) 
                VALUES ('test_record', 123.45)
            """)
            
            connection.commit()
            
            # Test lecture
            cursor.execute("SELECT * FROM test_table LIMIT 1")
            result = cursor.fetchone()
            
            print(f"✅ Test d'insertion/lecture réussi : {result}")
            
            # Nettoyage
            cursor.execute("DROP TABLE test_table")
            connection.commit()
            
            cursor.close()
            connection.close()
            
            print("✅ Test MySQL complet réussi !")
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()