#!/usr/bin/env python3
"""
PDF to Text Converter
=====================
Simple, reliable tool for converting PDFs to readable text for analysis.

Features:
- Multiple PDF format support (PyPDF2 + pdfplumber fallback)
- Smart text cleaning (removes encoding artifacts, normalizes spacing)
- Page tracking and metadata extraction
- CLI interface with flexible options
- Error handling and recovery
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import re

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


class PDFConverter:
    """Handle PDF to text conversion with multiple strategies."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def log(self, message: str):
        """Print verbose output if enabled."""
        if self.verbose:
            print(f"[PDF] {message}", file=sys.stderr)
    
    def clean_text(self, text: str) -> str:
        """Remove encoding artifacts and normalize spacing."""
        # Remove null bytes and other control characters
        text = text.replace('\x00', '').replace('\r', '')
        
        # Fix common PDF encoding issues
        text = re.sub(r'\u00ad', '', text)  # Remove soft hyphens
        text = re.sub(r'\ufeff', '', text)  # Remove BOM
        
        # Normalize multiple spaces (but preserve intentional indentation)
        text = re.sub(r' {2,}', ' ', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Normalize line breaks (preserve paragraph spacing)
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
        
        text = '\n'.join(cleaned_lines)
        
        # Remove trailing whitespace from each line
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        return text.strip()
    
    def extract_with_pdfplumber(self, pdf_path: str) -> Tuple[str, Dict]:
        """Extract text using pdfplumber (better for formatted PDFs)."""
        try:
            import pdfplumber
        except ImportError:
            return None, {}
        
        try:
            full_text = []
            metadata = {}
            
            with pdfplumber.open(pdf_path) as pdf:
                # Extract metadata
                if pdf.metadata:
                    metadata = {
                        'title': pdf.metadata.get('Title'),
                        'author': pdf.metadata.get('Author'),
                        'subject': pdf.metadata.get('Subject'),
                        'creator': pdf.metadata.get('Creator'),
                        'producer': pdf.metadata.get('Producer'),
                        'creation_date': str(pdf.metadata.get('CreationDate')),
                        'modification_date': str(pdf.metadata.get('ModDate')),
                    }
                
                # Extract text from each page
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        # Add page marker
                        full_text.append(f"\n--- PAGE {page_num} ---\n")
                        full_text.append(text)
            
            text = ''.join(full_text)
            return text, metadata
            
        except Exception as e:
            self.log(f"pdfplumber extraction failed: {e}")
            return None, {}
    
    def extract_with_pypdf2(self, pdf_path: str) -> Tuple[str, Dict]:
        """Extract text using PyPDF2 (fallback option)."""
        try:
            import PyPDF2
        except ImportError:
            return None, {}
        
        try:
            full_text = []
            metadata = {}
            
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                # Extract metadata
                if reader.metadata:
                    metadata = {
                        'title': reader.metadata.get('/Title'),
                        'author': reader.metadata.get('/Author'),
                        'subject': reader.metadata.get('/Subject'),
                        'creator': reader.metadata.get('/Creator'),
                        'producer': reader.metadata.get('/Producer'),
                    }
                
                # Extract text from each page
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        full_text.append(f"\n--- PAGE {page_num} ---\n")
                        full_text.append(text)
            
            text = ''.join(full_text)
            return text, metadata
            
        except Exception as e:
            self.log(f"PyPDF2 extraction failed: {e}")
            return None, {}
    
    def convert(self, pdf_path: str, output_path: Optional[str] = None,
                use_pdfplumber: bool = True, clean: bool = True) -> Dict:
        """
        Convert PDF to text with error handling and multiple strategies.
        
        Args:
            pdf_path: Path to PDF file
            output_path: Path to save text (if None, returns text only)
            use_pdfplumber: Try pdfplumber first (better for formatted PDFs)
            clean: Clean text output (remove artifacts)
        
        Returns:
            Dict with keys: success, text, metadata, pages, path
        """
        pdf_file = Path(pdf_path)
        
        if not pdf_file.exists():
            return {
                'success': False,
                'error': f"PDF file not found: {pdf_path}",
                'text': '',
                'metadata': {},
                'pages': 0
            }
        
        self.log(f"Converting {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")
        
        text = None
        metadata = {}
        
        # Try pdfplumber first (better for most PDFs)
        if use_pdfplumber and HAS_PDFPLUMBER:
            self.log("Attempting extraction with pdfplumber...")
            text, metadata = self.extract_with_pdfplumber(pdf_path)
        
        # Fallback to PyPDF2
        if text is None and HAS_PYPDF2:
            self.log("Attempting extraction with PyPDF2...")
            text, metadata = self.extract_with_pypdf2(pdf_path)
        
        # If both failed, return error
        if text is None:
            return {
                'success': False,
                'error': 'No PDF extraction libraries available. Install: pip install pdfplumber PyPDF2',
                'text': '',
                'metadata': {},
                'pages': 0
            }
        
        # Clean text if requested
        if clean:
            original_len = len(text)
            text = self.clean_text(text)
            self.log(f"Text cleaned: {original_len} → {len(text)} chars")
        
        # Count pages
        page_count = text.count('--- PAGE')
        
        # Save output if requested
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(text, encoding='utf-8')
            self.log(f"Saved to {output_path}")
        
        return {
            'success': True,
            'text': text,
            'metadata': metadata,
            'pages': page_count,
            'path': str(pdf_file.absolute())
        }


def main():
    """CLI interface for PDF conversion."""
    parser = argparse.ArgumentParser(
        description='Convert PDF to readable text for analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s document.pdf                    # Print to stdout
  %(prog)s document.pdf -o output.txt      # Save to file
  %(prog)s document.pdf --json             # Output as JSON
  %(prog)s *.pdf -d output/                # Batch convert to directory
        '''
    )
    
    parser.add_argument('pdf', nargs='+', help='PDF file(s) to convert')
    parser.add_argument('-o', '--output', help='Output text file (or directory for batch)')
    parser.add_argument('-d', '--directory', help='Output directory (shorthand for batch)')
    parser.add_argument('--json', action='store_true', help='Output as JSON with metadata')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-clean', action='store_true', help='Skip text cleaning')
    parser.add_argument('--pypdf2-only', action='store_true', help='Use PyPDF2 only (no pdfplumber)')
    
    args = parser.parse_args()
    
    # Resolve output directory
    output_dir = None
    if args.directory:
        output_dir = Path(args.directory)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    converter = PDFConverter(verbose=args.verbose)
    
    # Handle multiple PDFs
    pdf_files = []
    for pattern in args.pdf:
        pdf_files.extend(Path('.').glob(pattern))
    
    if not pdf_files:
        print(f"Error: No PDF files found matching {args.pdf}", file=sys.stderr)
        sys.exit(1)
    
    results = []
    
    for pdf_file in pdf_files:
        if not pdf_file.suffix.lower() == '.pdf':
            continue
        
        # Determine output path
        output_path = None
        if output_dir:
            output_path = output_dir / f"{pdf_file.stem}.txt"
        elif args.output and not output_dir:
            output_path = args.output
        
        # Convert
        result = converter.convert(
            str(pdf_file),
            output_path=output_path,
            use_pdfplumber=not args.pypdf2_only,
            clean=not args.no_clean
        )
        
        results.append(result)
        
        # Output
        if args.json:
            # Don't include full text in JSON output (too verbose)
            output_result = {**result}
            output_result['text'] = f"[{len(result['text'])} characters extracted]"
            print(json.dumps(output_result, indent=2, default=str))
        elif len(pdf_files) == 1 and not output_path:
            # Single file to stdout
            print(result['text'])
        else:
            # Summary
            if result['success']:
                print(f"✓ {pdf_file.name}: {result['pages']} pages, {len(result['text'])} chars")
            else:
                print(f"✗ {pdf_file.name}: {result.get('error', 'Unknown error')}")
    
    # Exit code
    if all(r['success'] for r in results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
