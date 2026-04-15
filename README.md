# PDF to Text Converter

Simple, reliable tool for converting PDFs to readable text for analysis. Handles multiple PDF formats and edge cases with clean output formatting.

## Features

✅ **Multiple extraction methods** - Uses pdfplumber for best formatting, falls back to PyPDF2 for tricky PDFs  
✅ **Smart text cleaning** - Removes encoding artifacts, control characters, and formatting junk  
✅ **Batch processing** - Convert multiple PDFs at once  
✅ **Flexible output** - Save to file or print to stdout  
✅ **Verbose logging** - Debug mode for troubleshooting edge cases  
✅ **Handles edge cases** - Damaged PDFs, mixed encodings, OCR artifacts  

## Installation

### Option 1: Direct Usage
```bash
cd /Users/vishen/pdf-to-text-converter
python pdf_converter.py your-file.pdf
```

### Option 2: Install as Command
```bash
cd /Users/vishen/pdf-to-text-converter
chmod +x pdf_converter.py
ln -s $(pwd)/pdf_converter.py /usr/local/bin/pdf2txt
pdf2txt your-file.pdf
```

### Option 3: Use in Python
```python
from pdf_converter import PDFConverter

converter = PDFConverter(verbose=True)
text = converter.convert('input.pdf')
print(text)

# Or save to file
converter.convert('input.pdf', output_path='output.txt')
```

## Usage

### Basic Conversion
```bash
python pdf_converter.py input.pdf
```
Output is printed to stdout.

### Save to File
```bash
python pdf_converter.py input.pdf -o output.txt
```

### Multiple Files → Batch Processing
```bash
python pdf_converter.py file1.pdf file2.pdf file3.pdf -o output/
```
Creates `output/file1.txt`, `output/file2.txt`, `output/file3.txt`

### Glob Pattern Support
```bash
python pdf_converter.py "*.pdf" -o output/
```
Converts all PDFs in current directory to `output/`

### Verbose Logging (Debugging)
```bash
python pdf_converter.py input.pdf -v
```
Shows detailed extraction steps and warnings.

## How It Works

1. **Extraction Phase**
   - First tries `pdfplumber` for best-quality text extraction (preserves formatting)
   - Falls back to `PyPDF2` if pdfplumber fails (more reliable for damaged PDFs)

2. **Cleaning Phase**
   - Removes UTF-8 encoding artifacts (BOM, null bytes, etc.)
   - Fixes line spacing and excessive whitespace
   - Removes control characters
   - Normalizes paragraph breaks

3. **Output Phase**
   - Clean, readable text suitable for analysis and processing

## Examples

### Example 1: Analyze a Report
```bash
python pdf_converter.py 2024-Q4-Report.pdf -o report.txt
cat report.txt | grep -i "revenue"
```

### Example 2: Process Multiple Documents
```bash
python pdf_converter.py Documents/*.pdf -o extracted/ -v
# Check what was extracted
ls -la extracted/
```

### Example 3: Use Programmatically
```python
from pdf_converter import PDFConverter

converter = PDFConverter()
for pdf in ['contract.pdf', 'agreement.pdf']:
    text = converter.convert(pdf)
    # Process text
    words = text.split()
    print(f"{pdf}: {len(words)} words")
```

## Troubleshooting

### PDF seems corrupt or extraction fails
- Use verbose mode to see what's happening: `python pdf_converter.py input.pdf -v`
- The tool automatically tries multiple extraction methods
- If both fail, the PDF may be genuinely unreadable

### Text looks garbled
- This is usually encoding artifacts. The cleaning phase removes most of these
- If text is still bad, the PDF might be scanned image-based (needs OCR, not supported yet)

### Performance is slow
- Large PDFs take longer. This is normal.
- pdfplumber is more thorough but slower; PyPDF2 is faster

## Dependencies

- `PyPDF2` - Core PDF reading (required)
- `pdfplumber` - Enhanced formatting extraction (optional, auto-installed)

Both are installed automatically on first run.

## Requirements

- Python 3.7+
- pip (for auto-installation of dependencies)

## License

Simple utility for Vishen's workflow. Use freely.

## Architecture Notes

### Why Two Extraction Methods?

- **pdfplumber**: Better for structured PDFs with tables and formatting
- **PyPDF2**: More robust for damaged/malformed PDFs

The tool tries pdfplumber first (best results) and automatically falls back to PyPDF2 if needed.

### Text Cleaning Strategy

The cleaning phase addresses common PDF extraction issues:
- UTF-8 BOM artifacts (`ï¿½`)
- Null bytes and control characters
- Excessive whitespace and irregular line breaks
- OCR artifacts and encoding junk

This results in clean text suitable for analysis, NLP processing, or search.

### Batch Processing

When processing multiple files:
- Each PDF is processed independently
- Errors in one file don't stop processing of others
- Output directory is created automatically

## Roadmap

Possible future enhancements:
- OCR support for image-based PDFs (tesseract)
- Table extraction and formatting preservation
- Confidence scoring for extraction quality
- Metadata extraction (title, author, creation date)
- Direct output to JSON/CSV formats

---

**Built for reliable PDF analysis. Simple. Effective. Trustworthy.**
