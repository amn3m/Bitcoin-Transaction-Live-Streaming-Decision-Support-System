#!/usr/bin/env python3
"""
Check database schema and identify issues
"""

import sqlite3
import sys
import os

def check_database_schema():
    """Check the actual database schema"""
    db_path = 'data/bitcoin_unified_dw.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 DATABASE SCHEMA ANALYSIS")
        print("=" * 40)
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tables: {tables}")
        
        # Get all views
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in cursor.fetchall()]
        print(f"👁️ Views: {views}")
        
        # Check specific tables/views the dashboard expects
        expected_objects = {
            'FactTransactions': 'table',
            'DimWallet': 'table', 
            'TransactionAnalysis': 'table',
            'DailySummary': 'table',
            'vw_DailySummary': 'view',
            'vw_TransactionAnalysis': 'view',
            'vw_WalletRisk': 'view',
            'vw_MarketPerformance': 'view'
        }
        
        print(f"\n🎯 CHECKING EXPECTED OBJECTS")
        print("=" * 35)
        
        missing_objects = []
        for obj_name, obj_type in expected_objects.items():
            if obj_type == 'table' and obj_name in tables:
                print(f"✅ {obj_name} (table) - Found")
            elif obj_type == 'view' and obj_name in views:
                print(f"✅ {obj_name} (view) - Found")
            else:
                print(f"❌ {obj_name} ({obj_type}) - Missing")
                missing_objects.append((obj_name, obj_type))
        
        # Check FactTransactions structure
        if 'FactTransactions' in tables:
            print(f"\n📋 FactTransactions Structure:")
            cursor.execute("PRAGMA table_info(FactTransactions)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   {col[1]} ({col[2]})")
        
        # Check data counts
        print(f"\n📈 DATA COUNTS")
        print("=" * 20)
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count:,} records")
            except Exception as e:
                print(f"   {table}: Error - {e}")
        
        for view in views:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {view}")
                count = cursor.fetchone()[0]
                print(f"   {view}: {count:,} records")
            except Exception as e:
                print(f"   {view}: Error - {e}")
        
        conn.close()
        
        if missing_objects:
            print(f"\n⚠️ MISSING OBJECTS FOUND")
            print("=" * 25)
            for obj_name, obj_type in missing_objects:
                print(f"   {obj_name} ({obj_type})")
            return False
        else:
            print(f"\n✅ ALL EXPECTED OBJECTS FOUND")
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    if check_database_schema():
        print(f"\n🎉 Database schema is compatible with dashboard!")
    else:
        print(f"\n⚠️ Database schema issues found. Dashboard may have limited functionality.")
