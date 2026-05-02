#!/usr/bin/env python3
"""
PDF to Text Converter
Simple, reliable tool for converting PDFs to readable text with formatting preservation.
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional, Tuple
import logging

# Try to import PDF libraries
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from pdf2image import convert_from_path
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFConverter:
    """Main PDF to text converter with multiple extraction methods."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check which PDF libraries are available."""
        if self.verbose:
            logger.info("Available PDF libraries:")
            logger.info(f"  PyPDF2: {HAS_PYPDF2}")
            logger.info(f"  pdfplumber: {HAS_PDFPLUMBER}")
            logger.info(f"  OCR (pdf2image + pytesseract): {HAS_OCR}")
        
        if not (HAS_PYPDF2 or HAS_PDFPLUMBER):
            raise ImportError(
                "Please install PyPDF2 or pdfplumber:\n"
                "  pip install PyPDF2\n"
                "  # or\n"
                "  pip install pdfplumber"
            )
    
    def convert_file(self, pdf_path: str, output_path: Optional[str] = None) -> Tuple[str, str]:
        """
        Convert PDF to text using best available method.
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional output file path
        
        Returns:
            Tuple of (extracted_text, method_used)
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        logger.info(f"Converting: {pdf_path.name}")
        
        # Try extraction methods in order of preference
        text = None
        method = None
        
        # Method 1: pdfplumber (best for most PDFs)
        if HAS_PDFPLUMBER and text is None:
            try:
                text, method = self._extract_pdfplumber(pdf_path)
                if text.strip():
                    logger.info(f"✅ Extracted via pdfplumber ({len(text)} chars)")
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}")
        
        # Method 2: PyPDF2 (fallback)
        if HAS_PYPDF2 and (text is None or not text.strip()):
            try:
                text, method = self._extract_pypdf2(pdf_path)
                if text.strip():
                    logger.info(f"✅ Extracted via PyPDF2 ({len(text)} chars)")
            except Exception as e:
                logger.warning(f"PyPDF2 failed: {e}")
        
        # Method 3: OCR (last resort for scanned PDFs)
        if HAS_OCR and (text is None or not text.strip()):
            try:
                text, method = self._extract_ocr(pdf_path)
                if text.strip():
                    logger.info(f"✅ Extracted via OCR ({len(text)} chars)")
            except Exception as e:
                logger.warning(f"OCR failed: {e}")
        
        if not text:
            raise ValueError("Could not extract text from PDF using any method")
        
        # Clean and normalize text
        text = self._clean_text(text)
        
        # Write to output file if specified
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding='utf-8')
            logger.info(f"✅ Written to: {output_path}")
        
        return text, method
    
    def _extract_pdfplumber(self, pdf_path: Path) -> Tuple[str, str]:
        """Extract text using pdfplumber."""
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {page_num} ---\n{text}")
                    if self.verbose:
                        logger.info(f"  Page {page_num}: {len(text)} chars")
        
        return '\n\n'.join(text_parts), 'pdfplumber'
    
    def _extract_pypdf2(self, pdf_path: Path) -> Tuple[str, str]:
        """Extract text using PyPDF2."""
        text_parts = []
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {page_num} ---\n{text}")
                    if self.verbose:
                        logger.info(f"  Page {page_num}: {len(text)} chars")
        
        return '\n\n'.join(text_parts), 'PyPDF2'
    
    def _extract_ocr(self, pdf_path: Path) -> Tuple[str, str]:
        """Extract text using OCR (for scanned PDFs)."""
        images = convert_from_path(pdf_path)
        text_parts = []
        
        for page_num, image in enumerate(images, 1):
            text = pytesseract.image_to_string(image)
            if text:
                text_parts.append(f"--- Page {page_num} (OCR) ---\n{text}")
                if self.verbose:
                    logger.info(f"  Page {page_num} (OCR): {len(text)} chars")
        
        return '\n\n'.join(text_parts), 'OCR'
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace while preserving structure
        lines = text.split('\n')
        cleaned = []
        
        for line in lines:
            # Remove control characters and encoding artifacts
            line = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', line)
            # Normalize unicode spaces
            line = re.sub(r'[\u2000-\u200b]', ' ', line)
            # Remove trailing whitespace
            line = line.rstrip()
            cleaned.append(line)
        
        # Remove excessive blank lines
        text = '\n'.join(cleaned)
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        return text.strip()


def main():
    """CLI interface for PDF converter."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert PDF to text with multiple extraction methods',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s input.pdf                          # Print to stdout
  %(prog)s input.pdf -o output.txt            # Save to file
  %(prog)s input.pdf -o output.txt -v        # Verbose output
  %(prog)s *.pdf -o output/                   # Batch convert to directory
        '''
    )
    
    parser.add_argument('pdf_files', nargs='+', help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    converter = PDFConverter(verbose=args.verbose)
    
    # Handle batch conversion
    pdf_files = []
    for pattern in args.pdf_files:
        pdf_files.extend(Path('.').glob(pattern) if '*' in pattern else [Path(pattern)])
    
    if not pdf_files:
        logger.error("No PDF files found")
        sys.exit(1)
    
    for pdf_path in pdf_files:
        try:
            # Determine output path
            if args.output:
                output_path = Path(args.output)
                if output_path.is_dir() or args.output.endswith('/'):
                    output_path = output_path / f"{pdf_path.stem}.txt"
            else:
                output_path = None
            
            text, method = converter.convert_file(str(pdf_path), str(output_path) if output_path else None)
            
            if not output_path:
                print(text)
            
            logger.info(f"✅ Done: {pdf_path.name} (via {method})")
            
        except Exception as e:
            logger.error(f"❌ Error processing {pdf_path}: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
