#!/usr/bin/env python3
"""
Tests for PDF converter.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_converter import PDFConverter


def test_converter_initialization():
    """Test converter initialization."""
    converter = PDFConverter(verbose=False)
    assert converter is not None
    assert isinstance(converter, PDFConverter)


def test_text_cleaning():
    """Test text cleaning functionality."""
    converter = PDFConverter(verbose=False)
    
    # Test with encoding artifacts
    dirty_text = "Hello\x00World\u200b\n\n\n\nTest"
    clean = converter._clean_text(dirty_text)
    
    # Check control characters are removed
    assert '\x00' not in clean
    assert '\u200b' not in clean
    # Check excessive blank lines are removed
    assert '\n\n\n' not in clean


def test_text_normalization():
    """Test unicode normalization."""
    converter = PDFConverter(verbose=False)
    
    # Test with various unicode spaces
    text_with_spaces = "Hello\u2000World\u2001Test"
    clean = converter._clean_text(text_with_spaces)
    
    # Should have normal spaces instead of unicode spaces
    assert '\u2000' not in clean
    assert '\u2001' not in clean
    assert 'Hello' in clean and 'World' in clean


if __name__ == '__main__':
    # Run basic tests
    test_converter_initialization()
    print("✅ Converter initialization test passed")
    
    test_text_cleaning()
    print("✅ Text cleaning test passed")
    
    test_text_normalization()
    print("✅ Text normalization test passed")
    
    print("\n✅ All tests passed!")
