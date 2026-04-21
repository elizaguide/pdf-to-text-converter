#!/usr/bin/env python3
"""
Tests for PDF to Text Converter
"""

import sys
import os
from pathlib import Path
import tempfile
import unittest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pdf_converter import PDFConverter


class TestPDFConverter(unittest.TestCase):
    """Test suite for PDFConverter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.converter = PDFConverter(verbose=False)
    
    def test_converter_initialization(self):
        """Test converter initializes correctly"""
        self.assertIsNotNone(self.converter)
        self.assertEqual(self.converter.stats['pages_processed'], 0)
    
    def test_text_cleaning(self):
        """Test text cleaning removes artifacts"""
        test_cases = [
            # (input, expected_output)
            ('hello  \n\n\n  world', 'hello\n\nworld'),
            ('test\x00text', 'testtext'),
            ('ï»¿content', 'content'),
            ('normal  spaces', 'normal spaces'),
            ('trailing \n', 'trailing'),
            ('\x01\x02\x03text', 'text'),
        ]
        
        for input_text, expected in test_cases:
            result = self.converter._clean_text(input_text)
            self.assertEqual(result, expected, 
                           f"Failed cleaning: {repr(input_text)}")
    
    def test_missing_file(self):
        """Test error handling for missing PDF"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_pdf('/nonexistent/file.pdf')
    
    def test_invalid_file_type(self):
        """Test error handling for non-PDF files"""
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            with self.assertRaises(ValueError):
                self.converter.convert_pdf(f.name)


class TestTextCleaning(unittest.TestCase):
    """Detailed text cleaning tests"""
    
    def setUp(self):
        self.converter = PDFConverter()
    
    def test_null_bytes_removed(self):
        """Test null bytes are removed"""
        text = "hello\x00world"
        result = self.converter._clean_text(text)
        self.assertNotIn('\x00', result)
    
    def test_utf8_bom_removed(self):
        """Test UTF-8 BOM is removed"""
        text = "ï»¿content"
        result = self.converter._clean_text(text)
        self.assertEqual(result, "content")
    
    def test_multiple_newlines_normalized(self):
        """Test multiple newlines normalized to 2"""
        text = "line1\n\n\n\n\nline2"
        result = self.converter._clean_text(text)
        self.assertEqual(result, "line1\n\nline2")
    
    def test_multiple_spaces_collapsed(self):
        """Test multiple spaces collapsed to 1"""
        text = "word1    word2"
        result = self.converter._clean_text(text)
        self.assertEqual(result, "word1 word2")


if __name__ == '__main__':
    unittest.main()
