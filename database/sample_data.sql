-- ================================
-- SAMPLE DATA FOR AI PREDICTIVE SYSTEM
-- Données d'exemple pour démonstration
-- ================================

USE chatbot_predictive;

-- ================================
-- INITIAL ML MODEL
-- ================================

INSERT INTO ml_models (name, version, algorithm, performance_score, hyperparameters, feature_columns) 
VALUES (
    'SalesPredictor',
    'v1.0',
    'RandomForest',
    0.8950,
    '{"n_estimators": 100, "max_depth": 10, "random_state": 42}',
    '["day_of_week", "month", "is_weekend", "temperature", "marketing_spend"]'
);

INSERT INTO ml_models (name, version, algorithm, performance_score, hyperparameters, feature_columns) 
VALUES (
    'RevenueForecaster',
    'v1.1',
    'XGBoost',
    0.9123,
    '{"learning_rate": 0.1, "max_depth": 8, "n_estimators": 200}',
    '["day_of_week", "month", "is_weekend", "temperature", "marketing_spend", "region"]'
);

-- ================================
-- SAMPLE SALES DATA (Last 30 days)
-- ================================

INSERT INTO sales_data (date, sales_amount, quantity, product_category, region, day_of_week, month, is_weekend, temperature, marketing_spend) VALUES
('2024-12-15', 145.67, 3, 'Electronics', 'North', 0, 12, FALSE, 8.5, 250.00),
('2024-12-15', 89.23, 2, 'Clothing', 'South', 0, 12, FALSE, 8.5, 250.00),
('2024-12-15', 234.78, 1, 'Electronics', 'East', 0, 12, FALSE, 8.5, 250.00),
('2024-12-16', 167.89, 4, 'Books', 'West', 1, 12, FALSE, 9.2, 180.00),
('2024-12-16', 298.45, 2, 'Home', 'Central', 1, 12, FALSE, 9.2, 180.00),
('2024-12-17', 156.34, 3, 'Sports', 'North', 2, 12, FALSE, 7.8, 320.00),
('2024-12-18', 189.67, 5, 'Electronics', 'South', 3, 12, FALSE, 6.5, 280.00),
('2024-12-19', 223.45, 2, 'Clothing', 'East', 4, 12, FALSE, 5.9, 190.00),
('2024-12-20', 278.90, 6, 'Home', 'West', 5, 12, TRUE, 4.2, 420.00),
('2024-12-21', 345.67, 4, 'Electronics', 'Central', 6, 12, TRUE, 3.8, 380.00),
('2024-12-22', 198.23, 3, 'Books', 'North', 0, 12, FALSE, 2.1, 210.00),
('2024-12-23', 267.89, 5, 'Sports', 'South', 1, 12, FALSE, 1.5, 340.00),
('2024-12-24', 156.78, 2, 'Clothing', 'East', 2, 12, FALSE, 0.8, 150.00),
('2024-12-25', 89.45, 1, 'Books', 'West', 3, 12, FALSE, -0.2, 100.00),
('2024-12-26', 234.56, 4, 'Electronics', 'Central', 4, 12, FALSE, 1.3, 280.00),
('2024-12-27', 345.23, 6, 'Home', 'North', 5, 12, TRUE, 2.7, 450.00),
('2024-12-28', 189.90, 3, 'Sports', 'South', 6, 12, TRUE, 4.1, 320.00),
('2024-12-29', 267.34, 5, 'Electronics', 'East', 0, 12, FALSE, 5.8, 290.00),
('2024-12-30', 178.67, 2, 'Clothing', 'West', 1, 12, FALSE, 7.2, 240.00),
('2024-12-31', 298.45, 4, 'Books', 'Central', 2, 12, FALSE, 8.9, 380.00),
('2025-01-01', 156.78, 1, 'Electronics', 'North', 3, 1, FALSE, 10.5, 200.00),
('2025-01-02', 234.89, 3, 'Home', 'South', 4, 1, FALSE, 12.1, 320.00),
('2025-01-03', 189.45, 5, 'Sports', 'East', 5, 1, TRUE, 13.8, 410.00),
('2025-01-04', 267.23, 2, 'Clothing', 'West', 6, 1, TRUE, 15.2, 380.00),
('2025-01-05', 145.67, 4, 'Books', 'Central', 0, 1, FALSE, 16.9, 250.00),
('2025-01-06', 298.90, 6, 'Electronics', 'North', 1, 1, FALSE, 18.3, 390.00),
('2025-01-07', 178.34, 3, 'Home', 'South', 2, 1, FALSE, 19.7, 280.00),
('2025-01-08', 234.56, 5, 'Sports', 'East', 3, 1, FALSE, 21.1, 340.00),
('2025-01-09', 189.78, 2, 'Clothing', 'West', 4, 1, FALSE, 22.5, 290.00),
('2025-01-10', 267.45, 4, 'Electronics', 'Central', 5, 1, TRUE, 23.8, 420.00);

-- ================================
-- SAMPLE PREDICTIONS
-- ================================

INSERT INTO predictions (model_id, prediction_date, target_date, predicted_value, confidence_score, actual_value, feature_values) VALUES
(1, '2025-01-08', '2025-01-09', 189.78, 0.9250, 189.78, '{"day_of_week": 4, "month": 1, "is_weekend": false, "temperature": 22.5, "marketing_spend": 290.00}'),
(1, '2025-01-09', '2025-01-10', 267.45, 0.9180, 267.45, '{"day_of_week": 5, "month": 1, "is_weekend": true, "temperature": 23.8, "marketing_spend": 420.00}'),
(1, '2025-01-10', '2025-01-11', 195.67, 0.9320, NULL, '{"day_of_week": 6, "month": 1, "is_weekend": true, "temperature": 25.1, "marketing_spend": 380.00}'),
(2, '2025-01-08', '2025-01-09', 192.34, 0.9410, 189.78, '{"day_of_week": 4, "month": 1, "is_weekend": false, "temperature": 22.5, "marketing_spend": 290.00}'),
(2, '2025-01-09', '2025-01-10', 271.23, 0.9380, 267.45, '{"day_of_week": 5, "month": 1, "is_weekend": true, "temperature": 23.8, "marketing_spend": 420.00}'),
(2, '2025-01-10', '2025-01-11', 198.90, 0.9450, NULL, '{"day_of_week": 6, "month": 1, "is_weekend": true, "temperature": 25.1, "marketing_spend": 380.00}');

-- ================================
-- SAMPLE CONVERSATIONS
-- ================================

INSERT INTO conversations (session_id, message_type, message_content, intent_detected, confidence_score, processing_time_ms) VALUES
('demo_20250113_001', 'user', 'Hello! How are you?', 'greeting', 0.9500, 120),
('demo_20250113_001', 'assistant', 'Hello! I''m your AI-powered predictive assistant! How can I help you today?', NULL, NULL, 250),
('demo_20250113_001', 'user', 'Predict tomorrow''s sales', 'prediction', 0.9200, 150),
('demo_20250113_001', 'assistant', '🔮 Prediction Generated Successfully! Average Forecast: 195.67, Confidence Level: 93.2%', NULL, NULL, 1200),
('demo_20250113_002', 'user', 'Train a new model', 'training', 0.8900, 180),
('demo_20250113_002', 'assistant', '🤖 Model Training Completed Successfully! Performance Score: 91.8%', NULL, NULL, 2500),
('demo_20250113_002', 'user', 'Analyze current trends', 'analysis', 0.9100, 160),
('demo_20250113_002', 'assistant', '📈 Analysis Complete. Overall Trend: Increasing (+8.7%), Strong Correlations detected.', NULL, NULL, 1800);

-- ================================
-- SAMPLE BUSINESS METRICS
-- ================================

INSERT INTO business_metrics (metric_name, metric_value, metric_date, category, target_value, variance_percentage) VALUES
('daily_sales_total', 267.45, '2025-01-10', 'sales', 250.00, 6.98),
('weekly_sales_growth', 12.4, '2025-01-10', 'sales', 10.0, 24.0),
('model_accuracy_avg', 91.8, '2025-01-10', 'ml', 90.0, 2.0),
('api_response_time_ms', 145.2, '2025-01-10', 'system', 150.0, -3.2),
('prediction_requests_daily', 47, '2025-01-10', 'system', 50, -6.0),
('data_quality_score', 98.5, '2025-01-10', 'system', 95.0, 3.7);

-- ================================
-- DATA QUALITY CHECKS
-- ================================

INSERT INTO data_quality (table_name, check_type, check_result, message) VALUES
('sales_data', 'completeness', 'passed', 'All required fields present'),
('sales_data', 'accuracy', 'passed', 'Sales amounts within expected range'),
('predictions', 'consistency', 'passed', 'Prediction dates are sequential'),
('ml_models', 'validity', 'passed', 'All models have valid performance scores'),
('conversations', 'timeliness', 'passed', 'Recent conversation data available');

-- ================================
-- CALL STORED PROCEDURES FOR ADDITIONAL DATA
-- ================================

-- Generate additional historical data (uncomment if needed)
-- CALL GenerateSampleSalesData(365);

-- Calculate current business metrics
CALL CalculateBusinessMetrics();

-- ================================
-- VERIFICATION QUERIES
-- ================================

-- Verify data insertion
SELECT 'Sales Data' as table_name, COUNT(*) as record_count FROM sales_data
UNION ALL
SELECT 'ML Models', COUNT(*) FROM ml_models
UNION ALL  
SELECT 'Predictions', COUNT(*) FROM predictions
UNION ALL
SELECT 'Conversations', COUNT(*) FROM conversations
UNION ALL
SELECT 'Business Metrics', COUNT(*) FROM business_metrics;