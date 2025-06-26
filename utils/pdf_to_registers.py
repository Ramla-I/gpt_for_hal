import PyPDF2
import re
import os
from pathlib import Path
import pymupdf4llm

def extract_markdown_text_from_pdf(pdf_path):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text

def extract_register_sections(text):
    """Extract register sections with their names and details."""
    # Pattern to match the complete register header format:
    # section_number register_name - ABBREVIATION (address; access)
    register_pattern = r'(\d+\.\d+\.\d+\.\d+\.\d+)\s+([^-]+)\s*-\s*([^(]+)\s*\(([^;]+);\s*([^)]+)\)(?:\n|$)(.*?)(?=\d+\.\d+\.\d+\.\d+\.\d+|$)'
    
    # Find all register sections
    matches = re.finditer(register_pattern, text, re.DOTALL)
    
    registers = {}
    for match in matches:
        register_number = match.group(1)
        register_name = match.group(2).strip()
        abbreviation = match.group(3).strip()
        address = match.group(4).strip()
        access = match.group(5).strip()
        content = match.group(6).strip()
        
        # Create a key that includes all register details
        register_key = (register_number, register_name, abbreviation, address, access)
        registers[register_key] = content
    
    return registers

def sanitize_filename(name):
    """Convert string to valid filename."""
    # Replace invalid filename characters with underscores
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', name)

def save_register_files(registers, output_dir):
    """Save each register section to a separate markdown file."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for (register_number, register_name, abbreviation, address, access), content in registers.items():
        # Create filename from register number and abbreviation
        safe_abbr = sanitize_filename(abbreviation)
        filename = f"{register_number.replace('.', '_')}_{safe_abbr}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Write content to file with detailed header
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Register {register_number}: {register_name}\n\n")
            f.write(f"**Abbreviation:** {abbreviation}\n")
            f.write(f"**Address:** {address}\n")
            f.write(f"**Access:** {access}\n\n")
            f.write("## Description\n\n")
            f.write(content)

def process_pdf_datasheet(pdf_path, output_dir):
    """Main function to process PDF datasheet."""
    try:
        # Extract text from PDF
        print(f"Extracting text from {pdf_path}...")
        markdown_text = extract_markdown_text_from_pdf(pdf_path)
        print(markdown_text)

        # Split into registers
        # print("Splitting into register sections...")
        # registers = extract_register_sections(markdown_text)
        
        # # Save register files
        # print(f"Saving register files to {output_dir}...")
        # save_register_files(registers, output_dir)
        
        # print(f"Successfully processed {len(registers)} registers!")
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert PDF datasheet to register markdown files')
    parser.add_argument('pdf_path', help='Path to the PDF datasheet')
    parser.add_argument('--output-dir', default='registers', help='Output directory for register files')
    
    args = parser.parse_args()
    
    process_pdf_datasheet(args.pdf_path, args.output_dir)