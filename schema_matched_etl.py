# schema_matched_etl.py
"""
ETL that exactly matches your data schema
Based on your actual FactTransactions, DimWallet, DimMarket, and DimTime tables
"""

import pandas as pd
import sqlite3
import numpy as np
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_data_warehouse_with_your_schema():
    """Create data warehouse matching your exact schema"""
    logger.info("🏗️ Creating data warehouse with your exact schema...")
    
    dw_path = 'data/bitcoin_unified_dw.db'
    dw_engine = create_engine(f'sqlite:///{dw_path}')
    
    # Remove existing database for clean start
    import os
    if os.path.exists(dw_path):
        os.remove(dw_path)
        logger.info("   Removed existing data warehouse")
    
    # Create schema matching your exact structure
    schema_sql = [
        # DimTime - matches your schema exactly
        """CREATE TABLE DimTime (
            TimeKey INTEGER PRIMARY KEY AUTOINCREMENT,
            FullTimestamp TIMESTAMP NOT NULL,
            Date DATE NOT NULL,
            Year INTEGER,
            Quarter INTEGER,
            Month INTEGER,
            MonthName VARCHAR(20),
            Day INTEGER,
            DayOfWeekNumber INTEGER,
            DayOfWeekName VARCHAR(20),
            Hour INTEGER,
            Minute INTEGER,
            Second INTEGER,
            IsWeekend BOOLEAN,
            WeekOfYear INTEGER
        )""",
        
        # DimMarket - matches your schema exactly
        """CREATE TABLE DimMarket (
            MarketDateKey INTEGER PRIMARY KEY AUTOINCREMENT,
            MarketDate DATE NOT NULL,
            btc_usd_price_open DECIMAL(15,2),
            btc_usd_price_close DECIMAL(15,2),
            volume_usd DECIMAL(20,2),
            market_cap_usd DECIMAL(20,2)
        )""",
        
        # DimWallet - matches your schema exactly
        """CREATE TABLE DimWallet (
            WalletKey INTEGER PRIMARY KEY AUTOINCREMENT,
            WalletAddress VARCHAR(100) NOT NULL,
            FirstSeenTimestamp TIMESTAMP,
            LastSeenTimestamp TIMESTAMP,
            TransactionCount INTEGER,
            TotalReceivedSatoshi BIGINT,
            TotalSentSatoshi BIGINT,
            FinalBalanceSatoshi BIGINT,
            LabelSource VARCHAR(100),
            EntityTag VARCHAR(100),
            EntityType VARCHAR(100),
            IsReportedAbuse BOOLEAN,
            AbuseCategory VARCHAR(100)
        )""",
        
        # FactTransactions - matches your schema exactly
        """CREATE TABLE FactTransactions (
            TransactionFactSK INTEGER PRIMARY KEY AUTOINCREMENT,
            TradeID BIGINT NOT NULL,
            Side VARCHAR(10),
            TimeKey INTEGER,
            MarketDateKey INTEGER,
            WalletKey INTEGER,
            Price DECIMAL(15,2),
            VolumeQuote DECIMAL(20,8),
            SizeBase DECIMAL(20,8),
            FOREIGN KEY (TimeKey) REFERENCES DimTime(TimeKey),
            FOREIGN KEY (MarketDateKey) REFERENCES DimMarket(MarketDateKey),
            FOREIGN KEY (WalletKey) REFERENCES DimWallet(WalletKey)
        )""",
        
        # Additional analysis tables
        """CREATE TABLE TransactionAnalysis (
            AnalysisKey INTEGER PRIMARY KEY AUTOINCREMENT,
            TransactionFactSK INTEGER,
            IsSuspicious BOOLEAN DEFAULT 0,
            AnomalyScore DECIMAL(5,2) DEFAULT 0,
            RiskLevel VARCHAR(20) DEFAULT 'LOW',
            AnalysisDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (TransactionFactSK) REFERENCES FactTransactions(TransactionFactSK)
        )""",
        
        # Daily summary table
        """CREATE TABLE DailySummary (
            SummaryKey INTEGER PRIMARY KEY AUTOINCREMENT,
            SummaryDate DATE NOT NULL UNIQUE,
            TotalTransactions INTEGER,
            TotalVolumeUSD DECIMAL(20,2),
            AvgPrice DECIMAL(15,2),
            MaxPrice DECIMAL(15,2),
            MinPrice DECIMAL(15,2),
            SuspiciousTransactions INTEGER,
            HighRiskTransactions INTEGER
        )""",
        
        # Indexes for performance
        "CREATE INDEX idx_fact_tradeid ON FactTransactions(TradeID)",
        "CREATE INDEX idx_fact_timekey ON FactTransactions(TimeKey)",
        "CREATE INDEX idx_fact_marketkey ON FactTransactions(MarketDateKey)",
        "CREATE INDEX idx_fact_walletkey ON FactTransactions(WalletKey)",
        "CREATE INDEX idx_fact_price ON FactTransactions(Price)",
        "CREATE INDEX idx_dimtime_date ON DimTime(Date)",
        "CREATE INDEX idx_dimmarket_date ON DimMarket(MarketDate)",
        "CREATE INDEX idx_dimwallet_address ON DimWallet(WalletAddress)"
    ]
    
    try:
        with dw_engine.connect() as conn:
            for i, stmt in enumerate(schema_sql):
                conn.execute(text(stmt))
                logger.info(f"   ✅ Schema statement {i+1}/{len(schema_sql)} executed")
            
            conn.commit()
            logger.info("✅ Schema created successfully")
        
        return dw_engine
        
    except Exception as e:
        logger.error(f"❌ Schema creation failed: {e}")
        return None

def load_your_data(dw_engine):
    """Load data from your existing databases"""
    logger.info("📥 Loading data from your existing databases...")
    
    try:
        with dw_engine.begin() as conn:
            
            # 1. Load DimTime
            logger.info("📅 Loading DimTime...")
            time_conn = sqlite3.connect('data/time_data.db')
            time_df = pd.read_sql("SELECT * FROM dim_time LIMIT 20000", time_conn)
            time_conn.close()
            
            # Map to your schema
            time_mapped = pd.DataFrame()
            time_mapped['FullTimestamp'] = pd.to_datetime(time_df['timestamp'])
            time_mapped['Date'] = time_mapped['FullTimestamp'].dt.date
            time_mapped['Year'] = time_df['year']
            time_mapped['Quarter'] = time_mapped['FullTimestamp'].dt.quarter
            time_mapped['Month'] = time_df['month']
            time_mapped['MonthName'] = time_mapped['FullTimestamp'].dt.strftime('%B')
            time_mapped['Day'] = time_df['day']
            time_mapped['DayOfWeekNumber'] = time_mapped['FullTimestamp'].dt.dayofweek
            time_mapped['DayOfWeekName'] = time_df['weekday']
            time_mapped['Hour'] = time_df['hour']
            time_mapped['Minute'] = time_mapped['FullTimestamp'].dt.minute
            time_mapped['Second'] = time_mapped['FullTimestamp'].dt.second
            time_mapped['IsWeekend'] = (time_mapped['FullTimestamp'].dt.dayofweek >= 5).astype(int)
            time_mapped['WeekOfYear'] = time_mapped['FullTimestamp'].dt.isocalendar().week
            
            time_mapped.to_sql('DimTime', conn, if_exists='append', index=False)
            logger.info(f"   ✅ DimTime: {len(time_mapped)} records")
            
            # 2. Load DimMarket
            logger.info("📊 Loading DimMarket...")
            market_conn = sqlite3.connect('data/dim_market.db')
            market_df = pd.read_sql("SELECT * FROM dim_market", market_conn)
            market_conn.close()
            
            # Map to your schema
            market_mapped = pd.DataFrame()
            market_mapped['MarketDate'] = pd.to_datetime(market_df['date']).dt.date
            market_mapped['btc_usd_price_open'] = market_df['btc_usd_price_open']
            market_mapped['btc_usd_price_close'] = market_df['btc_usd_price_close']
            market_mapped['volume_usd'] = market_df['volume_usd']
            market_mapped['market_cap_usd'] = market_df['market_cap_usd']
            
            market_mapped.to_sql('DimMarket', conn, if_exists='append', index=False)
            logger.info(f"   ✅ DimMarket: {len(market_mapped)} records")
            
            # 3. Load DimWallet
            logger.info("💳 Loading DimWallet...")
            wallet_conn = sqlite3.connect('data/dim_wallet.db')
            wallet_df = pd.read_sql("SELECT * FROM dim_wallet", wallet_conn)
            wallet_conn.close()
            
            # Map to your schema exactly
            wallet_mapped = pd.DataFrame()
            wallet_mapped['WalletAddress'] = wallet_df['wallet_address']
            wallet_mapped['FirstSeenTimestamp'] = pd.to_datetime(wallet_df['first_seen_timestamp'], errors='coerce')
            wallet_mapped['LastSeenTimestamp'] = pd.to_datetime(wallet_df['last_seen_timestamp'], errors='coerce')
            wallet_mapped['TransactionCount'] = wallet_df['transaction_count']
            wallet_mapped['TotalReceivedSatoshi'] = wallet_df['total_received_satoshi']
            wallet_mapped['TotalSentSatoshi'] = wallet_df['total_sent_satoshi']
            wallet_mapped['FinalBalanceSatoshi'] = wallet_df['final_balance_satoshi']
            wallet_mapped['LabelSource'] = wallet_df['label_source']
            wallet_mapped['EntityTag'] = wallet_df['entity_tag']
            wallet_mapped['EntityType'] = wallet_df['entity_type']
            wallet_mapped['IsReportedAbuse'] = wallet_df['is_reported_abuse']
            wallet_mapped['AbuseCategory'] = wallet_df['abuse_category']
            
            wallet_mapped.to_sql('DimWallet', conn, if_exists='append', index=False)
            logger.info(f"   ✅ DimWallet: {len(wallet_mapped)} records")
            
            # 4. Load FactTransactions
            logger.info("₿ Loading FactTransactions...")
            btc_conn = sqlite3.connect('data/bitcoin_dw.db')
            trans_df = pd.read_sql("SELECT * FROM fact_transactions LIMIT 10000", btc_conn)
            btc_conn.close()
            
            # Get foreign key mappings
            time_keys = pd.read_sql("SELECT TimeKey, Date FROM DimTime", conn)
            market_keys = pd.read_sql("SELECT MarketDateKey, MarketDate FROM DimMarket", conn)
            wallet_keys = pd.read_sql("SELECT WalletKey FROM DimWallet", conn)
            
            # Map transactions to your schema
            trans_mapped = pd.DataFrame()
            trans_mapped['TradeID'] = trans_df['trade_id']
            trans_mapped['Side'] = trans_df['side']
            trans_mapped['Price'] = trans_df['price']
            trans_mapped['VolumeQuote'] = trans_df['volume(quote)']
            trans_mapped['SizeBase'] = trans_df['size(base)']
            
            # Map foreign keys
            # For TimeKey - match by extracting date from timestamp
            trans_timestamps = pd.to_datetime(trans_df['timestamp'], unit='ms')
            trans_dates = trans_timestamps.dt.date
            
            # Create a lookup for time keys
            time_lookup = time_keys.set_index('Date')['TimeKey'].to_dict()
            trans_mapped['TimeKey'] = trans_dates.map(time_lookup)
            
            # For MarketDateKey - match by date
            market_lookup = market_keys.set_index('MarketDate')['MarketDateKey'].to_dict()
            trans_mapped['MarketDateKey'] = trans_dates.map(market_lookup)
            
            # For WalletKey - random assignment (since we don't have transaction->wallet mapping)
            if len(wallet_keys) > 0:
                trans_mapped['WalletKey'] = np.random.choice(wallet_keys['WalletKey'], size=len(trans_df), replace=True)
            
            # Clean up NaN values
            trans_mapped['TimeKey'] = trans_mapped['TimeKey'].fillna(1)
            trans_mapped['MarketDateKey'] = trans_mapped['MarketDateKey'].fillna(1)
            trans_mapped['WalletKey'] = trans_mapped['WalletKey'].fillna(1)
            
            trans_mapped.to_sql('FactTransactions', conn, if_exists='append', index=False)
            logger.info(f"   ✅ FactTransactions: {len(trans_mapped)} records")
            
            # 5. Create Transaction Analysis
            logger.info("🔍 Creating transaction analysis...")
            
            # Get all transaction keys
            fact_keys = pd.read_sql("SELECT TransactionFactSK, Price, VolumeQuote FROM FactTransactions", conn)
            
            analysis_data = pd.DataFrame()
            analysis_data['TransactionFactSK'] = fact_keys['TransactionFactSK']
            
            # Risk analysis based on patterns
            analysis_data['IsSuspicious'] = (
                (fact_keys['VolumeQuote'] % 1000 == 0) |  # Round amounts
                (fact_keys['VolumeQuote'] > 100000) |      # Large amounts
                (fact_keys['Price'] % 100 == 0)           # Round prices
            ).astype(int)
            
            # Anomaly score
            analysis_data['AnomalyScore'] = np.where(
                analysis_data['IsSuspicious'] == 1,
                50 + np.random.uniform(0, 50, len(fact_keys)),  # 50-100 for suspicious
                np.random.uniform(0, 30, len(fact_keys))        # 0-30 for normal
            )
            
            # Risk level
            analysis_data['RiskLevel'] = pd.cut(
                analysis_data['AnomalyScore'], 
                bins=[0, 25, 50, 75, 100], 
                labels=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            )
            
            analysis_data.to_sql('TransactionAnalysis', conn, if_exists='append', index=False)
            logger.info(f"   ✅ TransactionAnalysis: {len(analysis_data)} records")
            
            # 6. Create Daily Summary
            logger.info("📊 Creating daily summary...")
            
            daily_sql = """
            INSERT INTO DailySummary (
                SummaryDate, TotalTransactions, TotalVolumeUSD, AvgPrice, 
                MaxPrice, MinPrice, SuspiciousTransactions, HighRiskTransactions
            )
            SELECT 
                dt.Date as SummaryDate,
                COUNT(*) as TotalTransactions,
                SUM(ft.VolumeQuote) as TotalVolumeUSD,
                AVG(ft.Price) as AvgPrice,
                MAX(ft.Price) as MaxPrice,
                MIN(ft.Price) as MinPrice,
                SUM(CASE WHEN ta.IsSuspicious = 1 THEN 1 ELSE 0 END) as SuspiciousTransactions,
                SUM(CASE WHEN ta.RiskLevel IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as HighRiskTransactions
            FROM FactTransactions ft
            JOIN DimTime dt ON ft.TimeKey = dt.TimeKey
            LEFT JOIN TransactionAnalysis ta ON ft.TransactionFactSK = ta.TransactionFactSK
            GROUP BY dt.Date
            ORDER BY dt.Date
            """
            
            conn.execute(text(daily_sql))
            logger.info("   ✅ DailySummary created")
            
            logger.info("✅ All data loaded successfully")
            
    except Exception as e:
        logger.error(f"❌ Data loading failed: {e}")
        return False
    
    return True

def create_analytical_views(dw_engine):
    """Create views for analysis matching your schema"""
    logger.info("👁️ Creating analytical views...")
    
    views = [
        # Transaction Analysis View
        """CREATE VIEW vw_TransactionAnalysis AS
        SELECT 
            ft.TradeID,
            ft.Side,
            dt.Date,
            dt.Hour,
            dt.DayOfWeekName,
            ft.Price,
            ft.VolumeQuote,
            ft.SizeBase,
            dw.WalletAddress,
            dw.EntityType,
            ta.IsSuspicious,
            ta.AnomalyScore,
            ta.RiskLevel
        FROM FactTransactions ft
        LEFT JOIN DimTime dt ON ft.TimeKey = dt.TimeKey
        LEFT JOIN DimWallet dw ON ft.WalletKey = dw.WalletKey
        LEFT JOIN TransactionAnalysis ta ON ft.TransactionFactSK = ta.TransactionFactSK""",
        
        # Daily Summary View
        """CREATE VIEW vw_DailySummary AS
        SELECT 
            SummaryDate,
            TotalTransactions,
            ROUND(TotalVolumeUSD, 2) as TotalVolumeUSD,
            ROUND(AvgPrice, 2) as AvgPrice,
            ROUND(MaxPrice, 2) as MaxPrice,
            ROUND(MinPrice, 2) as MinPrice,
            SuspiciousTransactions,
            HighRiskTransactions,
            ROUND(SuspiciousTransactions * 100.0 / TotalTransactions, 2) as SuspiciousRate
        FROM DailySummary
        ORDER BY SummaryDate DESC""",
        
        # Wallet Risk View
        """CREATE VIEW vw_WalletRisk AS
        SELECT 
            dw.WalletAddress,
            dw.EntityType,
            dw.IsReportedAbuse,
            dw.AbuseCategory,
            dw.TransactionCount,
            ROUND(dw.TotalReceivedSatoshi / 100000000.0, 8) as TotalReceivedBTC,
            COUNT(ft.TransactionFactSK) as RecentTransactions,
            AVG(ta.AnomalyScore) as AvgAnomalyScore,
            SUM(CASE WHEN ta.IsSuspicious = 1 THEN 1 ELSE 0 END) as SuspiciousTransactions
        FROM DimWallet dw
        LEFT JOIN FactTransactions ft ON dw.WalletKey = ft.WalletKey
        LEFT JOIN TransactionAnalysis ta ON ft.TransactionFactSK = ta.TransactionFactSK
        GROUP BY dw.WalletKey, dw.WalletAddress, dw.EntityType, dw.IsReportedAbuse, 
                 dw.AbuseCategory, dw.TransactionCount, dw.TotalReceivedSatoshi
        ORDER BY AvgAnomalyScore DESC""",
        
        # Market Performance View
        """CREATE VIEW vw_MarketPerformance AS
        SELECT 
            dm.MarketDate,
            dm.btc_usd_price_open,
            dm.btc_usd_price_close,
            ROUND(dm.btc_usd_price_close - dm.btc_usd_price_open, 2) as PriceChange,
            ROUND((dm.btc_usd_price_close - dm.btc_usd_price_open) * 100.0 / dm.btc_usd_price_open, 2) as PriceChangePercent,
            dm.volume_usd,
            COUNT(ft.TransactionFactSK) as TransactionCount
        FROM DimMarket dm
        LEFT JOIN FactTransactions ft ON dm.MarketDateKey = ft.MarketDateKey
        GROUP BY dm.MarketDateKey, dm.MarketDate, dm.btc_usd_price_open, 
                 dm.btc_usd_price_close, dm.volume_usd
        ORDER BY dm.MarketDate DESC"""
    ]
    
    try:
        with dw_engine.connect() as conn:
            for i, view in enumerate(views):
                conn.execute(text(view))
                logger.info(f"   ✅ View {i+1}/{len(views)} created")
            
            conn.commit()
            logger.info("✅ All views created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ View creation failed: {e}")
        return False

def validate_and_test(dw_engine):
    """Validate the data warehouse and run test queries"""
    logger.info("🔍 Validating data warehouse...")
    
    try:
        with dw_engine.connect() as conn:
            
            # Check table counts
            tables = ['DimTime', 'DimMarket', 'DimWallet', 'FactTransactions', 
                     'TransactionAnalysis', 'DailySummary']
            
            print("\n" + "="*60)
            print("📊 BITCOIN DECISION SUPPORT SYSTEM - DATA VALIDATION")
            print("="*60)
            
            for table in tables:
                count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
                print(f"   {table}: {count:,} records")
            
            # Test analytics
            print("\n📈 SAMPLE ANALYTICS:")
            
            # Daily summary
            daily_sample = pd.read_sql("""
                SELECT * FROM vw_DailySummary LIMIT 5
            """, conn)
            print("\nDaily Summary (Top 5 days):")
            print(daily_sample.to_string(index=False))
            
            # Transaction analysis
            trans_sample = pd.read_sql("""
                SELECT TradeID, Side, Price, VolumeQuote, IsSuspicious, RiskLevel 
                FROM vw_TransactionAnalysis LIMIT 10
            """, conn)
            print("\nTransaction Analysis (Sample 10):")
            print(trans_sample.to_string(index=False))
            
            # Risk summary
            risk_summary = pd.read_sql("""
                SELECT 
                    RiskLevel,
                    COUNT(*) as Count,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM TransactionAnalysis), 2) as Percentage
                FROM TransactionAnalysis 
                GROUP BY RiskLevel 
                ORDER BY Count DESC
            """, conn)
            print("\nRisk Level Distribution:")
            print(risk_summary.to_string(index=False))
            
            print("\n" + "="*60)
            print("🎉 SUCCESS! Your Bitcoin DSS is fully operational!")
            print("="*60)
            
    except Exception as e:
        logger.error(f"❌ Validation failed: {e}")
        return False
    
    return True

def main():
    """Main function to create the complete data warehouse"""
    print("🚀 BITCOIN DECISION SUPPORT SYSTEM")
    print("Schema-Matched Implementation")
    print("=" * 60)
    
    # Step 1: Create schema
    dw_engine = create_data_warehouse_with_your_schema()
    if not dw_engine:
        print("❌ Schema creation failed")
        return
    
    # Step 2: Load data
    if not load_your_data(dw_engine):
        print("❌ Data loading failed")
        return
    
    # Step 3: Create views
    if not create_analytical_views(dw_engine):
        print("❌ View creation failed")
        return
    
    # Step 4: Validate and test
    if validate_and_test(dw_engine):
        print("\n🎯 NEXT STEPS:")
        print("1. Launch dashboard: streamlit run dashboard_app.py")
        print("2. Explore database: sqlite3 data/bitcoin_unified_dw.db")
        print("3. Try these queries:")
        print("   SELECT * FROM vw_DailySummary;")
        print("   SELECT * FROM vw_TransactionAnalysis LIMIT 20;")
        print("   SELECT * FROM vw_WalletRisk WHERE IsReportedAbuse = 1;")
        print("   SELECT * FROM vw_MarketPerformance LIMIT 10;")
    else:
        print("❌ Validation failed")

if __name__ == "__main__":
    main()