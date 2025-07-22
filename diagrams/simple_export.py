#!/usr/bin/env python3
"""
Simple diagram export utility
Creates HTML files that can be easily exported to images
"""

import os

def create_standalone_html(mermaid_file, output_html):
    """Create a standalone HTML file with embedded Mermaid diagram"""
    
    # Read the mermaid content
    try:
        with open(mermaid_file, 'r', encoding='utf-8') as f:
            mermaid_content = f.read().strip()
    except Exception as e:
        print(f"❌ Error reading {mermaid_file}: {e}")
        return False
    
    # Create HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin DSS - {os.path.basename(mermaid_file)}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            color: #2c3e50;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2em;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0;
            color: #666;
            font-size: 1.1em;
        }}
        
        .diagram-container {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow: auto;
        }}
        
        .mermaid {{
            text-align: center;
            background: white;
        }}
        
        .export-info {{
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: center;
            color: #666;
            max-width: 800px;
        }}
        
        .export-info h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        
        .export-info ul {{
            text-align: left;
            display: inline-block;
        }}
        
        @media print {{
            .export-info {{
                display: none;
            }}
            body {{
                margin: 0;
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>₿ Bitcoin Decision Support System</h1>
        <p>Database Schema & Architecture Diagram</p>
    </div>
    
    <div class="diagram-container">
        <div class="mermaid">
{mermaid_content}
        </div>
    </div>
    
    <div class="export-info">
        <h3>📥 Export Instructions</h3>
        <ul>
            <li><strong>Save as Image:</strong> Right-click on diagram → "Save image as..."</li>
            <li><strong>Print to PDF:</strong> Ctrl+P → "Save as PDF"</li>
            <li><strong>Copy Image:</strong> Right-click on diagram → "Copy image"</li>
            <li><strong>High Quality:</strong> Zoom to 150-200% before saving</li>
        </ul>
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#3498db',
                primaryTextColor: '#2c3e50',
                primaryBorderColor: '#2980b9',
                lineColor: '#34495e',
                secondaryColor: '#ecf0f1',
                tertiaryColor: '#f8f9fa',
                background: '#ffffff',
                mainBkg: '#ffffff',
                secondBkg: '#f8f9fa'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }},
            er: {{
                useMaxWidth: true
            }}
        }});
        
        // Add click handler for better UX
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Mermaid diagram loaded successfully');
        }});
    </script>
</body>
</html>"""
    
    # Write HTML file
    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Created: {output_html}")
        return True
    except Exception as e:
        print(f"❌ Error creating {output_html}: {e}")
        return False

def main():
    """Main function to create exportable HTML files"""
    print("🎨 SIMPLE DIAGRAM EXPORT UTILITY")
    print("=" * 40)
    
    # Define diagrams to process
    diagrams = [
        ('database_schema.mmd', 'Database Schema'),
        ('system_architecture.mmd', 'System Architecture'),
        ('data_flow.mmd', 'Data Flow Process')
    ]
    
    success_count = 0
    
    for mermaid_file, title in diagrams:
        if os.path.exists(mermaid_file):
            print(f"\n📊 Processing: {title}")
            
            # Create output filename
            base_name = os.path.splitext(mermaid_file)[0]
            output_html = f"{base_name}_export.html"
            
            if create_standalone_html(mermaid_file, output_html):
                success_count += 1
                print(f"   📁 Output: {output_html}")
        else:
            print(f"❌ File not found: {mermaid_file}")
    
    print(f"\n🎉 EXPORT COMPLETE")
    print("=" * 20)
    print(f"✅ Successfully created {success_count} HTML export files")
    
    if success_count > 0:
        print(f"\n📋 Next steps:")
        print("1. Open any *_export.html file in your browser")
        print("2. Right-click on the diagram to save as image")
        print("3. Use Ctrl+P to print/save as PDF")
        print("4. Zoom to 150-200% for higher quality exports")
        
        print(f"\n📁 Created files:")
        for mermaid_file, title in diagrams:
            if os.path.exists(mermaid_file):
                base_name = os.path.splitext(mermaid_file)[0]
                output_html = f"{base_name}_export.html"
                if os.path.exists(output_html):
                    print(f"   • {output_html}")

if __name__ == "__main__":
    main()
