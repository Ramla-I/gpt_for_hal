import json
import pdfplumber
import csv
import re

def extract_sentences_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract body text
            text = page.extract_text()
            if text:
                all_text += text + " "

            # Extract tables and flatten them into text
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    line = ' '.join(cell.strip() if cell else '' for cell in row)
                    if line:
                        all_text += line + " "

    # Split into sentences (rough but effective)
    sentences = re.split(r'(?<=[.?!])\s+', all_text.strip())
    cleaned_sentences = [s.strip() for s in sentences if s.strip()]

    # Write sentences to datasheet.txt
    with open("datasheet.txt", "w", encoding="utf-8") as f:
        for sentence in cleaned_sentences:
            f.write(sentence + "\n")

    return cleaned_sentences

def load_dependencies_with_sentences(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["dependencies"]

def find_exact_match(input_sentence, pdf_lines):
    input_clean = input_sentence.strip().lower()
    for line in pdf_lines:
        if input_clean == line.strip().lower():
            return line.strip()
    return "NOT FOUND"

def find_best_sentence_match(input_sentence, pdf_sentences):
    input_clean = input_sentence.strip().lower()

    # Try exact match
    for sentence in pdf_sentences:
        if input_clean == sentence.strip().lower():
            return sentence.strip(), "exact"

    # Try partial match
    for sentence in pdf_sentences:
        if input_clean in sentence.strip().lower():
            return sentence.strip(), "partial"

    return "NOT FOUND", "none"

def save_results_to_csv(dependencies, pdf_sentences, output_file="output.csv"):
    total = len(dependencies)
    matched = 0

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Dependee Register",
            "Dependent Register",
            "Input Line",
            "Matched Line",
            "Match Type"
        ])

        for dep in dependencies:
            dependee = dep.get("dependee_register", {}).get("register_name", "N/A")
            dependent = dep.get("dependent_register", {}).get("register_name", "N/A")
            sentence = dep.get("relevant_sentence", "").strip()

            matched_sentence, match_type = find_best_sentence_match(sentence, pdf_sentences)
            if match_type != "none":
                matched += 1

            writer.writerow([
                dependee,
                dependent,
                sentence,
                matched_sentence,
                match_type
            ])

    print(f"\nTotal items in input: {total}")
    print(f"Total matches found in PDF (exact or partial): {matched}")
# Example usage
if __name__ == "__main__":
    pdf_path = "../datasheet/82579/82579_datasheet_143_229.pdf"            # Your PDF document
    json_path = "gemini2.json"         # Your PDF file

    dependencies = load_dependencies_with_sentences(json_path)
    pdf_lines = extract_sentences_from_pdf(pdf_path)
    save_results_to_csv(dependencies, pdf_lines)
