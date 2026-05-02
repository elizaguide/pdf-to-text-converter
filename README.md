# PDF to Text Converter

A simple, reliable tool for converting PDFs to readable text with support for multiple extraction methods and proper handling of edge cases.

## Features

✅ **Multiple Extraction Methods**
- **pdfplumber** - Best for most PDFs with layout preservation
- **PyPDF2** - Fast fallback for text-based PDFs
- **OCR** - Automatic fallback for scanned PDFs (optional)

✅ **Smart Fallback Chain**
- Tries best method first, automatically falls back if needed
- Detects and reports which extraction method was used

✅ **Text Cleaning**
- Removes encoding artifacts and control characters
- Normalizes unicode spaces
- Removes excessive blank lines
- Preserves document structure

✅ **Batch Processing**
- Convert single PDF or multiple files at once
- Flexible output options (stdout, file, directory)

✅ **Simple CLI**
- Easy command-line interface
- Clear progress logging
- Verbose mode for debugging

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/mindvalley/pdf-text-converter.git
cd pdf-text-converter

# Install dependencies (basic - includes pdfplumber + PyPDF2)
pip install -r requirements.txt

# Optional: Install OCR support for scanned PDFs
pip install pdf2image pytesseract
```

### Manual Setup

```bash
# Install core dependencies
pip install PyPDF2 pdfplumber

# Optional: OCR for scanned PDFs
pip install pdf2image pytesseract
```

## Usage

### Basic Conversion

```bash
# Print extracted text to stdout
python3 pdf2text input.pdf

# Save to file
python3 pdf2text input.pdf -o output.txt

# Verbose output (see extraction details)
python3 pdf2text input.pdf -o output.txt -v
```

### Batch Processing

```bash
# Convert multiple PDFs to a directory
python3 pdf2text document1.pdf document2.pdf -o output/

# Convert all PDFs in current directory
python3 pdf2text *.pdf -o output/

# With verbose output
python3 pdf2text *.pdf -o output/ -v
```

### From Python

```python
from src.pdf_converter import PDFConverter

# Create converter instance
converter = PDFConverter(verbose=True)

# Convert single file
text, method = converter.convert_file('input.pdf', 'output.txt')
print(f"Extracted {len(text)} characters using {method}")

# Just get the text without saving
text, method = converter.convert_file('input.pdf')
print(text)
```

## Examples

### Example 1: Simple Conversion

```bash
$ python3 pdf2text research.pdf -o research.txt
2026-05-02 03:15:22,123 - INFO - Converting: research.pdf
2026-05-02 03:15:22,456 - INFO - ✅ Extracted via pdfplumber (45382 chars)
2026-05-02 03:15:22,789 - INFO - ✅ Written to: research.txt
```

### Example 2: Batch Processing

```bash
$ python3 pdf2text *.pdf -o converted/ -v
2026-05-02 03:16:00,123 - INFO - Available PDF libraries:
2026-05-02 03:16:00,124 - INFO -   PyPDF2: True
2026-05-02 03:16:00,125 - INFO -   pdfplumber: True
2026-05-02 03:16:00,126 - INFO -   OCR: False
Converting: document1.pdf
  Page 1: 2841 chars
  Page 2: 3152 chars
✅ Done: document1.pdf (via pdfplumber)
Converting: document2.pdf
  Page 1: 1923 chars
✅ Done: document2.pdf (via PyPDF2)
```

### Example 3: Programmatic Usage

```python
from src.pdf_converter import PDFConverter

converter = PDFConverter(verbose=True)

# Convert with detailed output
text, method = converter.convert_file(
    'analysis.pdf',
    'analysis.txt'
)

print(f"Method used: {method}")
print(f"Text length: {len(text)} characters")
print(f"Preview: {text[:200]}...")
```

## Extraction Methods

### 1. pdfplumber (Preferred)
- **Best for:** Most modern PDFs with structured text
- **Pros:** Preserves layout, handles tables well, very reliable
- **Speed:** Fast

### 2. PyPDF2 (Fallback)
- **Best for:** Text-based PDFs when pdfplumber has issues
- **Pros:** Lightweight, reliable, good for simple PDFs
- **Speed:** Very fast

### 3. OCR (Last Resort)
- **Best for:** Scanned PDFs with images instead of text
- **Pros:** Can extract from images, very flexible
- **Speed:** Slow (requires image processing)
- **Note:** Optional, requires additional installation

## Troubleshooting

### "ImportError: No module named 'pdfplumber'"
Install the required libraries:
```bash
pip install -r requirements.txt
```

### Text extraction is empty or garbled
1. Try with verbose mode to see which method was used
2. Check if PDF is encrypted or corrupted
3. Try the `-v` flag to see detailed extraction info
4. For scanned PDFs, install OCR: `pip install pdf2image pytesseract`

### PDF with mixed content (text + images)
The converter will:
1. Try pdfplumber first (handles mixed content well)
2. Fall back to PyPDF2 if needed
3. Use OCR as last resort if text extraction fails

### Unicode/Encoding Issues
The converter automatically:
- Removes control characters
- Normalizes unicode spaces
- Handles encoding artifacts
- Returns clean UTF-8 text

## Performance

Typical conversion times:
- **Simple PDFs (< 10 pages):** < 100ms
- **Medium PDFs (10-50 pages):** 100-500ms
- **Large PDFs (> 100 pages):** 500ms-2s
- **Scanned PDFs (with OCR):** 1-5 seconds per page

## Architecture

```
pdf-text-converter/
├── src/
│   └── pdf_converter.py       # Main converter class
├── tests/
│   └── test_converter.py      # Unit tests
├── pdf2text                   # CLI wrapper
├── requirements.txt           # Dependencies
├── README.md                  # This file
└── samples/                   # Sample PDFs for testing
```

## Development

### Run Tests

```bash
python3 -m pytest tests/ -v
```

### Add New Features

1. Extend `PDFConverter` class
2. Add new extraction method
3. Update `convert_file()` logic
4. Add tests
5. Update documentation

## Common Tasks

### Make CLI Executable

```bash
chmod +x pdf2text
./pdf2text input.pdf
```

### Add to PATH

```bash
export PATH="$PATH:$(pwd)"
pdf2text input.pdf
```

### Install Locally

```bash
pip install -e .
pdf2text input.pdf
```

## Contributing

1. Test with your PDFs
2. Report issues with sample PDFs
3. Submit improvements
4. Keep it simple and focused

## License

MIT License - Simple and reliable PDF to text conversion tool

## Support

For issues or questions:
1. Check README troubleshooting section
2. Run with `-v` flag for verbose output
3. Check PDF file integrity
4. Verify all dependencies are installed

## Version History

- **v1.0.0** - Initial release
  - pdfplumber extraction
  - PyPDF2 fallback
  - OCR support
  - Text cleaning
  - CLI interface
  - Batch processing

---

**Built with ❤️ for fast, reliable PDF text extraction**
