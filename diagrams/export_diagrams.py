#!/usr/bin/env python3
"""
Export diagrams to various formats
Requires: pip install playwright
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import playwright
        print("✅ Playwright is available")
        return True
    except ImportError:
        print("❌ Playwright not found")
        print("Install with: pip install playwright")
        print("Then run: playwright install")
        return False

def create_html_for_export(mermaid_file, output_html):
    """Create HTML file for diagram export"""
    
    # Read mermaid content
    with open(mermaid_file, 'r', encoding='utf-8') as f:
        mermaid_content = f.read()
    
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: white;
        }}
        .mermaid {{
            text-align: center;
            background: white;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_content}
    </div>
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#3498db',
                primaryTextColor: '#2c3e50',
                primaryBorderColor: '#2980b9',
                lineColor: '#34495e'
            }}
        }});
    </script>
</body>
</html>"""
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)

def export_to_image(html_file, output_file, format='png'):
    """Export HTML to image using Playwright"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Load the HTML file
            page.goto(f"file://{os.path.abspath(html_file)}")
            
            # Wait for mermaid to render
            page.wait_for_timeout(3000)
            
            if format.lower() == 'png':
                # Screenshot the entire page
                page.screenshot(path=output_file, full_page=True)
            elif format.lower() == 'pdf':
                # Export as PDF
                page.pdf(path=output_file, format='A4', print_background=True)
            
            browser.close()
            print(f"✅ Exported: {output_file}")
            
    except Exception as e:
        print(f"❌ Export failed: {e}")

def export_all_diagrams():
    """Export all diagrams to PNG and PDF"""

    print("🎨 EXPORTING DIAGRAMS")
    print("=" * 30)

    # Check current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")

    # List available files
    mmd_files = [f for f in os.listdir('.') if f.endswith('.mmd')]
    print(f"📋 Found .mmd files: {mmd_files}")

    if not mmd_files:
        print("❌ No .mmd files found in current directory")
        print("💡 Make sure you're running this script from the diagrams/ folder")
        return False

    if not check_requirements():
        print("⚠️ Playwright not available, skipping automated export")
        print("💡 Use manual export methods instead")
        return False

    diagrams = [
        ('database_schema.mmd', 'Database Schema'),
        ('system_architecture.mmd', 'System Architecture'),
        ('data_flow.mmd', 'Data Flow Process')
    ]

    # Create exports directory
    exports_dir = Path('exports')
    exports_dir.mkdir(exist_ok=True)
    print(f"📁 Created exports directory: {exports_dir.absolute()}")

    success_count = 0

    for mermaid_file, title in diagrams:
        if not os.path.exists(mermaid_file):
            print(f"❌ File not found: {mermaid_file}")
            continue

        print(f"\n📊 Processing: {title}")

        # Create temporary HTML file
        base_name = Path(mermaid_file).stem
        temp_html = f"temp_{base_name}.html"

        try:
            # Create HTML for export
            print(f"   🔧 Creating HTML: {temp_html}")
            create_html_for_export(mermaid_file, temp_html)

            # Export to PNG
            png_output = exports_dir / f"{base_name}.png"
            print(f"   📸 Exporting PNG: {png_output}")
            export_to_image(temp_html, str(png_output), 'png')

            # Export to PDF
            pdf_output = exports_dir / f"{base_name}.pdf"
            print(f"   📄 Exporting PDF: {pdf_output}")
            export_to_image(temp_html, str(pdf_output), 'pdf')

            # Clean up temp file
            if os.path.exists(temp_html):
                os.remove(temp_html)
                print(f"   🧹 Cleaned up: {temp_html}")

            success_count += 1

        except Exception as e:
            print(f"❌ Error processing {mermaid_file}: {e}")
            print(f"   Error type: {type(e).__name__}")
            if os.path.exists(temp_html):
                try:
                    os.remove(temp_html)
                    print(f"   🧹 Cleaned up temp file: {temp_html}")
                except:
                    pass

    if success_count > 0:
        print(f"\n🎉 Export complete! {success_count} diagrams exported.")
        print(f"📁 Check the 'exports' folder: {exports_dir.absolute()}")
        return True
    else:
        print(f"\n❌ No diagrams were exported successfully.")
        return False

def create_export_instructions():
    """Create instructions for manual export"""
    
    instructions = """# Diagram Export Instructions

## 📊 Available Export Methods

### Method 1: Online Mermaid Editor (Recommended)
1. Go to https://mermaid.live/
2. Copy content from any .mmd file
3. Paste into the editor
4. Click "Export" button
5. Choose format: PNG, SVG, or PDF

### Method 2: HTML Viewer
1. Open `diagram_viewer.html` in your browser
2. Right-click on any diagram
3. Select "Save image as..." or "Copy image"
4. Or use browser print function for PDF

### Method 3: Command Line (Advanced)
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Export to PNG
mmdc -i database_schema.mmd -o database_schema.png

# Export to SVG
mmdc -i system_architecture.mmd -o system_architecture.svg

# Export to PDF
mmdc -i data_flow.mmd -o data_flow.pdf
```

### Method 4: Python Script (This file)
```bash
# Install requirements
pip install playwright
playwright install

# Run export script
python export_diagrams.py
```

## 📁 Files Available for Export

1. **database_schema.mmd** - Database ER diagram
2. **system_architecture.mmd** - System architecture
3. **data_flow.mmd** - Data flow process
4. **diagram_viewer.html** - Interactive viewer

## 🎨 Recommended Formats

- **PNG**: Best for presentations and documents
- **SVG**: Best for web and scalable graphics
- **PDF**: Best for printing and documentation
- **HTML**: Best for interactive viewing

## 💡 Tips

- Use PNG for high-quality images
- Use SVG for web integration
- Use PDF for documentation
- Adjust browser zoom for different resolutions
"""
    
    with open('EXPORT_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("📋 Created EXPORT_INSTRUCTIONS.md")

def main():
    """Main export function"""
    print("🎨 BITCOIN DSS DIAGRAM EXPORTER")
    print("=" * 40)
    
    # Create export instructions
    create_export_instructions()
    
    # Try automated export
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        export_all_diagrams()
    else:
        print("\n📋 Export options:")
        print("1. Run with --auto flag for automated export")
        print("2. Use diagram_viewer.html for interactive viewing")
        print("3. Check EXPORT_INSTRUCTIONS.md for manual methods")
        print("4. Use online Mermaid editor: https://mermaid.live/")

if __name__ == "__main__":
    main()
