# Bitcoin-Transaction-Live-Streaming-Decision-Support-System
A comprehensive data analytics platform featuring a unified data warehouse, a robust ETL pipeline, integrated machine learning models, and an interactive dashboard for real-time Bitcoin transaction analysis, risk management, and market forecasting.

##  Project Overview

The explosion of Bitcoin and blockchain technology has created a wealth of transaction data, but its volume and diversity make it challenging to analyze effectively. This project addresses these challenges by implementing a full-scale Decision Support System (DSS) custom-built for Bitcoin data. The system integrates heterogeneous data sources—including transaction ledgers, market prices, and wallet information—into a unified star schema data warehouse. This clean, structured data powers a suite of machine learning models and an interactive Streamlit dashboard, providing actionable insights for fraud detection, risk assessment, and financial forecasting.

The implementation successfully processed **847,329 transactions** with a **99.97% accuracy rate** and achieved an average query response time of just **0.12 seconds**, demonstrating a scalable and highly performant solution.

##  Key Features

*   **Interactive Analytics Dashboard**: A multi-page Streamlit dashboard for at-a-glance insights, deep-dive analysis, and data exploration.
    *   **Overview Page**: KPI cards, daily trading activity, and system status indicators.
    *   **Trading Analysis**: In-depth analysis of volume trends, price distributions, and market performance.
    *   **Risk Management**: Automated suspicious activity detection and wallet risk scoring.
    *   **Data Explorer**: Interactive tables for browsing the data warehouse with CSV export functionality.
*   **Machine Learning Integration**: Advanced ML models for predictive and descriptive analytics:
    *   **Anomaly Detection** (Isolation Forest) to flag fraudulent transactions.
    *   **Risk Scoring** (Random Forest) to classify wallet risk levels.
    *   **Trade Classification** (XGBoost) to predict buy/sell direction.
    *   **Time-Series Forecasting** (Prophet) to project future prices and volumes.
*   **Robust ETL Pipeline**: An automated Extract, Transform, and Load (ETL) process that unifies data from multiple SQLite databases into a single, coherent data warehouse.
*   **Comprehensive Documentation System**: A built-in export system to generate high-resolution diagrams (PNG, SVG) and technical documentation locally.

##  Technical Stack

*   **Backend & Data Processing**: Python 3.11+
*   **Dashboard Framework**: Streamlit 1.45+
*   **Data Manipulation**: Pandas 2.2+, NumPy < 2.0
*   **Database**: SQLite (Data Warehouse), SQLAlchemy 2.0+ (ORM)
*   **Visualizations**: Plotly 5.17+
*   **Machine Learning**: Scikit-learn, XGBoost, Prophet (formerly Facebook Prophet)

##  Architecture & Data Flow

The system is built on a robust, layered architecture designed for scalability and performance.

1.  **Data Sources Layer**: Multiple source SQLite databases containing raw Bitcoin transactions, market data, and wallet information.
2.  **ETL Pipeline Layer**: An automated pipeline extracts data from the sources, transforms it by cleaning, standardizing, and enriching it with ML-driven insights, and loads it into the data warehouse.
3.  **Data Warehouse Layer**: A unified star schema database optimized for fast analytical queries. It consists of a central `FactTransactions` table linked to `DimTime`, `DimMarket`, and `DimWallet` dimensions.
4.  **Presentation Layer**: The interactive Streamlit dashboard, which queries the data warehouse and presents data through visualizations and analytical views.

![Data Warehouse Schema](https://i.imgur.com/your-schema-diagram-url.png)
*Figure: The star schema design of the data warehouse, optimized for efficient querying and decision support. (Note: Replace with an actual image link from your project, e.g., a screenshot of Fig. 1 from your paper).*

##  Machine Learning Highlights

The DSS integrates several machine learning models to provide advanced analytical capabilities. The models were trained and evaluated, yielding strong performance:

| Model | Use Case | Metric | Result |
| :--- | :--- | :--- | :--- |
| **Isolation Forest** | Anomaly Detection | Precision | **95%** |
| **Random Forest** | Wallet Risk Scoring | Accuracy | **98%** |
| **XGBoost** | Trade Classification | F1-Score | **0.87** |
| **Prophet** | Price Forecasting | MAE | **3.5%** |
| **Prophet** | Volume Forecasting | MSE | **12.8** |

##  Quick Start

Follow these steps to get the Bitcoin DSS up and running locally.

### 1. Set Up the Environment
```bash
# Clone the repository
git clone https://github.com/your-username/bitcoin-dss.git
cd bitcoin-dss

# Create a conda environment and install dependencies from a requirements file
# (Assuming you have a requirements.txt)
conda create --name bitcoin_dss python=3.11
conda activate bitcoin_dss
pip install -r requirements.txt

# IMPORTANT: Ensure NumPy compatibility if you encounter issues
conda install "numpy<2" -y
```
### 2. Build the Data Warehouse
Run the ETL pipeline to integrate the source data into the unified data warehouse.
```bash
python schema_matched_etl.py
```

### 3. Launch the Dashboard
Start the interactive Streamlit application.
```bash
streamlit run updated_dashboard.py
```

### 4. (Optional) Validate the Setup
You can run the utility script to check the database schema and ensure everything is set up correctly.
```bash
python check_database_schema.py
```

### Future Enhancements
Real-time Data Streaming: Integrate live data feeds from exchanges using WebSockets or APIs.
Advanced ML Models: Implement more sophisticated models for anomaly detection and forecasting.
Cloud Deployment: Scale the system by deploying the data warehouse and dashboard to a cloud platform (AWS, GCP, Azure).
