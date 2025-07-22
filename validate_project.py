#!/usr/bin/env python3
"""
Final project validation script
Ensures all components are working correctly
"""

import os
import sys
import sqlite3
from datetime import datetime

def check_file_structure():
    """Validate project file structure"""
    print("🗂️ CHECKING PROJECT STRUCTURE")
    print("=" * 40)
    
    required_files = [
        'updated_dashboard.py',
        'schema_matched_etl.py',
        'check_database_schema.py',
        'test_environment.py',
        'README.md',
        'PROJECT_SUMMARY.md',
        'schema.sql'
    ]
    
    required_dirs = [
        'data',
        'config',
        'docs',
        'notebooks',
        'src',
        'tests'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/")
            missing_dirs.append(dir)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def check_database():
    """Validate database structure and data"""
    print(f"\n🗄️ CHECKING DATABASE")
    print("=" * 25)
    
    db_path = 'data/bitcoin_unified_dw.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['FactTransactions', 'DimTime', 'DimMarket', 'DimWallet']
        
        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table}: {count:,} records")
            else:
                print(f"❌ {table}: Missing")
                return False
        
        # Check views
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in cursor.fetchall()]
        
        expected_views = ['vw_DailySummary', 'vw_TransactionAnalysis']
        
        for view in expected_views:
            if view in views:
                print(f"✅ {view}: Available")
            else:
                print(f"⚠️ {view}: Missing (optional)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_imports():
    """Test critical imports"""
    print(f"\n📦 CHECKING IMPORTS")
    print("=" * 22)
    
    imports_to_test = [
        ('streamlit', 'Streamlit dashboard framework'),
        ('pandas', 'Data manipulation library'),
        ('plotly.express', 'Visualization library'),
        ('sqlalchemy', 'Database ORM'),
    ]
    
    all_imports_ok = True
    
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {module}: {description}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def check_dashboard_syntax():
    """Check dashboard file for syntax errors"""
    print(f"\n🖥️ CHECKING DASHBOARD SYNTAX")
    print("=" * 32)
    
    try:
        with open('updated_dashboard.py', 'r') as f:
            code = f.read()
        
        compile(code, 'updated_dashboard.py', 'exec')
        print("✅ Dashboard syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking dashboard: {e}")
        return False

def generate_report():
    """Generate final validation report"""
    print(f"\n📋 VALIDATION REPORT")
    print("=" * 25)
    
    checks = [
        ("File Structure", check_file_structure()),
        ("Database", check_database()),
        ("Imports", check_imports()),
        ("Dashboard Syntax", check_dashboard_syntax())
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nResults: {passed}/{total} checks passed")
    
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {check_name}: {status}")
    
    if passed == total:
        print(f"\n🎉 ALL CHECKS PASSED!")
        print("✅ Project is ready for use")
        print(f"\n🚀 Next steps:")
        print("1. streamlit run updated_dashboard.py")
        print("2. Open http://localhost:8501 in your browser")
        print("3. Explore the Bitcoin Decision Support System")
        return True
    else:
        print(f"\n⚠️ {total - passed} checks failed")
        print("❌ Please fix the issues above before proceeding")
        return False

def main():
    """Main validation function"""
    print("🔍 BITCOIN DSS PROJECT VALIDATION")
    print("=" * 45)
    print(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = generate_report()
    
    if success:
        print(f"\n✅ Project validation completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Project validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
