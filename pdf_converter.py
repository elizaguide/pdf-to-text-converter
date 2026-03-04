#!/usr/bin/env python3
"""
PDF to Text Converter
Simple, reliable tool for extracting text from PDF files with clean formatting.
Handles multiple PDF formats and removes encoding artifacts.
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional, Tuple
import PyPDF2


class PDFToTextConverter:
    """Convert PDF files to clean, readable text."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize converter.
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
    
    def log(self, message: str) -> None:
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"[PDF Converter] {message}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text of encoding artifacts and formatting issues.
        
        Args:
            text: Raw extracted text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove null bytes and other control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Fix common OCR/encoding artifacts
        text = re.sub(r'\n\s*\n[\s\n]+', '\n\n', text)  # Multiple blank lines → double newline
        text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)    # Hyphenation at line breaks
        text = re.sub(r'\s+', ' ', text)                # Multiple spaces → single space
        text = re.sub(r' +\n', '\n', text)              # Trailing spaces
        
        # Fix common OCR mistakes (basic patterns)
        text = re.sub(r'\bi\b(?=[A-Z])', 'I', text)     # Lowercase i → I before capitals
        text = re.sub(r'([a-z])\s+([a-z])\s+([a-z])', r'\1\2\3', text)  # Split words
        
        # Normalize whitespace at start/end
        text = text.strip()
        
        return text
    
    def extract_from_pdf(self, pdf_path: str) -> Tuple[str, bool]:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, success_flag)
        """
        try:
            pdf_path = Path(pdf_path)
            
            if not pdf_path.exists():
                return f"ERROR: File not found: {pdf_path}", False
            
            if not pdf_path.suffix.lower() == '.pdf':
                return f"ERROR: File is not a PDF: {pdf_path}", False
            
            self.log(f"Opening: {pdf_path.name}")
            
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                num_pages = len(pdf_reader.pages)
                self.log(f"Found {num_pages} pages")
                
                extracted_text = []
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    self.log(f"Extracting page {page_num}/{num_pages}")
                    page_text = page.extract_text()
                    
                    if page_text:
                        extracted_text.append(page_text)
                    else:
                        self.log(f"Warning: Page {page_num} yielded no text")
                
                # Join all pages with page separators
                full_text = '\n\n--- Page Break ---\n\n'.join(extracted_text)
                
                # Clean the text
                self.log("Cleaning text")
                cleaned_text = self.clean_text(full_text)
                
                self.log(f"Extraction complete: {len(cleaned_text)} characters")
                return cleaned_text, True
        
        except PyPDF2.PdfReadError as e:
            return f"ERROR: PDF reading error - {str(e)}", False
        except Exception as e:
            return f"ERROR: {type(e).__name__} - {str(e)}", False
    
    def convert_file(
        self, 
        input_path: str, 
        output_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Convert PDF file to text file.
        
        Args:
            input_path: Path to input PDF
            output_path: Path to output text file (optional, defaults to input.txt)
            
        Returns:
            Tuple of (success, message)
        """
        input_path = Path(input_path)
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix('.txt')
        else:
            output_path = Path(output_path)
        
        # Extract text
        text, success = self.extract_from_pdf(str(input_path))
        
        if not success:
            return False, text
        
        # Write to file
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            message = f"✓ Converted: {input_path.name} → {output_path.name}"
            self.log(message)
            return True, message
        
        except Exception as e:
            return False, f"ERROR: Failed to write output - {str(e)}"
    
    def convert_string(self, pdf_path: str) -> Tuple[bool, str]:
        """
        Convert PDF and return text as string (not saved to file).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (success, text)
        """
        return self.extract_from_pdf(pdf_path)


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("PDF to Text Converter")
        print("\nUsage:")
        print("  pdf-converter <input.pdf>                    # Creates input.txt")
        print("  pdf-converter <input.pdf> <output.txt>       # Custom output path")
        print("  pdf-converter --help                         # Show this help")
        print("\nOptions:")
        print("  -v, --verbose                               # Print progress messages")
        print("\nExamples:")
        print("  pdf-converter document.pdf")
        print("  pdf-converter document.pdf output/text.txt")
        print("  pdf-converter -v document.pdf output.txt")
        sys.exit(1)
    
    # Parse arguments
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ['-v', '--verbose']]
    
    if '--help' in args or '-h' in args:
        print("PDF to Text Converter - Command line tool for extracting text from PDFs")
        print("\nUsage: pdf-converter [options] <input.pdf> [output.txt]")
        print("\nOptions:")
        print("  -v, --verbose    Show progress messages")
        print("  --help          Show this help message")
        sys.exit(0)
    
    if len(args) < 1:
        print("ERROR: No input file provided")
        sys.exit(1)
    
    input_file = args[0]
    output_file = args[1] if len(args) > 1 else None
    
    # Run conversion
    converter = PDFToTextConverter(verbose=verbose)
    success, message = converter.convert_file(input_file, output_file)
    
    print(message)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
