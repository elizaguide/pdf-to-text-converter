#!/usr/bin/env python3
"""
PDF to Text Converter
Simple, reliable tool for converting PDFs to readable text for analysis
Handles multiple PDF formats and edge cases with clean output formatting
"""

import sys
import os
import re
import argparse
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("ERROR: PyPDF2 not installed. Installing now...")
    os.system("pip install PyPDF2 -q")
    import PyPDF2

try:
    import pdfplumber
except ImportError:
    print("INFO: pdfplumber not installed. Using PyPDF2 fallback...")
    pdfplumber = None


class PDFConverter:
    """Main PDF to text converter with multiple fallback strategies"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def log(self, message):
        """Print verbose logs if enabled"""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)
    
    def clean_text(self, text):
        """
        Clean extracted text by removing encoding artifacts and formatting issues
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline (preserve paragraph breaks)
        text = re.sub(r'\n\n+', '\n\n', text)
        
        # Remove control characters and artifacts
        text = ''.join(ch for ch in text if ord(ch) >= 32 or ch in '\n\t\r')
        
        # Fix common encoding issues
        text = text.replace('ï¿½', '')  # UTF-8 BOM artifact
        text = text.replace('\x00', '')  # Null bytes
        
        # Remove excessive whitespace at line starts (from OCR/encoding)
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        text = '\n'.join(lines)
        
        # Remove blank lines at start and end
        text = text.strip()
        
        return text
    
    def extract_with_pdfplumber(self, pdf_path):
        """Extract text using pdfplumber (best for formatted text)"""
        if pdfplumber is None:
            return None
            
        try:
            self.log(f"Attempting extraction with pdfplumber...")
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num} ---\n{page_text}\n"
                    except Exception as e:
                        self.log(f"Warning: Could not extract page {page_num}: {e}")
                        continue
                return text if text else None
        except Exception as e:
            self.log(f"pdfplumber extraction failed: {e}")
            return None
    
    def extract_with_pypdf2(self, pdf_path):
        """Extract text using PyPDF2 (fallback, more reliable for damaged PDFs)"""
        try:
            self.log(f"Attempting extraction with PyPDF2...")
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                self.log(f"PDF has {num_pages} pages")
                
                for page_num, page in enumerate(reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num} ---\n{page_text}\n"
                    except Exception as e:
                        self.log(f"Warning: Could not extract page {page_num}: {e}")
                        continue
                
                return text if text else None
        except Exception as e:
            self.log(f"PyPDF2 extraction failed: {e}")
            return None
    
    def convert(self, pdf_path, output_path=None):
        """
        Convert PDF to text using best available method
        
        Args:
            pdf_path: Path to input PDF
            output_path: Optional path to save output text (else returns string)
            
        Returns:
            Extracted text string if output_path is None, else True/False
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        self.log(f"Converting: {pdf_path}")
        
        # Try pdfplumber first (better formatting)
        text = self.extract_with_pdfplumber(str(pdf_path))
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text:
            text = self.extract_with_pypdf2(str(pdf_path))
        
        if not text:
            raise ValueError(f"Could not extract text from PDF: {pdf_path}")
        
        # Clean the extracted text
        text = self.clean_text(text)
        
        # Save or return
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            self.log(f"Saved output to: {output_path}")
            return True
        else:
            return text


def main():
    """CLI interface for PDF converter"""
    parser = argparse.ArgumentParser(
        description="Convert PDF to clean, readable text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_converter.py input.pdf
  python pdf_converter.py input.pdf -o output.txt
  python pdf_converter.py input.pdf -o output.txt -v
  python pdf_converter.py *.pdf -o output/
        """
    )
    
    parser.add_argument('pdf_files', nargs='+', help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', help='Output path (file or directory)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    converter = PDFConverter(verbose=args.verbose)
    
    # Handle multiple input files
    pdf_files = []
    for pattern in args.pdf_files:
        matches = Path('.').glob(pattern) if '*' in pattern else [Path(pattern)]
        pdf_files.extend(matches)
    
    if not pdf_files:
        print("ERROR: No PDF files found", file=sys.stderr)
        sys.exit(1)
    
    # Process each file
    for pdf_path in pdf_files:
        try:
            output_path = None
            if args.output:
                output_dir = Path(args.output)
                if len(pdf_files) > 1 or (output_dir.exists() and output_dir.is_dir()):
                    # Multiple files → output is directory
                    output_path = output_dir / f"{pdf_path.stem}.txt"
                else:
                    # Single file → output is file path
                    output_path = Path(args.output)
            
            text = converter.convert(str(pdf_path), output_path=output_path)
            
            if output_path:
                print(f"✓ Converted: {pdf_path} → {output_path}")
            else:
                print(text)
                
        except Exception as e:
            print(f"✗ Error converting {pdf_path}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
