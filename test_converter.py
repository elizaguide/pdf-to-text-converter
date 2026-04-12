#!/usr/bin/env python3
"""
Test suite for PDF to Text Converter
"""

import sys
import tempfile
from pathlib import Path

# Try importing the converter
try:
    from pdf_converter import PDFConverter
    print("✅ Successfully imported PDFConverter")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def test_file_not_found():
    """Test handling of missing file."""
    print("\n📋 Test 1: File not found")
    converter = PDFConverter()
    success, message = converter.convert('nonexistent.pdf')
    assert not success, "Should return False for missing file"
    assert "not found" in message.lower(), f"Error message should mention file: {message}"
    print("   ✅ Correctly handles missing files")


def test_invalid_file():
    """Test handling of non-PDF file."""
    print("\n📋 Test 2: Invalid file type")
    converter = PDFConverter()
    
    # Create a temp text file
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        temp_path = f.name
    
    try:
        success, message = converter.convert(temp_path)
        assert not success, "Should return False for non-PDF"
        assert "not a pdf" in message.lower(), f"Error message should mention PDF: {message}"
        print("   ✅ Correctly rejects non-PDF files")
    finally:
        Path(temp_path).unlink()


def test_text_cleaning():
    """Test text cleaning functions."""
    print("\n📋 Test 3: Text cleaning")
    converter = PDFConverter()
    
    # Test multiple spaces
    dirty = "Hello    world"
    clean = converter._clean_text(dirty)
    assert clean == "Hello world", f"Should collapse spaces: {clean}"
    print("   ✅ Collapses multiple spaces")
    
    # Test multiple newlines
    dirty = "Line1\n\n\n\nLine2"
    clean = converter._clean_text(dirty)
    assert "Line1\n\nLine2" in clean, f"Should limit newlines: {clean}"
    print("   ✅ Limits excessive newlines")
    
    # Test trailing spaces
    dirty = "Line1  \nLine2  "
    clean = converter._clean_text(dirty)
    assert clean == "Line1\nLine2", f"Should remove trailing spaces: {clean}"
    print("   ✅ Removes trailing spaces")


def test_module_import():
    """Test that module can be imported correctly."""
    print("\n📋 Test 4: Module structure")
    assert hasattr(PDFConverter, 'convert'), "PDFConverter should have convert method"
    assert hasattr(PDFConverter, 'save_text'), "PDFConverter should have save_text method"
    assert hasattr(PDFConverter, '_clean_text'), "PDFConverter should have _clean_text method"
    print("   ✅ All required methods present")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("PDF to Text Converter - Test Suite")
    print("=" * 50)
    
    try:
        test_module_import()
        test_text_cleaning()
        test_file_not_found()
        test_invalid_file()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
