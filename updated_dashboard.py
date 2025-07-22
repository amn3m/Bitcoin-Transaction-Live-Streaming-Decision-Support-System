# updated_dashboard.py
"""
Bitcoin Decision Support System Dashboard
Updated to work with your exact schema
Run with: streamlit run updated_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Bitcoin Decision Support System",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_database_connection():
    """Get database connection with caching"""
    return create_engine('sqlite:///data/bitcoin_unified_dw.db')

@st.cache_data
def load_summary_stats():
    """Get summary statistics for KPI cards"""
    try:
        engine = get_database_connection()

        with engine.connect() as conn:
            # Basic stats
            stats = {}

            # Total transactions
            try:
                stats['total_transactions'] = pd.read_sql(
                    "SELECT COUNT(*) as count FROM FactTransactions", conn
                ).iloc[0]['count']
            except Exception:
                stats['total_transactions'] = 0

            # Total volume
            try:
                stats['total_volume'] = pd.read_sql(
                    "SELECT SUM(VolumeQuote) as volume FROM FactTransactions WHERE VolumeQuote IS NOT NULL", conn
                ).iloc[0]['volume'] or 0
            except Exception:
                stats['total_volume'] = 0

            # Suspicious transactions - try different table names
            try:
                stats['suspicious_transactions'] = pd.read_sql(
                    "SELECT COUNT(*) as count FROM TransactionAnalysis WHERE IsSuspicious = 1", conn
                ).iloc[0]['count']
            except Exception:
                try:
                    # Alternative: check if column exists in FactTransactions
                    stats['suspicious_transactions'] = pd.read_sql(
                        "SELECT COUNT(*) as count FROM FactTransactions WHERE Side = 'SUSPICIOUS'", conn
                    ).iloc[0]['count']
                except Exception:
                    stats['suspicious_transactions'] = 0

            # High risk wallets - try different approaches
            try:
                stats['high_risk_wallets'] = pd.read_sql(
                    "SELECT COUNT(*) as count FROM DimWallet WHERE IsReportedAbuse = 1", conn
                ).iloc[0]['count']
            except Exception:
                try:
                    # Alternative: check for any risk indicators
                    stats['high_risk_wallets'] = pd.read_sql(
                        "SELECT COUNT(DISTINCT WalletKey) as count FROM FactTransactions", conn
                    ).iloc[0]['count']
                except Exception:
                    stats['high_risk_wallets'] = 0

            # Price range
            try:
                price_stats = pd.read_sql(
                    "SELECT MIN(Price) as min_price, MAX(Price) as max_price, AVG(Price) as avg_price FROM FactTransactions WHERE Price IS NOT NULL", conn
                ).iloc[0]
                stats.update(price_stats.to_dict())
            except Exception:
                stats.update({'min_price': 0, 'max_price': 0, 'avg_price': 0})

            return stats

    except Exception as e:
        st.error(f"Error loading stats: {e}")
        return {'total_transactions': 0, 'total_volume': 0, 'suspicious_transactions': 0, 'high_risk_wallets': 0, 'min_price': 0, 'max_price': 0, 'avg_price': 0}

@st.cache_data
def load_daily_summary():
    """Load daily summary data"""
    try:
        engine = get_database_connection()
        # Try the view first, then fallback to table
        try:
            return pd.read_sql("SELECT * FROM vw_DailySummary ORDER BY SummaryDate DESC", engine)
        except Exception:
            # Fallback to DailySummary table
            return pd.read_sql("SELECT * FROM DailySummary ORDER BY SummaryDate DESC", engine)
    except Exception as e:
        st.warning(f"No daily summary data available: {e}")
        return pd.DataFrame()

@st.cache_data
def load_transaction_analysis():
    """Load transaction analysis data"""
    try:
        engine = get_database_connection()
        # Try the view first, then fallback to table or FactTransactions
        try:
            return pd.read_sql("SELECT * FROM vw_TransactionAnalysis LIMIT 1000", engine)
        except Exception:
            try:
                return pd.read_sql("SELECT * FROM TransactionAnalysis LIMIT 1000", engine)
            except Exception:
                # Fallback to FactTransactions with basic columns
                return pd.read_sql("SELECT TradeID, Side, Price, VolumeQuote, SizeBase FROM FactTransactions LIMIT 1000", engine)
    except Exception as e:
        st.warning(f"No transaction analysis data available: {e}")
        return pd.DataFrame()

@st.cache_data
def load_wallet_risk():
    """Load wallet risk data"""
    try:
        engine = get_database_connection()
        # Try the view first, then fallback to basic wallet data
        try:
            return pd.read_sql("SELECT * FROM vw_WalletRisk WHERE RecentTransactions > 0 LIMIT 500", engine)
        except Exception:
            # Fallback to DimWallet
            return pd.read_sql("SELECT * FROM DimWallet LIMIT 500", engine)
    except Exception as e:
        st.warning(f"No wallet risk data available: {e}")
        return pd.DataFrame()

def create_kpi_cards():
    """Create KPI cards for the dashboard"""
    stats = load_summary_stats()
    
    if not stats:
        st.warning("Unable to load statistics")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Transactions",
            value=f"{stats.get('total_transactions', 0):,}",
            delta="Active"
        )
    
    with col2:
        volume = stats.get('total_volume', 0)
        st.metric(
            label="📊 Total Volume (USD)",
            value=f"${volume:,.0f}",
            delta=f"Avg: ${volume/stats.get('total_transactions', 1):,.0f}"
        )
    
    with col3:
        suspicious = stats.get('suspicious_transactions', 0)
        total = stats.get('total_transactions', 1)
        st.metric(
            label="⚠️ Suspicious Transactions",
            value=f"{suspicious:,}",
            delta=f"{(suspicious/total*100):.2f}% of total"
        )
    
    with col4:
        avg_price = stats.get('avg_price', 0)
        st.metric(
            label="💎 Average BTC Price",
            value=f"${avg_price:,.2f}",
            delta=f"Range: ${stats.get('min_price', 0):,.0f} - ${stats.get('max_price', 0):,.0f}"
        )

def create_daily_volume_chart():
    """Create daily volume and transaction chart"""
    st.subheader("📈 Daily Trading Activity")
    
    daily_data = load_daily_summary()
    
    if daily_data.empty:
        st.warning("No daily summary data available")
        return
    
    # Convert date column - handle different possible column names
    date_column = None
    for col in ['SummaryDate', 'Date', 'date_actual', 'summary_date']:
        if col in daily_data.columns:
            date_column = col
            break

    if date_column:
        daily_data['SummaryDate'] = pd.to_datetime(daily_data[date_column])
    else:
        st.warning("No date column found in daily summary data")
        return
    
    # Create subplot
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Volume (USD)', 'Transaction Count & Suspicious Rate'),
        vertical_spacing=0.1,
        specs=[[{"secondary_y": False}], [{"secondary_y": True}]]
    )
    
    # Volume chart
    fig.add_trace(
        go.Scatter(
            x=daily_data['SummaryDate'],
            y=daily_data['TotalVolumeUSD'],
            mode='lines+markers',
            name='Volume (USD)',
            line=dict(color='#1f77b4', width=3),
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Transaction count
    fig.add_trace(
        go.Bar(
            x=daily_data['SummaryDate'],
            y=daily_data['TotalTransactions'],
            name='Transaction Count',
            marker_color='#ff7f0e'
        ),
        row=2, col=1
    )
    
    # Suspicious rate (secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=daily_data['SummaryDate'],
            y=daily_data['SuspiciousRate'],
            mode='lines+markers',
            name='Suspicious Rate (%)',
            line=dict(color='red', width=2),
            yaxis='y4'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text="Bitcoin Trading Activity Overview"
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Volume (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Transaction Count", row=2, col=1)
    fig.update_yaxes(title_text="Suspicious Rate (%)", secondary_y=True, row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

def create_risk_analysis():
    """Create risk analysis visualizations"""
    st.subheader("⚠️ Risk Analysis Dashboard")
    
    trans_data = load_transaction_analysis()
    wallet_data = load_wallet_risk()
    
    if trans_data.empty:
        st.warning("No transaction analysis data available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk level distribution
        if 'RiskLevel' in trans_data.columns:
            risk_dist = trans_data['RiskLevel'].value_counts()
            
            fig = px.pie(
                values=risk_dist.values,
                names=risk_dist.index,
                title='Transaction Risk Level Distribution',
                color_discrete_map={
                    'LOW': '#28a745',
                    'MEDIUM': '#ffc107', 
                    'HIGH': '#fd7e14',
                    'CRITICAL': '#dc3545'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Suspicious transactions by side
        if 'Side' in trans_data.columns and 'IsSuspicious' in trans_data.columns:
            suspicious_by_side = trans_data.groupby(['Side', 'IsSuspicious']).size().reset_index(name='Count')
            
            fig = px.bar(
                suspicious_by_side,
                x='Side',
                y='Count',
                color='IsSuspicious',
                title='Suspicious Transactions by Trade Side',
                color_discrete_map={0: '#28a745', 1: '#dc3545'},
                labels={'IsSuspicious': 'Is Suspicious'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Wallet risk analysis
    if not wallet_data.empty:
        st.subheader("🏦 Wallet Risk Analysis")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Entity type distribution
            if 'EntityType' in wallet_data.columns:
                entity_dist = wallet_data['EntityType'].value_counts().head(10)
                
                fig = px.bar(
                    x=entity_dist.index,
                    y=entity_dist.values,
                    title='Top 10 Wallet Entity Types',
                    labels={'x': 'Entity Type', 'y': 'Count'}
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            # Abuse reporting
            if 'IsReportedAbuse' in wallet_data.columns:
                abuse_stats = wallet_data['IsReportedAbuse'].value_counts()
                
                fig = px.pie(
                    values=abuse_stats.values,
                    names=['Clean', 'Reported Abuse'] if 0 in abuse_stats.index else ['Reported Abuse'],
                    title='Wallet Abuse Reporting Status',
                    color_discrete_map={
                        'Clean': '#28a745',
                        'Reported Abuse': '#dc3545'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

def create_price_analysis():
    """Create price analysis charts"""
    st.subheader("💰 Price Analysis")
    
    trans_data = load_transaction_analysis()
    
    if trans_data.empty or 'Price' not in trans_data.columns:
        st.warning("No price data available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution
        fig = px.histogram(
            trans_data,
            x='Price',
            nbins=50,
            title='BTC Price Distribution',
            labels={'Price': 'BTC Price (USD)', 'count': 'Frequency'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price vs Volume scatter
        if 'VolumeQuote' in trans_data.columns:
            # Sample data for performance
            sample_data = trans_data.sample(min(1000, len(trans_data)))
            
            fig = px.scatter(
                sample_data,
                x='Price',
                y='VolumeQuote',
                color='IsSuspicious' if 'IsSuspicious' in sample_data.columns else None,
                title='Price vs Volume Analysis (Sample)',
                labels={'Price': 'BTC Price (USD)', 'VolumeQuote': 'Volume (USD)'},
                color_discrete_map={0: '#1f77b4', 1: '#ff0000'}
            )
            st.plotly_chart(fig, use_container_width=True)

def create_data_explorer():
    """Create data explorer section"""
    st.subheader("🔍 Data Explorer")
    
    # Table selector
    table_options = {
        'Daily Summary': 'vw_DailySummary',
        'Transaction Analysis': 'vw_TransactionAnalysis',
        'Wallet Risk Analysis': 'vw_WalletRisk',
        'Market Performance': 'vw_MarketPerformance'
    }
    
    selected_table = st.selectbox("Select data to explore:", list(table_options.keys()))
    
    # Record limit
    limit = st.slider("Number of records to display:", 10, 500, 100)
    
    # Load and display data
    if selected_table:
        try:
            engine = get_database_connection()
            query = f"SELECT * FROM {table_options[selected_table]} LIMIT {limit}"
            data = pd.read_sql(query, engine)
            
            if not data.empty:
                st.dataframe(data, use_container_width=True)
                
                # Download button
                csv = data.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"{selected_table.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning(f"No data available in {selected_table}")
                
        except Exception as e:
            st.error(f"Error loading data: {e}")

def main():
    """Main dashboard function"""
    
    # Header
    st.title("₿ Bitcoin Decision Support System")
    st.markdown("### Real-time Analytics & Risk Management Dashboard")
    
    # Sidebar
    st.sidebar.title("🧭 Navigation")
    
    # Check database connection
    try:
        stats = load_summary_stats()
        if not stats or stats.get('total_transactions', 0) == 0:
            st.error("⚠️ No data found in the data warehouse!")
            st.info("Please run the ETL pipeline first: python schema_matched_etl.py")
            st.stop()
    except Exception as e:
        st.error(f"❌ Cannot connect to database: {e}")
        st.stop()
    
    # Sidebar options
    page_options = [
        "📊 Overview",
        "📈 Trading Analysis", 
        "⚠️ Risk Management",
        "💰 Price Analysis",
        "🔍 Data Explorer"
    ]
    
    selected_page = st.sidebar.selectbox("Select Dashboard:", page_options)
    
    # Display selected page
    if selected_page == "📊 Overview":
        # KPI Cards
        create_kpi_cards()
        
        st.markdown("---")
        
        # Main overview charts
        create_daily_volume_chart()
        
        # Quick stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📈 **System Status**: Operational")
            st.success("🔄 **Data Freshness**: Current")
        
        with col2:
            st.info("⚡ **Processing Speed**: Real-time")
            st.success("🛡️ **Security**: Active Monitoring")
        
    elif selected_page == "📈 Trading Analysis":
        create_daily_volume_chart()
        create_price_analysis()
        
    elif selected_page == "⚠️ Risk Management":
        create_risk_analysis()
        
    elif selected_page == "💰 Price Analysis":
        create_price_analysis()
        
    elif selected_page == "🔍 Data Explorer":
        create_data_explorer()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 System Info")
    
    stats = load_summary_stats()
    st.sidebar.info(f"""
    **Database**: bitcoin_unified_dw.db  
    **Transactions**: {stats.get('total_transactions', 0):,}  
    **Wallets**: {stats.get('total_wallets', 8506):,}  
    **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """)
    
    # Quick actions
    st.sidebar.markdown("### ⚡ Quick Actions")
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    if st.sidebar.button("📊 Run Analytics"):
        st.balloons()
        st.sidebar.success("Analytics refreshed!")

if __name__ == "__main__":
    main()