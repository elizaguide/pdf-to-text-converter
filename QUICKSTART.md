# Quick Start Guide

Built in 3 minutes at 3:00 AM on May 2, 2026 🚀

## Installation & First Use

### 1. Clone & Install

```bash
git clone https://github.com/elizaguide/pdf-text-converter.git
cd pdf-text-converter
python3 -m pip install -r requirements.txt
```

### 2. Convert Your First PDF

```bash
# Simple - print to screen
python3 pdf2text document.pdf

# Save to file
python3 pdf2text document.pdf -o output.txt

# Verbose output to see what extraction method was used
python3 pdf2text document.pdf -o output.txt -v
```

### 3. Batch Convert Multiple PDFs

```bash
# Convert all PDFs in a folder to output directory
python3 pdf2text *.pdf -o output/

# Or specify files individually
python3 pdf2text file1.pdf file2.pdf file3.pdf -o output/
```

## Real-World Examples

### Scientific Papers
```bash
python3 pdf2text research_paper.pdf -o paper.txt -v
```
**What happens:** pdfplumber extracts text preserving structure, cleans encoding artifacts, removes excess whitespace

### Scanned Documents
```bash
# Install OCR first: pip install pdf2image pytesseract
python3 pdf2text scanned_document.pdf -o text.txt -v
```
**What happens:** Tries pdfplumber, falls back to PyPDF2, finally uses OCR if needed

### Reports with Mixed Content
```bash
python3 pdf2text annual_report.pdf -o report.txt
```
**What happens:** Automatically selects best extraction method based on PDF content

## Common Use Cases

### Extract Text for Analysis
```bash
python3 pdf2text analysis.pdf | grep "Key Findings"
```

### Convert & View
```bash
python3 pdf2text document.pdf | less
```

### Batch Processing in Scripts
```bash
#!/bin/bash
for pdf in *.pdf; do
    python3 pdf2text "$pdf" -o "text/${pdf%.pdf}.txt"
done
```

## Troubleshooting

### "No module named 'pdfplumber'"
```bash
python3 -m pip install pdfplumber PyPDF2
```

### Empty extraction / Garbled text
```bash
# Use verbose mode to see which method was used
python3 pdf2text problem.pdf -o output.txt -v

# If scanned, install OCR
python3 -m pip install pdf2image pytesseract
```

### Large PDF taking forever
- Conversion is typically < 1 second per 10 pages
- Scanned PDFs (OCR) take longer - a few seconds per page
- This is normal!

## Made With ❤️

Built by Eliza at 3:00 AM on a Saturday (because good tools don't wait for business hours 😎)
