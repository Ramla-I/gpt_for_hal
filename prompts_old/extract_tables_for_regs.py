from openai import OpenAI, OpenAIError
import os

client = OpenAI()


def extract_table_data(reg_list_file, datasheet_pdf, registers_summary_path):
    """ Prompt for extracting data in CSV format """

    prompt = (
        "Given the following PDF text, identify and extract the 'Registers Summary PF — BAR 0' table only.\n"
        "If the table is not found in the data below, then extract all information, as long as it matches the format below:\n\n"
        "Offset,Abbreviation,Name,Block,RW,Reset,Page\n\n"
        "Extract all the rows and provide them in a clean, CSV format.\n\n"
        "The table has multiple subsections, so skip this text if needed and continue with the same format extraction.\n"
        "Continue extracting data unless you encounter information that does not follow the specified format.\n\n"
        "Please remove all the spaced after commas; When parsing the Offset, you might encounter hex expressions type of 0x0E800+4*n, n=1..3.\n"
        "Since hanving comma in parsing such epxressions would ruin the CSV format, please format these addresses to 0x0E800+4*n&n=1..3 (use & instead).\n"
        "For the Nname column, make sure that there are not (...) or [...] inside. Please remove them and leave only text beyond.\n\n"
        "Return only the extracted data, with no additional comments or explanations; not csv word in the bginning or anything.\n"
        "Your output should be able to completely be copied to a CSV file!\n\n"
        "The header line is not needed in the extracted data; it is already present in the file.\n\n"
        f"{pdf_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert data extractor."},
                {"role": "user", "content": prompt}
            ],
        )

        table_data = response.choices[0].message.content.strip()
        table_data = table_data.replace("```", "").strip()
        
        # Append the data to the CSV file
        with open(registers_summary_path, mode='a', newline='', encoding='utf-8') as file:
            file.write(table_data + '\n')

        print(f"CSV data successfully written to {registers_summary_path}")

    except OpenAIError as e:
        raise RuntimeError(f"An error occurred while making a request to OpenAI: {e}")
