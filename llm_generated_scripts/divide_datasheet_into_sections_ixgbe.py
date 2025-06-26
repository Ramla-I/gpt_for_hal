import re
import sys
import pymupdf4llm

def divide_datasheet_into_sections(datasheet_text):
    # Split the text into lines
    lines = datasheet_text.split('\n')
    # Regex to match a section header that's on its own line (possibly with leading #, spaces, and ** at start/end)
    # header_regex = re.compile(r'^\s*#?\s*\*\*(\d+(?:\.\d+)+)\s+.*\*\*')
    header_regex = re.compile(
        r'^[\s#*]*'
        r'(\d+(?:\.\d+)+)\s+'         # Section number (e.g. 12.0.3.4.27)
        r'([^*]+?\([^)]*\)[^*]*)'     # Register name, must contain parenthesis e.g. 'Multiple ... (xxxx; RW)'
        r'[\s*]*$'
    )

    # Collect (line_index, line_text) of all section header lines
    header_indices = [
        (idx, line)
        for idx, line in enumerate(lines)
        if header_regex.match(line)
    ]

    sections = []
    for i, (header_idx, header_line) in enumerate(header_indices):
        # Section starts at header_idx
        section_start = header_idx
        # Section ends at next header, or at end of lines
        if i + 1 < len(header_indices):
            section_end = header_indices[i + 1][0]
        else:
            section_end = len(lines)
        # Get section lines, strip leading/trailing blank lines
        section_lines = lines[section_start:section_end]
        while section_lines and section_lines[0].strip() == '':
            section_lines = section_lines[1:]
        while section_lines and section_lines[-1].strip() == '':
            section_lines = section_lines[:-1]
        if section_lines:
            section_text = '\n'.join(section_lines)
            sections.append(section_text)
    return sections



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_section_headers.py <pdf_path> <output_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    datasheet_text = pymupdf4llm.to_markdown(pdf_path)
    sections = divide_datasheet_into_sections(datasheet_text)
    print(len(sections))
    # for i, section in enumerate(sections, 1):
    #     print(f"\n=== Section {i} ===\n{section}\n")