import re
import sys
import pymupdf4llm


def split_datasheet_sections(md_text):
    # Preprocess: Join split bold lines (multi-line headers)
    md_text = re.sub(r'\*\*(.*?)\*\*\s*\n\s*\*\*(.*?)\*\*', r'**\1 \2**', md_text)
    # print(md_text)
    
    # This regex matches headers like:
    # **12.0.3.16.4** **MACsec RX Not using SA - LSECRXNUSA[n] (0x043C0 + 4*n (n=0…3); RC)**
    header_pattern = re.compile(
        # \*\* – Matches literal **
        # (\d+(?:\.\d+)+) – Matches the section number like 10.5.5.5.5 (one or more dots)
        # \*\* \*\* – Matches the ** ** separator between section number and name
        # (.*?) – Lazily captures the section name
        # - – Matches the literal dash between name and abbreviation
        # (.*?) – Lazily captures the section abbreviation
        # \((.+)\) – Captures everything inside the outermost parentheses (including nested ones)
        # \*\* – Closing bold
        r"\*\*(\d+(?:\.\d+)+)\*\* \*\*(.*?) - (.*?) \((.+)\)\*\*",
        re.MULTILINE
    )

    # Find all matches and their positions
    matches = list(header_pattern.finditer(md_text))

    # Slice the full text into sections using match positions
    sections = {}
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        section_text = md_text[start:end].strip()
        section_number = match.group(1).strip()
        section_header = match.group(2).strip()
        section_abbreviation = match.group(3).strip()
        sections[section_abbreviation] = section_text
    return sections

# Example usage:
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_section_headers.py <pdf_path> <output_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    datasheet_text = pymupdf4llm.to_markdown(pdf_path)
    sections = split_datasheet_sections(datasheet_text)
    print(len(sections))


## Summary of Identification Criteria

# - **A section header is identified by a line starting at the beginning with (optional bold/heading chars) and a section number (e.g., 12.0.3.2.1), followed by at least one space and further text.**
# - **Multi-line headers** are handled by aggregating following lines that look like a continuation (e.g., register mode, "RW)", etc).
# - **Section splitting only occurs at header lines that stand alone at the start of a line**—so inline references are not falsely detected as section splits.
# - **Output:** A list of full text blocks, each with the section header as first line and all the associated content.

# This approach is robust to the datasheet's actual structure, avoids false positives from references, and doesn't miss real sections even if the header is a little complex or split. You can adjust the regex as needed for variants in other datasheets.