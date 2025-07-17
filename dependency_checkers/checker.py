import json
import re
import pdfplumber

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"
    return all_text

def find_register_pairs_nearby(pdf_text, register_pairs, max_distance=5):
    words = re.findall(r'\w+', pdf_text.lower())
    matches = []

    for reg1, reg2 in register_pairs:
        reg1 = reg1.lower()
        reg2 = reg2.lower()

        positions = [i for i, w in enumerate(words) if w in (reg1, reg2)]

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                idx1, idx2 = positions[i], positions[j]
                if abs(idx1 - idx2) <= max_distance:
                    start = max(0, min(idx1, idx2) - 5)
                    end = min(len(words), max(idx1, idx2) + 6)
                    snippet = ' '.join(words[start:end])
                    if reg1 in snippet and reg2 in snippet:
                        matches.append((reg1, reg2, snippet))
                    break  # one match is enough per pair
    return matches

def load_register_pairs_from_file(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    pairs = []
    for entry in data['dependencies']:
        r1 = entry['dependee_register']['register_name']
        r2 = entry['dependent_register']['register_name']
        pairs.append((r1, r2))
    return pairs

# Example usage
if __name__ == "__main__":
    pdf_path = "../datasheet/82579/82579_datasheet_143_229.pdf"            # Your PDF document
    json_path = "gemini.json"      # Your structured JSON input
    max_distance = 20                    # Max words apart

    register_pairs = load_register_pairs_from_file(json_path)
    pdf_text = extract_text_from_pdf(pdf_path)
    found_matches = find_register_pairs_nearby(pdf_text, register_pairs, max_distance)

    print(f"\nFound {len(found_matches)} register pair match(es):\n")
    for i, (reg1, reg2, snippet) in enumerate(found_matches, 1):
        print(f"{i}. [{reg1}] and [{reg2}] found in:\n   \"{snippet}\"\n")
