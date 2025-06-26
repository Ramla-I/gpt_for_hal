import re
import sys
import pymupdf4llm

def extract_section_headers(text):
    headers = []
    # We'll consider headers at the START of a line, with possible leading #, *, spaces, etc.
    # Regex parts:
    #   ^[\s#*]*               : Optional whitespace, hash or asterisk (markdown title/bold)
    #   (\d+(\.\d+)+)         : Hierarchical numbers like 12.0.3.4.27
    #   \s+                   : Spaces
    #   ([^\n*]+)             : The register name, up to next newline (but not trailing * markdown bold end)
    #   \(.*\)                : Parentheses with address info (optional), keep as part of header
    #   (\*{0,2})             : Optional closing **
    #   $                     : End of line
    # Note: For multi-line (not just linewise), we split on newlines
    header_pattern = re.compile(
        r'^[\s#*]*'
        r'(\d+(?:\.\d+)+)\s+'         # Section number (e.g. 12.0.3.4.27)
        r'([^*]+?\([^)]*\)[^*]*)'     # Register name, must contain parenthesis e.g. 'Multiple ... (xxxx; RW)'
        r'[\s*]*$'
    )
    for line in text.split('\n'):
        m = header_pattern.match(line)
        if m:
            # Clean up markdown symbols, whitespace
            header = line.strip(" #*")
            headers.append(header)
    return headers

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_section_headers.py <pdf_path> <output_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    datasheet_text = pymupdf4llm.to_markdown(pdf_path)
    headers = extract_section_headers(datasheet_text)
    output_file = sys.argv[2]
    with open(output_file, "w", encoding="utf-8") as f:
        for header in headers:
            f.write(header + "\n")