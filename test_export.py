#!/usr/bin/env python3
"""
Simple test script to identify export issues
"""

import os
import sys

def test_basic_functionality():
    """Test basic Python functionality"""
    print("🧪 TESTING BASIC FUNCTIONALITY")
    print("=" * 35)
    
    # Test current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Test file listing
    try:
        files = os.listdir('.')
        print(f"📋 Files in current directory: {len(files)} files")
        
        # Look for diagrams folder
        if 'diagrams' in files:
            print("✅ diagrams/ folder found")
            
            # List diagrams folder contents
            diagram_files = os.listdir('diagrams')
            print(f"📊 Files in diagrams/: {diagram_files}")
            
            # Check for .mmd files
            mmd_files = [f for f in diagram_files if f.endswith('.mmd')]
            print(f"📋 .mmd files found: {mmd_files}")
            
        else:
            print("❌ diagrams/ folder not found")
            
    except Exception as e:
        print(f"❌ Error listing files: {e}")

def test_file_reading():
    """Test reading mermaid files"""
    print(f"\n📖 TESTING FILE READING")
    print("=" * 25)
    
    mmd_files = [
        'diagrams/database_schema.mmd',
        'diagrams/system_architecture.mmd', 
        'diagrams/data_flow.mmd'
    ]
    
    for file_path in mmd_files:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    print(f"✅ {file_path}: {lines} lines, {len(content)} characters")
            else:
                print(f"❌ {file_path}: File not found")
        except Exception as e:
            print(f"❌ {file_path}: Error reading - {e}")

def test_imports():
    """Test required imports"""
    print(f"\n📦 TESTING IMPORTS")
    print("=" * 20)
    
    # Test pathlib
    try:
        from pathlib import Path
        print("✅ pathlib.Path: Available")
    except ImportError as e:
        print(f"❌ pathlib.Path: {e}")
    
    # Test playwright (optional)
    try:
        import playwright
        print("✅ playwright: Available")
    except ImportError:
        print("⚠️ playwright: Not installed (optional for automated export)")

def test_html_creation():
    """Test HTML file creation"""
    print(f"\n🌐 TESTING HTML CREATION")
    print("=" * 27)
    
    test_mermaid = """graph TD
    A[Start] --> B[Process]
    B --> C[End]"""
    
    test_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="mermaid">
{content}
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>""".format(content=test_mermaid)
    
    try:
        test_file = 'test_diagram.html'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_html)
        
        print(f"✅ Created test HTML file: {test_file}")
        
        # Clean up
        os.remove(test_file)
        print("✅ Cleaned up test file")
        
    except Exception as e:
        print(f"❌ HTML creation failed: {e}")

def main():
    """Main test function"""
    print("🔍 EXPORT SCRIPT DIAGNOSTICS")
    print("=" * 35)
    
    test_basic_functionality()
    test_file_reading()
    test_imports()
    test_html_creation()
    
    print(f"\n💡 RECOMMENDATIONS")
    print("=" * 20)
    print("1. If all tests pass, the export script should work")
    print("2. For automated export, install: pip install playwright")
    print("3. For manual export, use: https://mermaid.live/")
    print("4. Or use the HTML viewer: diagrams/diagram_viewer.html")

if __name__ == "__main__":
    main()
