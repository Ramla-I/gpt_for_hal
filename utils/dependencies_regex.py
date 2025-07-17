import re
from typing import List, Dict, Optional, Tuple

# Syntax definition (BNF-like format)
# REG_INFO_LIST = REG_INFO {, REG_INFO}
# DEPENDS_BLOCK = depends { REG_INFO_LIST }+
# EXPRESSION = REG_INFO { DEPENDS_BLOCK }+
# REG_INFO = [ Operation(read | write) REGISTER_NAME <SUBFIELD_ABBR RANGE [VALUE] {, SUBFIELD_ABBR RANGE [VALUE]}> ]

# Regex patterns
REGISTER_NAME_PATTERN = r'[A-Za-z0-9_]+'
SUBFIELD_ABBR_PATTERN = r'[A-Za-z0-9_]+'
# RANGE_PATTERN matches a single number (e.g., "4"), a colon-separated range (e.g., "4:0"), a comma-separated range (e.g., "4,0"), or a dash-separated range (e.g., "4-0").
RANGE_PATTERN = r'\d+(?::\d+|,\d+|-\d+)?'
VALUE_PATTERN = r'[A-Za-z0-9_]+|NA'
OPERATION_PATTERN = r'(read|write)'

# Individual subfield pattern: SUBFIELD_ABBR RANGE [VALUE]
SUBFIELD_PATTERN = rf'{SUBFIELD_ABBR_PATTERN}\s+{RANGE_PATTERN}(?:\s+{VALUE_PATTERN})?'

# REG_INFO pattern: Operation REGISTER_NAME <subfields>
REG_INFO_PATTERN = rf'({OPERATION_PATTERN})\s+({REGISTER_NAME_PATTERN})\s+<({SUBFIELD_PATTERN}(?:\s*,\s*{SUBFIELD_PATTERN})*)>'

# REG_INFO_LIST pattern: REG_INFO {, REG_INFO}
REG_INFO_LIST_PATTERN = rf'{REG_INFO_PATTERN}(?:\s*,\s*{REG_INFO_PATTERN})*'

# DEPENDS_BLOCK pattern: depends { REG_INFO_LIST }+
DEPENDS_BLOCK_PATTERN = rf'depends\s+({REG_INFO_LIST_PATTERN})'

# EXPRESSION pattern: REG_INFO { DEPENDS_BLOCK }+
EXPRESSION_PATTERN = rf'^({REG_INFO_PATTERN})(?:\s+{DEPENDS_BLOCK_PATTERN})*$'

def is_valid_expression(s: str) -> bool:
    """
    Check if the input string matches the EXPRESSION_PATTERN.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string matches the EXPRESSION_PATTERN, False otherwise.
    """
    return re.match(EXPRESSION_PATTERN, s.strip()) is not None



def main(filename: str):
    """
    Reads a file line by line and checks if each line matches the EXPRESSION_PATTERN.
    Prints the result for each line.
    """
    with open(filename, 'r') as f:
        for lineno, line in enumerate(f, 1):
            print(line)
            line = line.strip()
            if not line:
                continue
            if is_valid_expression(line):
                print(f"Line {lineno}: VALID")
            else:
                print(f"Line {lineno}: INVALID")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python dependencies_regex.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)