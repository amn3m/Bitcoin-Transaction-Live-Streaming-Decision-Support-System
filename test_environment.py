#!/usr/bin/env python3
"""
Test environment and dependencies
"""

import sys
import os

def test_basic_imports():
    """Test basic Python imports"""
    print("🧪 TESTING PYTHON ENVIRONMENT")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Test basic imports
    imports_to_test = [
        ('sqlite3', 'SQLite support'),
        ('datetime', 'Date/time support'),
        ('os', 'OS interface'),
        ('sys', 'System interface')
    ]
    
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {module}: {description}")
        except ImportError as e:
            print(f"❌ {module}: {e}")

def test_data_libraries():
    """Test data science libraries"""
    print(f"\n📊 TESTING DATA LIBRARIES")
    print("=" * 30)
    
    # Test numpy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}: Available")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        print("   Try: pip install --force-reinstall numpy")
    
    # Test pandas
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}: Available")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        print("   Try: pip install --force-reinstall pandas")
    
    # Test sqlalchemy
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy {sqlalchemy.__version__}: Available")
    except ImportError as e:
        print(f"❌ SQLAlchemy: {e}")
        print("   Try: pip install sqlalchemy")

def test_visualization_libraries():
    """Test visualization libraries"""
    print(f"\n📈 TESTING VISUALIZATION LIBRARIES")
    print("=" * 40)
    
    # Test plotly
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}: Available")
    except ImportError as e:
        print(f"❌ Plotly: {e}")
        print("   Try: pip install plotly")
    
    # Test streamlit
    try:
        import streamlit as st
        print(f"✅ Streamlit {st.__version__}: Available")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        print("   Try: pip install streamlit")

def test_database_connection():
    """Test database connection"""
    print(f"\n🗄️ TESTING DATABASE CONNECTION")
    print("=" * 35)
    
    try:
        import sqlite3
        
        # Check if database exists
        db_path = 'data/bitcoin_unified_dw.db'
        if os.path.exists(db_path):
            print(f"✅ Database file exists: {db_path}")
            
            # Test connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table count
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            print(f"✅ Database connection successful: {table_count} tables found")
            
            conn.close()
        else:
            print(f"❌ Database file not found: {db_path}")
            print("   Run the ETL script first to create the database")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

def provide_fix_recommendations():
    """Provide fix recommendations"""
    print(f"\n🔧 FIX RECOMMENDATIONS")
    print("=" * 25)
    
    print("If you see NumPy/Pandas errors:")
    print("1. pip uninstall numpy pandas")
    print("2. pip install numpy pandas")
    print("3. Or try: conda install numpy pandas")
    print()
    print("If database is missing:")
    print("1. Run: python schema_matched_etl.py")
    print("2. Or: python inspect_and_fix_data.py")
    print()
    print("To run the dashboard:")
    print("1. Fix environment issues first")
    print("2. streamlit run updated_dashboard.py")

if __name__ == "__main__":
    test_basic_imports()
    test_data_libraries()
    test_visualization_libraries()
    test_database_connection()
    provide_fix_recommendations()
