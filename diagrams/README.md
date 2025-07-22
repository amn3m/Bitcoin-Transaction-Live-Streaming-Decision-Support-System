# Bitcoin DSS Diagrams Export

This folder contains all the system diagrams in various formats for easy export and sharing.

## 📊 Available Diagrams

### 1. Database Schema (ER Diagram)
- **File**: `database_schema.mmd`
- **Type**: Entity Relationship Diagram
- **Description**: Complete database schema showing tables, columns, relationships, and views

### 2. System Architecture
- **File**: `system_architecture.mmd`
- **Type**: System Architecture Diagram
- **Description**: High-level system components and their interactions

### 3. Data Flow Process
- **File**: `data_flow.mmd`
- **Type**: Process Flow Diagram
- **Description**: End-to-end data flow from sources to user interface

## 🔧 How to Export Diagrams

### Method 1: Online Mermaid Editor
1. Go to [Mermaid Live Editor](https://mermaid.live/)
2. Copy the content from any `.mmd` file
3. Paste into the editor
4. Export as:
   - PNG (high resolution)
   - SVG (vector format)
   - PDF (document format)

### Method 2: VS Code Extension
1. Install "Mermaid Markdown Syntax Highlighting" extension
2. Open any `.mmd` file
3. Use Command Palette: "Mermaid: Export Diagram"
4. Choose format (PNG, SVG, PDF)

### Method 3: Command Line (mermaid-cli)
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

### Method 4: GitHub/GitLab
- GitHub and GitLab automatically render `.mmd` files
- View directly in repository
- Use browser print/save for export

## 📱 Viewing Options

### Desktop Applications
- **Draw.io**: Import Mermaid diagrams
- **Lucidchart**: Supports Mermaid import
- **Visio**: Can import SVG exports

### Online Viewers
- **Mermaid Live**: https://mermaid.live/
- **GitHub**: Direct rendering in repository
- **GitLab**: Direct rendering in repository

## 🎨 Customization

### Color Schemes
Each diagram includes custom styling:
- **Data Sources**: Light blue (#e1f5fe)
- **ETL Pipeline**: Light purple (#f3e5f5)
- **Data Warehouse**: Light green (#e8f5e8)
- **Application Layer**: Light orange (#fff3e0)
- **User Interface**: Light pink (#fce4ec)
- **Utilities**: Light lime (#f1f8e9)

### Modifying Diagrams
1. Edit the `.mmd` files directly
2. Modify colors by changing `classDef` definitions
3. Add/remove components as needed
4. Update relationships and connections

## 📋 Export Formats Comparison

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| PNG | Presentations, Documents | High quality, widely supported | Large file size |
| SVG | Web, Scalable graphics | Vector format, small size | Limited software support |
| PDF | Documentation, Printing | Professional format | Not editable |
| HTML | Interactive viewing | Clickable, responsive | Requires browser |

## 🔗 Integration Options

### Documentation
- Embed in README files
- Include in technical documentation
- Add to project wikis

### Presentations
- Export as PNG for PowerPoint/Keynote
- Use SVG for web presentations
- PDF for printed materials

### Development
- Include in code documentation
- Add to API documentation
- Use in system design documents

## 📞 Support

For diagram modifications or custom exports:
1. Edit the `.mmd` source files
2. Use the Mermaid Live Editor for testing
3. Export in your preferred format
4. Integrate into your documentation workflow
