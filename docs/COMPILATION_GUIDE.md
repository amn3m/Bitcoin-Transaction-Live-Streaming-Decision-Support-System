# LaTeX Compilation Guide for Bitcoin DSS Documentation

## 📄 Available Documents

### 1. **Complete LaTeX Document**
- **File**: `methodology_and_results.tex`
- **Description**: Full academic-quality document with advanced formatting
- **Pages**: ~15 pages when compiled
- **Features**: Professional tables, code listings, cross-references, bibliography

### 2. **Simplified LaTeX Document**
- **File**: `methodology_and_results_simple.tex`
- **Description**: Streamlined version for easier compilation
- **Pages**: ~12 pages when compiled
- **Features**: Basic formatting, essential content, minimal dependencies

### 3. **Markdown Version**
- **File**: `methodology_and_results.md`
- **Description**: Immediate viewing without LaTeX compilation
- **Format**: GitHub-compatible Markdown
- **Features**: Tables, code blocks, complete content

## 🔧 LaTeX Compilation Options

### Option 1: Online LaTeX Editor (Recommended) ⭐

#### Overleaf (Free)
1. Go to [https://www.overleaf.com/](https://www.overleaf.com/)
2. Create free account
3. Click "New Project" → "Upload Project"
4. Upload the `.tex` and `.bib` files
5. Click "Recompile" to generate PDF
6. Download PDF when compilation completes

#### Other Online Editors
- **ShareLaTeX**: [https://www.sharelatex.com/](https://www.sharelatex.com/)
- **Papeeria**: [https://papeeria.com/](https://papeeria.com/)
- **LaTeX Base**: [https://latexbase.com/](https://latexbase.com/)

### Option 2: Local LaTeX Installation

#### Windows - MiKTeX
```bash
# Download and install MiKTeX from https://miktex.org/
# Then compile:
cd docs
pdflatex methodology_and_results_simple.tex
pdflatex methodology_and_results_simple.tex  # Second pass for references
```

#### Mac - MacTeX
```bash
# Download and install MacTeX from https://www.tug.org/mactex/
# Then compile:
cd docs
pdflatex methodology_and_results_simple.tex
pdflatex methodology_and_results_simple.tex
```

#### Linux - TeX Live
```bash
# Install TeX Live
sudo apt-get install texlive-full  # Ubuntu/Debian
# or
sudo yum install texlive-scheme-full  # CentOS/RHEL

# Compile
cd docs
pdflatex methodology_and_results_simple.tex
pdflatex methodology_and_results_simple.tex
```

### Option 3: Automated Compilation Script

```bash
# Run the provided Python script
python docs/compile_latex.py

# This script will:
# 1. Check for LaTeX installation
# 2. Create simplified version if needed
# 3. Compile documents automatically
# 4. Clean up auxiliary files
```

## 📋 Compilation Steps (Manual)

### Basic Compilation
```bash
# Navigate to docs folder
cd docs

# Compile LaTeX to PDF
pdflatex methodology_and_results_simple.tex

# Second pass for cross-references and table of contents
pdflatex methodology_and_results_simple.tex
```

### With Bibliography (if using references)
```bash
# First LaTeX pass
pdflatex methodology_and_results.tex

# Process bibliography
bibtex methodology_and_results

# Second LaTeX pass
pdflatex methodology_and_results.tex

# Final pass
pdflatex methodology_and_results.tex
```

## 🛠️ Required LaTeX Packages

### Essential Packages (included in simplified version)
- `inputenc` - Input encoding support
- `amsmath` - Mathematical typesetting
- `graphicx` - Graphics inclusion
- `booktabs` - Professional tables
- `geometry` - Page layout control
- `hyperref` - Hyperlinks and bookmarks
- `listings` - Code syntax highlighting
- `xcolor` - Color support

### Additional Packages (full version)
- `amsfonts, amssymb` - Extended math symbols
- `longtable` - Multi-page tables
- `float` - Float positioning
- `subcaption` - Subfigures and subcaptions
- `enumitem` - Enhanced list formatting

## 🎯 Expected Output

### PDF Features
- **Professional Typography**: High-quality typesetting
- **Bookmarks**: Automatic navigation structure
- **Hyperlinks**: Clickable cross-references and URLs
- **Tables**: Professional formatting with booktabs
- **Code Listings**: Syntax-highlighted code blocks
- **Bibliography**: Academic-style references (if included)

### Document Structure
1. **Title Page**: Project title and metadata
2. **Abstract**: Executive summary
3. **Table of Contents**: Automatic generation
4. **Main Content**: 6 major sections
5. **Conclusion**: Summary and future work
6. **References**: Bibliography (if included)

## 🔍 Troubleshooting

### Common Issues and Solutions

#### "Package not found" errors
```bash
# For MiKTeX (Windows)
# Packages install automatically on first use

# For TeX Live (Linux/Mac)
sudo tlmgr install <package-name>
```

#### Compilation errors
1. **Check log file**: Look at `.log` file for detailed errors
2. **Try simplified version**: Use `methodology_and_results_simple.tex`
3. **Online compilation**: Use Overleaf for guaranteed compatibility

#### Font issues
- Use standard fonts (Computer Modern, Times, etc.)
- Avoid system-specific fonts
- Consider using `lualatex` or `xelatex` for advanced fonts

#### Bibliography issues
- Ensure `.bib` file is in same directory
- Run `bibtex` between LaTeX compilations
- Check BibTeX syntax in references

### Getting Help
1. **LaTeX Documentation**: [https://www.latex-project.org/help/documentation/](https://www.latex-project.org/help/documentation/)
2. **Stack Overflow**: Search "latex" tag for specific issues
3. **Overleaf Documentation**: [https://www.overleaf.com/learn](https://www.overleaf.com/learn)
4. **TeX Stack Exchange**: [https://tex.stackexchange.com/](https://tex.stackexchange.com/)

## 📱 Alternative Formats

### Convert to Other Formats

#### Markdown to PDF (using Pandoc)
```bash
# Install Pandoc: https://pandoc.org/installing.html
pandoc methodology_and_results.md -o methodology_and_results.pdf
```

#### LaTeX to HTML
```bash
# Using htlatex
htlatex methodology_and_results_simple.tex

# Using pandoc
pandoc methodology_and_results.tex -o methodology_and_results.html
```

#### LaTeX to Word
```bash
# Using pandoc
pandoc methodology_and_results.tex -o methodology_and_results.docx
```

## 🎉 Final Recommendations

### For Immediate Use
1. **View Markdown version**: `methodology_and_results.md` (no compilation needed)
2. **Use Overleaf**: Upload `.tex` files for instant PDF generation
3. **Try simplified version**: `methodology_and_results_simple.tex` compiles easier

### For Best Quality
1. **Use full LaTeX version**: `methodology_and_results.tex`
2. **Local LaTeX installation**: Better control and faster compilation
3. **Include bibliography**: Add citations for academic use

### For Sharing
1. **PDF format**: Universal compatibility
2. **High resolution**: Suitable for printing
3. **Bookmarks enabled**: Easy navigation
4. **Hyperlinks active**: Clickable references

---

**Note**: The Markdown version (`methodology_and_results.md`) contains the complete content and can be viewed immediately without any compilation. The LaTeX versions provide professional academic formatting for formal documentation or publication.
