#!/usr/bin/env python3
"""
Test suite for PDF to Text Converter
Validates all core functionality and edge cases
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_converter import PDFConverter

def create_simple_test_pdf():
    """
    Create a minimal valid PDF for testing
    Returns path to test PDF
    """
    # Use reportlab if available, else create minimal PDF manually
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        test_pdf = Path(tempfile.gettempdir()) / "test_sample.pdf"
        c = canvas.Canvas(str(test_pdf), pagesize=letter)
        c.setFont("Helvetica", 12)
        
        # Page 1
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 730, "This is a test document for the PDF converter.")
        c.drawString(100, 710, "")
        c.drawString(100, 690, "Features tested:")
        c.drawString(120, 670, "• Multiple pages support")
        c.drawString(120, 650, "• Text extraction accuracy")
        c.drawString(120, 630, "• Whitespace handling")
        c.showPage()
        
        # Page 2
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Page 2: Additional Content")
        c.drawString(100, 730, "This verifies multi-page extraction works correctly.")
        c.drawString(100, 710, "The converter should extract text from all pages.")
        c.showPage()
        
        c.save()
        return test_pdf
        
    except ImportError:
        # Fallback: Create minimal PDF manually
        test_pdf = Path(tempfile.gettempdir()) / "test_sample.pdf"
        
        # Minimal valid PDF structure
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 750 Td
(Test PDF) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000243 00000 n 
0000000336 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
419
%%EOF"""
        
        with open(test_pdf, 'wb') as f:
            f.write(pdf_content)
        return test_pdf


def test_basic_conversion():
    """Test basic PDF to text conversion"""
    print("\n🧪 Test 1: Basic Conversion")
    try:
        converter = PDFConverter(verbose=False)
        test_pdf = create_simple_test_pdf()
        text = converter.convert(str(test_pdf))
        
        assert text, "No text extracted"
        assert len(text) > 0, "Extracted text is empty"
        print(f"  ✓ Extracted {len(text)} characters")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_file_output():
    """Test saving to file"""
    print("\n🧪 Test 2: File Output")
    try:
        converter = PDFConverter(verbose=False)
        test_pdf = create_simple_test_pdf()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.txt"
            converter.convert(str(test_pdf), output_path=str(output_file))
            
            assert output_file.exists(), "Output file not created"
            content = output_file.read_text()
            assert len(content) > 0, "Output file is empty"
            print(f"  ✓ Saved {len(content)} characters to file")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_text_cleaning():
    """Test text cleaning functionality"""
    print("\n🧪 Test 3: Text Cleaning")
    try:
        converter = PDFConverter(verbose=False)
        
        # Test cases with encoding artifacts
        test_cases = [
            ("normal text", "normal text"),
            ("text  with   spaces", "text with spaces"),
            ("line1\n\n\n\nline2", "line1\n\nline2"),
            ("  indented  text  ", "indented text"),
        ]
        
        for input_text, expected in test_cases:
            cleaned = converter.clean_text(input_text)
            assert cleaned == expected, f"Expected '{expected}', got '{cleaned}'"
        
        print(f"  ✓ All {len(test_cases)} cleaning tests passed")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def test_error_handling():
    """Test error handling"""
    print("\n🧪 Test 4: Error Handling")
    try:
        converter = PDFConverter(verbose=False)
        
        # Test non-existent file
        try:
            converter.convert("/nonexistent/file.pdf")
            print("  ✗ Should have raised FileNotFoundError")
            return False
        except FileNotFoundError:
            pass
        
        # Test non-PDF file
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            try:
                converter.convert(f.name)
                print("  ✗ Should have raised ValueError for non-PDF")
                return False
            except ValueError:
                pass
        
        print("  ✓ Error handling works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return False


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("PDF to Text Converter - Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_conversion,
        test_file_output,
        test_text_cleaning,
        test_error_handling,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return all(results)


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
