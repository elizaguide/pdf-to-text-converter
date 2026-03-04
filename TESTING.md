# Testing Guide - PDF to Text Converter

## Test Cases

### Test 1: Help Command
```bash
python3 pdf_converter.py --help
```
✅ **Expected:** Shows help message with usage instructions

### Test 2: No Arguments
```bash
python3 pdf_converter.py
```
✅ **Expected:** Shows usage information

### Test 3: Verbose Mode (with real PDF)
```bash
./pdf-converter -v your_document.pdf
```
✅ **Expected:** 
- Shows progress messages
- Reports page count
- Shows extraction progress
- Creates output.txt file

### Test 4: Custom Output Path
```bash
./pdf-converter input.pdf custom_output.txt
```
✅ **Expected:** Creates file at `custom_output.txt`

### Test 5: Error Handling - Missing File
```bash
./pdf-converter nonexistent.pdf
```
✅ **Expected:** Shows error: "ERROR: File not found"

### Test 6: Error Handling - Wrong File Type
```bash
./pdf-converter document.docx
```
✅ **Expected:** Shows error: "ERROR: File is not a PDF"

## Integration Test

```python
from pdf_converter import PDFToTextConverter

converter = PDFToTextConverter(verbose=True)
success, message = converter.convert_file('test.pdf', 'test_output.txt')
assert success == True
assert 'Converted' in message
print("✓ Integration test passed")
```

## Manual Testing

1. **Real PDF Testing**: Run against the analysis document that triggered this build
   ```bash
   ./pdf-converter analysis_document.pdf output.txt
   ```

2. **Verify Output**:
   - Open `output.txt` in a text editor
   - Check that text is readable
   - Verify no encoding artifacts (garbage characters)
   - Confirm page breaks are marked

3. **Large PDF Test** (optional):
   - Test with a 50+ page PDF
   - Monitor performance
   - Verify all pages extracted

## Expected Output Format

```
[First page content]

--- Page Break ---

[Second page content]

--- Page Break ---

[Third page content]
```

## Success Criteria

- ✅ CLI responds to help/version commands
- ✅ File conversion creates .txt output
- ✅ Text is readable (no encoding artifacts)
- ✅ Multi-page PDFs handled correctly
- ✅ Error messages are clear
- ✅ Verbose mode provides progress feedback
- ✅ Handles edge cases gracefully

---

When ready, run real PDF through the converter and verify output quality.
