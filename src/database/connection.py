"""
Database Connection Manager
Handles MySQL connections with SQLAlchemy
"""

import os
import logging
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector
from mysql.connector import Error
from src.config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

class DatabaseConnection:
    """
    Database connection manager with connection pooling
    """
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize database connection and session factory"""
        try:
            # Database URL for SQLAlchemy
            database_url = (
                f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}"
                f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
                f"?charset=utf8mb4"
            )
            
            # Create engine with connection pooling
            self.engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,  # Validate connections before use
                pool_recycle=300,    # Recycle connections every 5 minutes
                echo=config.DEBUG    # Log SQL queries in debug mode
            )
            
            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logger.info("✅ Database connection established successfully")
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
        except SQLAlchemyError as e:
            logger.error(f"❌ SQLAlchemy connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
            raise
    
    def get_session(self) -> Session:
        """
        Get a new database session
        
        Returns:
            Session: SQLAlchemy session
        """
        if not self.SessionLocal:
            raise Exception("Database not initialized")
        return self.SessionLocal()
    
    def get_engine(self):
        """Get the SQLAlchemy engine"""
        return self.engine
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            bool: True if connection is successful
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("🔌 Database connection closed")

class MySQLDirectConnection:
    """
    Direct MySQL connection for raw SQL operations
    """
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish direct MySQL connection"""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                charset='utf8mb4',
                autocommit=False,
                connection_timeout=10
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                logger.info("✅ Direct MySQL connection established")
                return True
                
        except Error as e:
            logger.error(f"❌ MySQL connection error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """
        Execute SELECT query and return results
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            list: Query results
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
            
        except Error as e:
            logger.error(f"❌ Query execution error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Query error: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE query
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            int: Number of affected rows
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
            
        except Error as e:
            logger.error(f"❌ Update execution error: {e}")
            self.connection.rollback()
            return 0
        except Exception as e:
            logger.error(f"❌ Update error: {e}")
            self.connection.rollback()
            return 0
    
    def execute_many(self, query: str, data_list: list) -> int:
        """
        Execute batch INSERT/UPDATE operations
        
        Args:
            query (str): SQL query with placeholders
            data_list (list): List of parameter tuples
            
        Returns:
            int: Number of affected rows
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.executemany(query, data_list)
            self.connection.commit()
            return self.cursor.rowcount
            
        except Error as e:
            logger.error(f"❌ Batch execution error: {e}")
            self.connection.rollback()
            return 0
        except Exception as e:
            logger.error(f"❌ Batch error: {e}")
            self.connection.rollback()
            return 0
    
    def close(self):
        """Close MySQL connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("🔌 Direct MySQL connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing connection: {e}")

# Global database instances
db_connection = None
mysql_direct = None

def get_db_connection() -> DatabaseConnection:
    """Get global database connection instance"""
    global db_connection
    if db_connection is None:
        db_connection = DatabaseConnection()
    return db_connection

def get_mysql_direct() -> MySQLDirectConnection:
    """Get global direct MySQL connection instance"""
    global mysql_direct
    if mysql_direct is None:
        mysql_direct = MySQLDirectConnection()
    return mysql_direct

def get_db_session() -> Session:
    """
    Get database session (for dependency injection)
    
    Returns:
        Session: SQLAlchemy session
    """
    db = get_db_connection()
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

def init_database():
    """Initialize database connection on startup"""
    try:
        db = get_db_connection()
        if db.test_connection():
            logger.info("🚀 Database initialization successful")
            return True
        else:
            logger.error("❌ Database initialization failed")
            return False
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        return False

def close_database():
    """Close all database connections"""
    global db_connection, mysql_direct
    
    if db_connection:
        db_connection.close_connection()
        db_connection = None
    
    if mysql_direct:
        mysql_direct.close()
        mysql_direct = None
    
    logger.info("🔌 All database connections closed")