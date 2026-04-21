#!/usr/bin/env python3
"""
PDF to Text Converter - Clean, simple, reliable
Handles multiple PDF formats with intelligent text extraction and cleaning
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional, List
import PyPDF2


class PDFConverter:
    """Core PDF to text conversion engine"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {
            'pages_processed': 0,
            'text_extracted': 0,
            'encoding_errors': 0,
            'empty_pages': 0
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text: remove artifacts, normalize whitespace
        """
        # Remove null bytes and control characters
        text = text.replace('\x00', '')
        text = re.sub(r'[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        
        # Fix common PDF encoding artifacts
        text = text.replace('ï»¿', '')  # UTF-8 BOM
        text = text.replace('\ufeff', '')  # Zero-width no-break space
        text = text.replace('Â', '')  # Common encoding artifact
        
        # Normalize whitespace - order matters!
        # 1. Replace runs of spaces with single space (but preserve tabs for now)
        text = re.sub(r'[ ]+', ' ', text)
        
        # 2. Remove spaces before/after newlines
        text = re.sub(r' +\n', '\n', text)  # trailing spaces
        text = re.sub(r'\n +', '\n', text)  # leading spaces after newline
        
        # 3. Replace multiple newlines with exactly 2
        text = re.sub(r'\n\n+', '\n\n', text)
        
        # Clean page break artifacts
        text = re.sub(r'\n\s*-+\s*\n', '\n\n', text)  # Separator lines
        
        return text.strip()
    
    def convert_pdf(self, pdf_path: str) -> str:
        """
        Convert PDF to clean text
        Returns: Extracted text string
        Raises: FileNotFoundError, PyPDF2.PdfReadError
        """
        pdf_file = Path(pdf_path)
        
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        if not pdf_file.suffix.lower() == '.pdf':
            raise ValueError(f"File must be PDF: {pdf_path}")
        
        extracted_text = []
        
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                if self.verbose:
                    print(f"📄 Processing: {pdf_file.name} ({total_pages} pages)")
                
                for page_num, page in enumerate(reader.pages, 1):
                    try:
                        text = page.extract_text()
                        
                        if text and text.strip():
                            cleaned = self._clean_text(text)
                            if cleaned:
                                extracted_text.append(cleaned)
                                self.stats['text_extracted'] += len(cleaned)
                            else:
                                self.stats['empty_pages'] += 1
                        else:
                            self.stats['empty_pages'] += 1
                        
                        self.stats['pages_processed'] += 1
                        
                        if self.verbose and page_num % 10 == 0:
                            print(f"  ✓ Processed {page_num}/{total_pages} pages")
                    
                    except Exception as e:
                        self.stats['encoding_errors'] += 1
                        if self.verbose:
                            print(f"  ⚠️  Page {page_num}: {str(e)}")
                        continue
        
        except PyPDF2.PdfReadError as e:
            raise PyPDF2.PdfReadError(f"Failed to read PDF: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
        
        if not extracted_text:
            raise ValueError("No text could be extracted from PDF")
        
        if self.verbose:
            print(f"✅ Complete! {self.stats['pages_processed']} pages, "
                  f"{self.stats['empty_pages']} empty, "
                  f"{self.stats['encoding_errors']} errors")
        
        return '\n\n'.join(extracted_text)
    
    def convert_to_file(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert PDF and save to text file
        Returns: Path to output file
        """
        pdf_file = Path(pdf_path)
        
        if output_path is None:
            output_path = pdf_file.with_suffix('.txt')
        else:
            output_path = Path(output_path)
        
        text = self.convert_pdf(pdf_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        if self.verbose:
            file_size = output_path.stat().st_size
            print(f"💾 Saved: {output_path} ({file_size:,} bytes)")
        
        return str(output_path)


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert PDF to clean text',
        epilog='Examples:\n'
               '  pdf-convert input.pdf\n'
               '  pdf-convert input.pdf -o output.txt\n'
               '  pdf-convert input.pdf --verbose',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('-o', '--output', help='Output text file (default: same name, .txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        converter = PDFConverter(verbose=args.verbose)
        output_file = converter.convert_to_file(args.pdf_file, args.output)
        
        if not args.verbose:
            print(f"✅ Success! Output: {output_file}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except PyPDF2.PdfReadError as e:
        print(f"❌ PDF Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
