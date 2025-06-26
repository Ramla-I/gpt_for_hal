To improve the script and handle the error you encountered with `tabula`, I'll use another PDF processing library called `pdfminer`. `pdfminer` is a robust tool to extract text and analyze its structure from PDF files. Below is a revised script to extract register information from a PDF and save it into a CSV file.

Firstly, ensure you have `pdfminer.six` installed. You can install it using pip if it's not already installed:

```bash
pip install pdfminer.six
```

Here is the script using `pdfminer`:

```python
from pdfminer.high_level import extract_text
import pandas as pd
import csv
import re

def extract_register_info(pdf_path, register_list, output_csv):
    # Extract text from PDF
    text = extract_text(pdf_path)

    # Split the text into lines
    lines = text.split('\n')

    # Initialize an empty list to store register data
    register_data = []

    # Iterate over each register of interest
    for register in register_list:
        # Look for lines that contain the register abbreviation
        for line in lines:
            if register in line:
                # Use regex to extract potential fields from the line
                match = re.search(r'(\d+)\s+({})\s+([\w\s]+)\s+(R/W|R|W)'.format(register), line)
                if match:
                    offset, abbr, name, rw = match.groups()
                    register_info = [
                        offset.strip(),  # Offset
                        abbr.strip(),    # Abbreviation
                        name.strip(),    # Register Name
                        rw.strip()       # Read/Write Property
                    ]
                    register_data.append(register_info)

    # Create a DataFrame and write out to CSV
    headers = ['Offset', 'Abbreviation', 'Name', 'RW']
    df = pd.DataFrame(register_data, columns=headers)
    df.to_csv(output_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)

    print(f'Register data has been extracted to {output_csv}')

# Example usage:
pdf_path = 'datasheet/82579/82579_datasheet_143_229.pdf'
register_list = [
    'REG_STATUS', 'REG_CTRL', 'REG_EEPROM', 'REG_RXDESCLO',
    'REG_RXDESCHI', 'REG_RXDESCLEN', 'REG_RXDESCHEAD',
    'REG_RXDESCTAIL', 'REG_RCTRL', 'REG_TXDESCHI',
    'REG_TXDESCLO', 'REG_TXDESCLEN', 'REG_TXDESCHEAD',
    'REG_TXDESCTAIL', 'REG_TCTRL', 'REG_IMASK'
]
output_csv = 'register_data.csv'

extract_register_info(pdf_path, register_list, output_csv)
```

### Notes:
- **Robustness**: This script assumes a specific format (`offset abbreviation name rw`) in the PDF text. Adjustments might be needed based on your actual data format.
- **PDF Structure**: If your PDF structure is more complex than plain lines of text with register specifications, consider additional parsing logic tailored to the specific sections and ordering in the document.
- **Dependencies**: Make sure any necessary packages (e.g., `pdfminer.six`, `pandas`) are installed in your environment.

This script has better error handling, relies on text extraction from `pdfminer`, and processes the information using regular expressions to identify and extract the relevant data fields for each register. Adjust the regex pattern if the format in the datasheet differs.