# 📊 Bitcoin DSS Diagram Export Guide

This guide provides multiple methods to export the Bitcoin Decision Support System diagrams in various formats.

## 🎯 Quick Export Methods

### Method 1: Online Mermaid Editor (Recommended) ⭐
**Best for: High-quality exports in multiple formats**

1. **Go to**: [https://mermaid.live/](https://mermaid.live/)
2. **Copy content** from any `.mmd` file in this folder
3. **Paste** into the editor
4. **Click "Export"** and choose format:
   - PNG (high resolution)
   - SVG (vector graphics)
   - PDF (documents)

### Method 2: HTML Viewer (Current Setup) 🖥️
**Best for: Quick viewing and basic export**

1. **Open**: `diagram_viewer.html` in your browser
2. **Navigate** between diagrams using tabs
3. **Right-click** on any diagram
4. **Select**: "Save image as..." or "Copy image"
5. **For PDF**: Use browser print function (Ctrl+P → Save as PDF)

### Method 3: Simple Export Script 🐍
**Best for: Creating standalone HTML files**

```bash
cd diagrams
python simple_export.py
```

This creates individual HTML files for each diagram that can be easily exported.

## 📁 Available Diagrams

| File | Description | Content |
|------|-------------|---------|
| `database_schema.mmd` | Database ER Diagram | Tables, relationships, views |
| `system_architecture.mmd` | System Architecture | Components, data flow |
| `data_flow.mmd` | Data Flow Process | End-to-end process flow |

## 🎨 Export Formats Comparison

| Format | Best For | Quality | File Size | Editability |
|--------|----------|---------|-----------|-------------|
| **PNG** | Presentations, Documents | High | Large | No |
| **SVG** | Web, Scalable graphics | Vector | Small | Limited |
| **PDF** | Documentation, Printing | High | Medium | No |
| **HTML** | Interactive viewing | Vector | Small | Yes |

## 🔧 Advanced Export Methods

### Method 4: Command Line (mermaid-cli)
**Best for: Automated batch processing**

```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Export individual diagrams
mmdc -i database_schema.mmd -o database_schema.png
mmdc -i system_architecture.mmd -o system_architecture.svg
mmdc -i data_flow.mmd -o data_flow.pdf

# Batch export all diagrams
mmdc -i database_schema.mmd -o exports/database_schema.png
mmdc -i system_architecture.mmd -o exports/system_architecture.png
mmdc -i data_flow.mmd -o exports/data_flow.png
```

### Method 5: VS Code Extension
**Best for: Development workflow**

1. **Install**: "Mermaid Markdown Syntax Highlighting" extension
2. **Open**: any `.mmd` file in VS Code
3. **Command Palette**: Ctrl+Shift+P
4. **Run**: "Mermaid: Export Diagram"
5. **Choose**: PNG, SVG, or PDF

## 📐 Quality Settings

### For High-Quality Exports:
- **Browser zoom**: 150-200% before saving
- **PNG resolution**: Use "Save image as..." not screenshot
- **PDF settings**: Enable "Print backgrounds" option
- **SVG**: Best for scalable graphics

### For Web Use:
- **SVG format**: Smallest file size, scalable
- **Optimize**: Remove unnecessary whitespace
- **Responsive**: SVG adapts to container size

### For Print:
- **PDF format**: Best for documents
- **High DPI**: 300 DPI minimum for printing
- **Page size**: A4 or Letter format

## 🛠️ Troubleshooting

### Common Issues:

**Diagram not rendering:**
- Check internet connection (CDN required)
- Verify Mermaid syntax in `.mmd` files
- Try refreshing the browser

**Export quality poor:**
- Increase browser zoom before export
- Use PNG instead of JPEG
- Try SVG for vector graphics

**File not found errors:**
- Ensure you're in the `diagrams/` folder
- Check file names match exactly
- Verify file permissions

**Script errors:**
- Use manual export methods instead
- Check Python installation
- Try online Mermaid editor

## 📱 Platform-Specific Tips

### Windows:
- Use Edge or Chrome for best rendering
- Right-click → "Save image as..."
- Print to PDF using built-in printer

### Mac:
- Safari or Chrome recommended
- Cmd+Click for context menu
- Use "Export as PDF" in print dialog

### Linux:
- Firefox or Chrome work well
- Use print-to-file for PDF export
- Install mermaid-cli for command line

## 🎯 Recommended Workflow

1. **Quick viewing**: Use `diagram_viewer.html`
2. **High-quality export**: Use [mermaid.live](https://mermaid.live/)
3. **Batch processing**: Use mermaid-cli
4. **Development**: Use VS Code extension

## 📞 Support

If you encounter issues:

1. **Check this guide** for troubleshooting tips
2. **Try alternative methods** listed above
3. **Use online editor** as fallback: https://mermaid.live/
4. **Verify file contents** in `.mmd` files

## 🔗 Useful Links

- **Mermaid Live Editor**: https://mermaid.live/
- **Mermaid Documentation**: https://mermaid-js.github.io/mermaid/
- **Mermaid CLI**: https://github.com/mermaid-js/mermaid-cli
- **VS Code Extension**: Search "Mermaid" in extensions

---

**Note**: All diagrams are created using Mermaid syntax and can be edited by modifying the `.mmd` files directly.
