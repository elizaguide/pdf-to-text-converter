# PDF to Text Converter 📄

A simple, reliable Python tool for extracting clean text from PDF files. Handles multiple PDF formats, removes encoding artifacts, and produces readable output for analysis.

## Features ✨

- **Clean Text Output**: Automatically removes encoding artifacts, control characters, and formatting issues
- **Multi-Page Support**: Extracts text from all pages with page break markers
- **Error Handling**: Graceful handling of corrupted PDFs, missing files, and edge cases
- **Verbose Mode**: Optional progress messages for debugging
- **Simple CLI**: Easy-to-use command-line interface
- **No Dependencies**: Uses standard PyPDF2 library

## Installation

### Requirements
- Python 3.7+
- PyPDF2

```bash
pip install PyPDF2
```

### Quick Start

```bash
# Make the CLI executable
chmod +x pdf-converter

# Or run directly with Python
python3 pdf_converter.py
```

## Usage

### Basic Usage

Convert a PDF to text (creates `.txt` file with same name):
```bash
./pdf-converter document.pdf
# Creates: document.txt
```

### Custom Output Path

Specify where to save the text:
```bash
./pdf-converter document.pdf output/extracted_text.txt
```

### Verbose Mode

See progress messages during extraction:
```bash
./pdf-converter -v document.pdf
./pdf-converter --verbose document.pdf output.txt
```

### Python Module

Use as a Python module in your own code:

```python
from pdf_converter import PDFToTextConverter

# Create converter
converter = PDFToTextConverter(verbose=True)

# Option 1: Save to file
success, message = converter.convert_file('input.pdf', 'output.txt')
print(message)

# Option 2: Get text as string
success, text = converter.convert_string('input.pdf')
if success:
    print(text)
else:
    print(f"Error: {text}")
```

## Examples

### Example 1: Simple Document Conversion

```bash
$ ./pdf-converter research.pdf
[PDF Converter] Opening: research.pdf
[PDF Converter] Found 12 pages
[PDF Converter] Extracting page 1/12
[PDF Converter] Extracting page 2/12
...
[PDF Converter] Cleaning text
[PDF Converter] Extraction complete: 45623 characters
✓ Converted: research.pdf → research.txt
```

### Example 2: Batch Processing

```bash
# Convert all PDFs in a directory
for pdf in *.pdf; do
    ./pdf-converter "$pdf" "output/${pdf%.pdf}.txt"
done
```

### Example 3: With Custom Output

```bash
./pdf-converter -v documents/analysis.pdf reports/analysis_text.txt
```

## Text Cleaning

The converter automatically:

1. **Removes Control Characters**: Strips null bytes and invisible characters
2. **Fixes Line Breaks**: Handles hyphenation at line breaks
3. **Normalizes Whitespace**: Converts multiple spaces to single spaces
4. **Cleans Artifacts**: Removes encoding artifacts from OCR/scanning
5. **Preserves Structure**: Maintains paragraph breaks and page separators

### Output Format

- Pages are separated by: `--- Page Break ---`
- Paragraph breaks are preserved
- Trailing whitespace is removed
- Text is UTF-8 encoded

## Error Handling

The converter gracefully handles:

- Missing files
- Non-PDF files
- Corrupted PDFs
- Pages with no extractable text
- File write permissions issues

All errors are clearly reported with actionable messages.

## Performance

- Single-page PDF: ~100ms
- 100-page PDF: ~1-2 seconds
- Text cleaning: <50ms for typical documents

## API Reference

### PDFToTextConverter

```python
converter = PDFToTextConverter(verbose: bool = False)
```

#### Methods

**`extract_from_pdf(pdf_path: str) -> Tuple[str, bool]`**
- Extracts text from PDF
- Returns: (text_or_error, success_flag)

**`convert_file(input_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]`**
- Converts PDF file to text file
- Returns: (success, message)

**`convert_string(pdf_path: str) -> Tuple[bool, str]`**
- Converts PDF and returns text as string
- Returns: (success, text_or_error)

**`clean_text(text: str) -> str`**
- Cleans raw extracted text
- Returns: cleaned_text

## Troubleshooting

### PDFs with scanned images (no extractable text)

This converter extracts **digital text** from PDFs. For scanned PDFs with images, you'll need OCR software like Tesseract:

```bash
pip install pytesseract
# Then use Tesseract directly or fork this project
```

### Special characters appearing as garbage

The converter handles most encoding issues, but severely corrupted PDFs may need manual review. Check the PDF in a viewer first.

### Performance issues with large PDFs

Large PDFs (1000+ pages) may take several seconds. This is normal. Run with `--verbose` to monitor progress.

## License

MIT - Use freely in your projects

## Contributing

Found a bug? Have a feature request? Create an issue or submit a pull request.

---

**Built for Vishen | 💜 Eliza**
