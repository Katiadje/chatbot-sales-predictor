-- ================================
-- AI CHATBOT PREDICTIVE SYSTEM
-- MySQL Database Schema (GRATUIT)
-- ================================

CREATE DATABASE IF NOT EXISTS chatbot_predictive;
USE chatbot_predictive;

-- ================================
-- SALES DATA TABLE
-- ================================
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
);

-- ================================
-- ML MODELS TABLE
-- ================================
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
);

-- ================================
-- PREDICTIONS TABLE
-- ================================
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
);

-- ================================
-- CHAT CONVERSATIONS TABLE
-- ================================
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
);

-- ================================
-- DATA QUALITY MONITORING
-- ================================
CREATE TABLE IF NOT EXISTS data_quality (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    check_result ENUM('passed', 'failed', 'warning') NOT NULL,
    message TEXT,
    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_table_result (table_name, check_result),
    INDEX idx_check_date (check_date)
);

-- ================================
-- BUSINESS METRICS TABLE
-- ================================
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
);

-- ================================
-- VIEWS FOR ANALYTICS
-- ================================

-- Daily Sales Summary View
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    date,
    SUM(sales_amount) as total_sales,
    SUM(quantity) as total_quantity,
    AVG(sales_amount) as avg_sales,
    COUNT(*) as transaction_count,
    AVG(temperature) as avg_temperature,
    SUM(marketing_spend) as total_marketing_spend
FROM sales_data 
GROUP BY date
ORDER BY date;

-- Model Performance View
CREATE OR REPLACE VIEW model_performance AS
SELECT 
    m.id,
    m.name,
    m.version,
    m.algorithm,
    m.performance_score,
    COUNT(p.id) as prediction_count,
    AVG(p.confidence_score) as avg_confidence,
    AVG(ABS(p.accuracy_error)) as avg_error,
    m.created_at
FROM ml_models m
LEFT JOIN predictions p ON m.id = p.model_id
WHERE m.is_active = TRUE
GROUP BY m.id, m.name, m.version, m.algorithm, m.performance_score, m.created_at;

-- Recent Conversations View
CREATE OR REPLACE VIEW recent_conversations AS
SELECT 
    session_id,
    COUNT(*) as message_count,
    MAX(created_at) as last_message_time,
    COUNT(CASE WHEN message_type = 'user' THEN 1 END) as user_messages,
    COUNT(CASE WHEN message_type = 'assistant' THEN 1 END) as bot_messages,
    AVG(processing_time_ms) as avg_processing_time
FROM conversations 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY session_id
ORDER BY last_message_time DESC;

-- ================================
-- STORED PROCEDURES
-- ================================

DELIMITER //

-- Generate Sample Sales Data
CREATE PROCEDURE IF NOT EXISTS GenerateSampleSalesData(IN days_count INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE current_date DATE DEFAULT DATE_SUB(CURDATE(), INTERVAL days_count DAY);
    DECLARE base_sales DECIMAL(10,2) DEFAULT 100;
    DECLARE seasonal_factor DECIMAL(5,4);
    DECLARE trend_factor DECIMAL(5,4);
    DECLARE noise_factor DECIMAL(5,4);
    DECLARE final_sales DECIMAL(10,2);
    
    WHILE i < days_count DO
        -- Calculate seasonal factor (sine wave)
        SET seasonal_factor = 20 * SIN(2 * PI() * i / 365);
        
        -- Calculate trend factor (gradual increase)
        SET trend_factor = i * 0.1;
        
        -- Add random noise
        SET noise_factor = (RAND() - 0.5) * 20;
        
        -- Calculate final sales amount
        SET final_sales = base_sales + seasonal_factor + trend_factor + noise_factor;
        SET final_sales = GREATEST(final_sales, 10); -- Minimum sales
        
        INSERT INTO sales_data (
            date, 
            sales_amount, 
            quantity, 
            product_category,
            region,
            day_of_week,
            month,
            is_weekend,
            temperature,
            marketing_spend
        ) VALUES (
            current_date,
            final_sales,
            FLOOR(RAND() * 50) + 1,
            ELT(FLOOR(RAND() * 5) + 1, 'Electronics', 'Clothing', 'Books', 'Home', 'Sports'),
            ELT(FLOOR(RAND() * 4) + 1, 'North', 'South', 'East', 'West'),
            DAYOFWEEK(current_date) - 1,
            MONTH(current_date),
            CASE WHEN DAYOFWEEK(current_date) IN (1,7) THEN TRUE ELSE FALSE END,
            ROUND(RAND() * 30 + 5, 2), -- Temperature between 5-35°C
            ROUND(RAND() * 500 + 100, 2) -- Marketing spend 100-600
        );
        
        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
        SET i = i + 1;
    END WHILE;
END //

-- Calculate Business Metrics
CREATE PROCEDURE IF NOT EXISTS CalculateBusinessMetrics()
BEGIN
    -- Daily sales total
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'daily_sales_total',
        SUM(sales_amount),
        CURDATE(),
        'sales'
    FROM sales_data 
    WHERE date = CURDATE()
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
    -- Weekly sales growth
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'weekly_sales_growth',
        (
            (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)) -
            (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) AND date < DATE_SUB(CURDATE(), INTERVAL 7 DAY))
        ) / (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) AND date < DATE_SUB(CURDATE(), INTERVAL 7 DAY)) * 100,
        CURDATE(),
        'sales'
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
    -- Model accuracy average
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'model_accuracy_avg',
        AVG(performance_score) * 100,
        CURDATE(),
        'ml'
    FROM ml_models 
    WHERE is_active = TRUE
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
END //

DELIMITER ;

-- ================================
-- PERFORMANCE INDEXES
-- ================================

CREATE INDEX IF NOT EXISTS idx_sales_date_amount ON sales_data(date, sales_amount);
CREATE INDEX IF NOT EXISTS idx_predictions_target_date ON predictions(target_date);
CREATE INDEX IF NOT EXISTS idx_conversations_session_date ON conversations(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_models_active_score ON ml_models(is_active, performance_score);

-- ================================
-- SALES DATA TABLE
-- ================================
CREATE TABLE sales_data (
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
);

-- ================================
-- ML MODELS TABLE
-- ================================
CREATE TABLE ml_models (
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
);

-- ================================
-- PREDICTIONS TABLE
-- ================================
CREATE TABLE predictions (
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
);

-- ================================
-- CHAT CONVERSATIONS TABLE
-- ================================
CREATE TABLE conversations (
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
);

-- ================================
-- DATA QUALITY MONITORING
-- ================================
CREATE TABLE data_quality (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    check_result ENUM('passed', 'failed', 'warning') NOT NULL,
    message TEXT,
    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_table_result (table_name, check_result),
    INDEX idx_check_date (check_date)
);

-- ================================
-- BUSINESS METRICS TABLE
-- ================================
CREATE TABLE business_metrics (
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
);

-- ================================
-- VIEWS FOR ANALYTICS
-- ================================

-- Daily Sales Summary View
CREATE VIEW daily_sales_summary AS
SELECT 
    date,
    SUM(sales_amount) as total_sales,
    SUM(quantity) as total_quantity,
    AVG(sales_amount) as avg_sales,
    COUNT(*) as transaction_count,
    AVG(temperature) as avg_temperature,
    SUM(marketing_spend) as total_marketing_spend
FROM sales_data 
GROUP BY date
ORDER BY date;

-- Model Performance View
CREATE VIEW model_performance AS
SELECT 
    m.id,
    m.name,
    m.version,
    m.algorithm,
    m.performance_score,
    COUNT(p.id) as prediction_count,
    AVG(p.confidence_score) as avg_confidence,
    AVG(ABS(p.accuracy_error)) as avg_error,
    m.created_at
FROM ml_models m
LEFT JOIN predictions p ON m.id = p.model_id
WHERE m.is_active = TRUE
GROUP BY m.id, m.name, m.version, m.algorithm, m.performance_score, m.created_at;

-- Recent Conversations View
CREATE VIEW recent_conversations AS
SELECT 
    session_id,
    COUNT(*) as message_count,
    MAX(created_at) as last_message_time,
    COUNT(CASE WHEN message_type = 'user' THEN 1 END) as user_messages,
    COUNT(CASE WHEN message_type = 'assistant' THEN 1 END) as bot_messages,
    AVG(processing_time_ms) as avg_processing_time
FROM conversations 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY session_id
ORDER BY last_message_time DESC;

-- ================================
-- STORED PROCEDURES
-- ================================

DELIMITER //

-- Generate Sample Sales Data
CREATE PROCEDURE GenerateSampleSalesData(IN days_count INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE current_date DATE DEFAULT DATE_SUB(CURDATE(), INTERVAL days_count DAY);
    DECLARE base_sales DECIMAL(10,2) DEFAULT 100;
    DECLARE seasonal_factor DECIMAL(5,4);
    DECLARE trend_factor DECIMAL(5,4);
    DECLARE noise_factor DECIMAL(5,4);
    DECLARE final_sales DECIMAL(10,2);
    
    WHILE i < days_count DO
        -- Calculate seasonal factor (sine wave)
        SET seasonal_factor = 20 * SIN(2 * PI() * i / 365);
        
        -- Calculate trend factor (gradual increase)
        SET trend_factor = i * 0.1;
        
        -- Add random noise
        SET noise_factor = (RAND() - 0.5) * 20;
        
        -- Calculate final sales amount
        SET final_sales = base_sales + seasonal_factor + trend_factor + noise_factor;
        SET final_sales = GREATEST(final_sales, 10); -- Minimum sales
        
        INSERT INTO sales_data (
            date, 
            sales_amount, 
            quantity, 
            product_category,
            region,
            day_of_week,
            month,
            is_weekend,
            temperature,
            marketing_spend
        ) VALUES (
            current_date,
            final_sales,
            FLOOR(RAND() * 50) + 1,
            ELT(FLOOR(RAND() * 5) + 1, 'Electronics', 'Clothing', 'Books', 'Home', 'Sports'),
            ELT(FLOOR(RAND() * 4) + 1, 'North', 'South', 'East', 'West'),
            DAYOFWEEK(current_date) - 1,
            MONTH(current_date),
            CASE WHEN DAYOFWEEK(current_date) IN (1,7) THEN TRUE ELSE FALSE END,
            ROUND(RAND() * 30 + 5, 2), -- Temperature between 5-35°C
            ROUND(RAND() * 500 + 100, 2) -- Marketing spend 100-600
        );
        
        SET current_date = DATE_ADD(current_date, INTERVAL 1 DAY);
        SET i = i + 1;
    END WHILE;
END //

-- Calculate Business Metrics
CREATE PROCEDURE CalculateBusinessMetrics()
BEGIN
    -- Daily sales total
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'daily_sales_total',
        SUM(sales_amount),
        CURDATE(),
        'sales'
    FROM sales_data 
    WHERE date = CURDATE()
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
    -- Weekly sales growth
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'weekly_sales_growth',
        (
            (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)) -
            (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) AND date < DATE_SUB(CURDATE(), INTERVAL 7 DAY))
        ) / (SELECT SUM(sales_amount) FROM sales_data WHERE date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY) AND date < DATE_SUB(CURDATE(), INTERVAL 7 DAY)) * 100,
        CURDATE(),
        'sales'
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
    -- Model accuracy average
    INSERT INTO business_metrics (metric_name, metric_value, metric_date, category)
    SELECT 
        'model_accuracy_avg',
        AVG(performance_score) * 100,
        CURDATE(),
        'ml'
    FROM ml_models 
    WHERE is_active = TRUE
    ON DUPLICATE KEY UPDATE metric_value = VALUES(metric_value);
    
END //

DELIMITER ;

-- ================================
-- INITIAL DATA
-- ================================

-- Create default ML model
INSERT INTO ml_models (name, version, algorithm, performance_score, hyperparameters, feature_columns) 
VALUES (
    'SalesPredictor',
    'v1.0',
    'RandomForest',
    0.8950,
    '{"n_estimators": 100, "max_depth": 10, "random_state": 42}',
    '["day_of_week", "month", "is_weekend", "temperature", "marketing_spend"]'
);

-- Generate sample data (365 days)
CALL GenerateSampleSalesData(365);

-- Calculate initial metrics
CALL CalculateBusinessMetrics();