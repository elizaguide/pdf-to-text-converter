# PDF to Text Converter

A simple, reliable Python tool for converting PDF files to clean, readable text.

## Features

- ✅ Extracts text from PDF files with multiple pages
- ✅ Cleans and formats output (removes encoding artifacts, excess whitespace)
- ✅ Handles edge cases gracefully
- ✅ Page breaks marked clearly in output
- ✅ CLI interface for easy command-line usage
- ✅ Verbose mode for debugging
- ✅ Error handling and validation

## Installation

### Requirements
- Python 3.7+
- pip

### Setup

```bash
git clone https://github.com/vishen-lakhiani/pdf-to-text-converter.git
cd pdf-to-text-converter
pip install -r requirements.txt
```

## Usage

### Command Line

**Basic usage (saves to `document.txt`):**
```bash
python pdf_converter.py document.pdf
```

**Specify output file:**
```bash
python pdf_converter.py document.pdf output.txt
```

**Verbose mode (shows progress):**
```bash
python pdf_converter.py -v document.pdf
python pdf_converter.py --verbose document.pdf
```

**Full example:**
```bash
python pdf_converter.py -v my_research.pdf cleaned_text.txt
```

### As a Python Module

```python
from pdf_converter import PDFConverter

# Create converter
converter = PDFConverter(verbose=True)

# Method 1: Get text content
success, content = converter.convert('document.pdf')
if success:
    print(content)
else:
    print(f"Error: {content}")

# Method 2: Save to file
success, message = converter.save_text('document.pdf', 'output.txt')
print(message)
```

## Output

The converter produces clean text with:
- Encoding artifacts removed
- Multiple spaces collapsed to single spaces
- Excessive blank lines cleaned up
- Page breaks marked with `--- PAGE BREAK ---`
- Proper UTF-8 encoding

### Example
```
[Page 1 content]

--- PAGE BREAK ---

[Page 2 content]
```

## Error Handling

The tool handles common issues:
- Missing files
- Invalid PDF format
- Corrupted pages (skipped with warning)
- Encoding issues
- File permission problems

All errors are reported clearly with helpful messages.

## Exit Codes

- `0` = Success
- `1` = Error (check message for details)

## Performance

Typical performance on standard PDFs:
- Small documents (<10 pages): < 1 second
- Medium documents (10-100 pages): 1-5 seconds
- Large documents (100+ pages): 5-30 seconds

## Limitations

- Scanned PDFs (images) won't extract text - use OCR for those
- Complex layout PDFs may have reordered text
- Some PDF-embedded fonts may cause encoding issues

For scanned PDFs, consider using OCR tools like Tesseract or cloud solutions like Google Cloud Vision.

## Development

### Project Structure
```
pdf-to-text-converter/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── pdf_converter.py       # Main converter module
├── test_converter.py      # Test suite
└── .gitignore            # Git ignore rules
```

### Running Tests
```bash
python test_converter.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Created for Vishen Lakhiani

## Support

For issues or feature requests, please create a GitHub issue with:
- PDF file details (size, page count)
- Error message
- Steps to reproduce
- Python version

---

**Built with:** PyPDF2  
**Last Updated:** April 2026  
**Status:** Production Ready ✅
