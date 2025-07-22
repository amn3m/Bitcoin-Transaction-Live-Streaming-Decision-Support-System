-- Bitcoin Data Warehouse Schema Design
-- Star Schema with Fact and Dimension Tables

-- ==============================================
-- DIMENSION TABLES
-- ==============================================

-- Time Dimension Table
CREATE TABLE dim_time (
    time_key SERIAL PRIMARY KEY,
    date_actual DATE NOT NULL,
    timestamp_actual TIMESTAMP NOT NULL,
    hour_24 INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month_actual INTEGER,
    month_name VARCHAR(10),
    quarter_actual INTEGER,
    year_actual INTEGER,
    is_weekend BOOLEAN,
    UNIQUE(timestamp_actual)
);

-- Block Dimension Table
CREATE TABLE dim_block (
    block_key SERIAL PRIMARY KEY,
    block_hash VARCHAR(64) UNIQUE NOT NULL,
    block_height INTEGER UNIQUE NOT NULL,
    block_timestamp TIMESTAMP NOT NULL,
    difficulty BIGINT,
    block_size INTEGER,
    transaction_count INTEGER,
    miner_address VARCHAR(64),
    block_reward DECIMAL(20,8),
    total_fees DECIMAL(20,8)
);

-- Address Dimension Table
CREATE TABLE dim_address (
    address_key SERIAL PRIMARY KEY,
    address_hash VARCHAR(64) UNIQUE NOT NULL,
    address_type VARCHAR(20), -- P2PKH, P2SH, Bech32, etc.
    first_seen_date DATE,
    last_seen_date DATE,
    total_received DECIMAL(20,8) DEFAULT 0,
    total_sent DECIMAL(20,8) DEFAULT 0,
    current_balance DECIMAL(20,8) DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    risk_score INTEGER DEFAULT 0, -- 0-100 risk rating
    is_exchange BOOLEAN DEFAULT FALSE,
    is_mixer BOOLEAN DEFAULT FALSE,
    address_cluster_id INTEGER
);

-- Transaction Type Dimension
CREATE TABLE dim_transaction_type (
    type_key SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL,
    type_description TEXT,
    is_suspicious BOOLEAN DEFAULT FALSE
);

-- ==============================================
-- FACT TABLE
-- ==============================================

-- Main Bitcoin Transactions Fact Table
CREATE TABLE fact_bitcoin_transactions (
    transaction_key SERIAL PRIMARY KEY,
    transaction_hash VARCHAR(64) UNIQUE NOT NULL,
    
    -- Foreign Keys to Dimension Tables
    time_key INTEGER REFERENCES dim_time(time_key),
    block_key INTEGER REFERENCES dim_block(block_key),
    transaction_type_key INTEGER REFERENCES dim_transaction_type(type_key),
    
    -- Transaction Metrics
    input_count INTEGER NOT NULL,
    output_count INTEGER NOT NULL,
    total_input_value DECIMAL(20,8) NOT NULL,
    total_output_value DECIMAL(20,8) NOT NULL,
    transaction_fee DECIMAL(20,8) NOT NULL,
    transaction_size INTEGER NOT NULL, -- in bytes
    fee_per_byte DECIMAL(10,4),
    
    -- Analysis Fields
    is_coinbase BOOLEAN DEFAULT FALSE,
    is_suspicious BOOLEAN DEFAULT FALSE,
    anomaly_score DECIMAL(5,2) DEFAULT 0, -- ML-generated anomaly score
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================
-- BRIDGE TABLES (Many-to-Many Relationships)
-- ==============================================

-- Transaction Inputs Bridge Table
CREATE TABLE bridge_transaction_inputs (
    input_id SERIAL PRIMARY KEY,
    transaction_key INTEGER REFERENCES fact_bitcoin_transactions(transaction_key),
    address_key INTEGER REFERENCES dim_address(address_key),
    input_value DECIMAL(20,8) NOT NULL,
    input_index INTEGER NOT NULL,
    previous_transaction_hash VARCHAR(64),
    previous_output_index INTEGER
);

-- Transaction Outputs Bridge Table
CREATE TABLE bridge_transaction_outputs (
    output_id SERIAL PRIMARY KEY,
    transaction_key INTEGER REFERENCES fact_bitcoin_transactions(transaction_key),
    address_key INTEGER REFERENCES dim_address(address_key),
    output_value DECIMAL(20,8) NOT NULL,
    output_index INTEGER NOT NULL,
    is_spent BOOLEAN DEFAULT FALSE,
    spent_in_transaction VARCHAR(64),
    script_type VARCHAR(20)
);

-- ==============================================
-- AGGREGATED FACT TABLES (For Performance)
-- ==============================================

-- Daily Transaction Summary
CREATE TABLE fact_daily_summary (
    summary_key SERIAL PRIMARY KEY,
    date_actual DATE NOT NULL,
    total_transactions INTEGER,
    total_volume DECIMAL(20,8),
    total_fees DECIMAL(20,8),
    avg_transaction_size DECIMAL(10,2),
    avg_fee_per_byte DECIMAL(10,4),
    suspicious_transactions INTEGER,
    unique_addresses INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date_actual)
);

-- Hourly Transaction Metrics
CREATE TABLE fact_hourly_metrics (
    metric_key SERIAL PRIMARY KEY,
    date_hour TIMESTAMP NOT NULL,
    transaction_count INTEGER,
    transaction_volume DECIMAL(20,8),
    avg_confirmation_time DECIMAL(10,2),
    network_hash_rate BIGINT,
    price_usd DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date_hour)
);

-- ==============================================
-- INDEXES FOR PERFORMANCE
-- ==============================================

-- Fact table indexes
CREATE INDEX idx_fact_transactions_time ON fact_bitcoin_transactions(time_key);
CREATE INDEX idx_fact_transactions_block ON fact_bitcoin_transactions(block_key);
CREATE INDEX idx_fact_transactions_hash ON fact_bitcoin_transactions(transaction_hash);
CREATE INDEX idx_fact_transactions_fee ON fact_bitcoin_transactions(transaction_fee);
CREATE INDEX idx_fact_transactions_suspicious ON fact_bitcoin_transactions(is_suspicious);

-- Bridge table indexes
CREATE INDEX idx_bridge_inputs_transaction ON bridge_transaction_inputs(transaction_key);
CREATE INDEX idx_bridge_inputs_address ON bridge_transaction_inputs(address_key);
CREATE INDEX idx_bridge_outputs_transaction ON bridge_transaction_outputs(transaction_key);
CREATE INDEX idx_bridge_outputs_address ON bridge_transaction_outputs(address_key);

-- Dimension table indexes
CREATE INDEX idx_dim_time_date ON dim_time(date_actual);
CREATE INDEX idx_dim_block_height ON dim_block(block_height);
CREATE INDEX idx_dim_address_hash ON dim_address(address_hash);

-- ==============================================
-- VIEWS FOR COMMON QUERIES
-- ==============================================

-- Transaction Details View
CREATE VIEW vw_transaction_details AS
SELECT 
    ft.transaction_hash,
    dt.date_actual,
    dt.hour_24,
    db.block_height,
    ft.total_input_value,
    ft.total_output_value,
    ft.transaction_fee,
    ft.fee_per_byte,
    ft.is_suspicious,
    ft.anomaly_score
FROM fact_bitcoin_transactions ft
JOIN dim_time dt ON ft.time_key = dt.time_key
JOIN dim_block db ON ft.block_key = db.block_key;

-- Daily Transaction Summary View
CREATE VIEW vw_daily_transactions AS
SELECT 
    dt.date_actual,
    COUNT(*) as transaction_count,
    SUM(ft.total_output_value) as daily_volume,
    SUM(ft.transaction_fee) as daily_fees,
    AVG(ft.fee_per_byte) as avg_fee_per_byte,
    COUNT(CASE WHEN ft.is_suspicious THEN 1 END) as suspicious_count
FROM fact_bitcoin_transactions ft
JOIN dim_time dt ON ft.time_key = dt.time_key
GROUP BY dt.date_actual
ORDER BY dt.date_actual;

-- ==============================================
-- INITIAL DATA SETUP
-- ==============================================

-- Insert default transaction types
INSERT INTO dim_transaction_type (type_name, type_description, is_suspicious) VALUES
('Standard', 'Regular peer-to-peer transaction', FALSE),
('Coinbase', 'Mining reward transaction', FALSE),
('Multi-signature', 'Transaction requiring multiple signatures', FALSE),
('High-value', 'Transaction above average value threshold', FALSE),
('Rapid-succession', 'Multiple transactions from same address quickly', TRUE),
('Round-amount', 'Transaction with suspiciously round amounts', TRUE),
('Mixing', 'Potential coin mixing transaction', TRUE),
('Unknown', 'Transaction type could not be determined', FALSE);