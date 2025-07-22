# Bitcoin Decision Support System (DSS)

A comprehensive data warehouse and analytics dashboard for Bitcoin transaction analysis, risk management, and market insights.

## 🏗️ Project Structure

```
bitcoin_dss_project/
├── 📊 Core Application Files
│   ├── updated_dashboard.py          # Main Streamlit dashboard
│   ├── schema_matched_etl.py         # ETL pipeline
│   └── schema.sql                    # Database schema definition
│
├── 🗄️ Data Layer
│   └── data/
│       ├── bitcoin_unified_dw.db     # Main data warehouse
│       ├── bitcoin_dw.db             # Source: Bitcoin transactions
│       ├── dim_market.db             # Source: Market data
│       ├── dim_wallet.db             # Source: Wallet information
│       └── time_data.db              # Source: Time dimension
│
├── 🔧 Utilities
│   ├── check_database_schema.py      # Database validation
│   └── test_environment.py           # Environment testing
│
└── 📁 Project Organization
    ├── config/                       # Configuration files
    ├── docs/                         # Documentation
    ├── notebooks/                    # Jupyter notebooks
    ├── src/                          # Source code modules
    └── tests/                        # Test files
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Check environment compatibility
python test_environment.py

# Fix NumPy compatibility if needed
conda install "numpy<2" -y
```

### 2. Data Warehouse Setup
```bash
# Run ETL pipeline to create unified data warehouse
python schema_matched_etl.py
```

### 3. Launch Dashboard
```bash
# Start the interactive dashboard
streamlit run updated_dashboard.py
```

### 4. Validate Setup
```bash
# Check database schema and data
python check_database_schema.py
```

## 📊 Dashboard Features

### Overview Page
- **KPI Cards**: Total transactions, volume, suspicious activity, price metrics
- **Daily Trading Activity**: Volume trends and transaction counts
- **System Status**: Real-time monitoring indicators

### Trading Analysis
- **Volume Analysis**: Daily trading patterns
- **Price Analysis**: BTC price distribution and trends
- **Market Performance**: Trading metrics and insights

### Risk Management
- **Transaction Risk**: Risk level distribution
- **Suspicious Activity**: Flagged transactions by trade side
- **Wallet Analysis**: Entity types and abuse reporting

### Data Explorer
- **Interactive Tables**: Browse all data warehouse views
- **Export Functionality**: Download data as CSV
- **Real-time Queries**: Dynamic data exploration

## 🗄️ Database Schema

### Core Tables
- **FactTransactions**: Central fact table with trading data
- **DimTime**: Time dimension with date/time attributes
- **DimMarket**: Market data and pricing information
- **DimWallet**: Wallet information and risk indicators

### Analysis Tables
- **TransactionAnalysis**: Processed transaction insights
- **DailySummary**: Daily aggregated metrics

### Views
- **vw_DailySummary**: Daily trading summary
- **vw_TransactionAnalysis**: Enhanced transaction analysis
- **vw_WalletRisk**: Wallet risk assessment
- **vw_MarketPerformance**: Market performance metrics

## 🔧 Technical Requirements

### Dependencies
- Python 3.11+
- Streamlit 1.45+
- Pandas 2.2+
- NumPy < 2.0 (compatibility requirement)
- Plotly 5.17+
- SQLAlchemy 2.0+

### System Requirements
- 4GB+ RAM recommended
- 1GB+ disk space for data warehouse
- Modern web browser for dashboard

## 📈 Data Flow

1. **Extract**: Load data from source databases
2. **Transform**: Clean, validate, and enrich data
3. **Load**: Populate unified data warehouse
4. **Analyze**: Generate insights and aggregations
5. **Visualize**: Present data through interactive dashboard

## 🛡️ Security & Compliance

- **Data Privacy**: No personal information stored
- **Risk Assessment**: Automated suspicious activity detection
- **Audit Trail**: Complete transaction lineage
- **Access Control**: Dashboard-based data access

## 🔍 Troubleshooting

### Common Issues

**NumPy Compatibility Error**
```bash
conda install "numpy<2" -y
```

**Database Connection Issues**
```bash
python check_database_schema.py
```

**Missing Data**
```bash
python schema_matched_etl.py
```

### Support
- Check `test_environment.py` for environment issues
- Validate database with `check_database_schema.py`
- Review logs in ETL pipeline output

## 📝 License

This project is for educational and research purposes.
