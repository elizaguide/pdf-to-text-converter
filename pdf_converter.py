#!/usr/bin/env python3
"""
PDF to Text Converter
A simple, reliable tool for converting PDFs to readable text.
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional, Tuple

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 not found. Install with: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


class PDFConverter:
    """Convert PDF files to clean, readable text."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing encoding artifacts and formatting issues.
        """
        if not text:
            return ""
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Remove multiple newlines (keep max 2)
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        # Remove trailing spaces on each line
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Remove control characters and other encoding artifacts
        text = ''.join(char if ord(char) >= 32 or char in '\n\t\r' else '' for char in text)
        
        # Fix common encoding issues
        text = text.replace('\\x00', '')
        text = text.replace('\x00', '')
        
        return text.strip()
    
    def convert(self, pdf_path: str) -> Tuple[bool, str]:
        """
        Convert PDF to text.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (success: bool, content_or_error: str)
        """
        pdf_file = Path(pdf_path)
        
        # Validate file
        if not pdf_file.exists():
            return False, f"Error: File not found: {pdf_path}"
        
        if not pdf_file.suffix.lower() == '.pdf':
            return False, f"Error: Not a PDF file: {pdf_path}"
        
        try:
            if self.verbose:
                print(f"Opening PDF: {pdf_path}")
            
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Get metadata
                num_pages = len(reader.pages)
                if self.verbose:
                    print(f"PDF has {num_pages} pages")
                
                # Extract text from all pages
                text_content = []
                for page_num, page in enumerate(reader.pages, 1):
                    if self.verbose:
                        print(f"  Processing page {page_num}/{num_pages}...")
                    
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text)
                    except Exception as e:
                        if self.verbose:
                            print(f"    Warning: Issue extracting page {page_num}: {e}")
                        continue
                
                if not text_content:
                    return False, "Error: No text could be extracted from PDF"
                
                # Combine all pages
                full_text = '\n\n--- PAGE BREAK ---\n\n'.join(text_content)
                
                # Clean the text
                cleaned_text = self._clean_text(full_text)
                
                if self.verbose:
                    print(f"Extracted {len(cleaned_text)} characters from {num_pages} pages")
                
                return True, cleaned_text
                
        except PyPDF2.errors.PdfReadError as e:
            return False, f"Error: Invalid PDF file - {e}"
        except Exception as e:
            return False, f"Error: {type(e).__name__}: {e}"
    
    def save_text(self, pdf_path: str, output_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Convert PDF and save to text file.
        
        Args:
            pdf_path: Path to PDF file
            output_path: Path to save text (defaults to PDF filename with .txt extension)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        success, content = self.convert(pdf_path)
        
        if not success:
            return False, content
        
        # Determine output path
        if output_path is None:
            pdf_file = Path(pdf_path)
            output_path = str(pdf_file.with_suffix('.txt'))
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, f"Success: Saved to {output_path}"
        except Exception as e:
            return False, f"Error saving file: {e}"


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("PDF to Text Converter")
        print("\nUsage:")
        print("  python pdf_converter.py <pdf_file> [output_file]")
        print("\nOptions:")
        print("  -v, --verbose    Show detailed progress")
        print("\nExamples:")
        print("  python pdf_converter.py document.pdf")
        print("  python pdf_converter.py document.pdf output.txt")
        print("  python pdf_converter.py -v document.pdf")
        sys.exit(1)
    
    # Parse arguments
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ['-v', '--verbose']]
    
    if len(args) < 1:
        print("Error: PDF file required", file=sys.stderr)
        sys.exit(1)
    
    pdf_path = args[0]
    output_path = args[1] if len(args) > 1 else None
    
    converter = PDFConverter(verbose=verbose)
    success, message = converter.save_text(pdf_path, output_path)
    
    print(message)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
