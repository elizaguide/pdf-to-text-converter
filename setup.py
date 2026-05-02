#!/usr/bin/env python3
"""
Setup script for PDF to Text Converter.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-text-converter",
    version="1.0.0",
    author="Eliza",
    author_email="eliza@mindvalley.com",
    description="Simple, reliable tool for converting PDFs to readable text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mindvalley/pdf-text-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
    ],
    extras_require={
        "ocr": ["pdf2image>=1.16.0", "pytesseract>=0.3.10"],
        "dev": ["pytest>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "pdf2text=src.pdf_converter:main",
        ],
    },
)
