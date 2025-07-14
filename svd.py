from openai import OpenAI
import prompts
from utils.file_ops import read_file, write_file, read_csv, append_to_file, write_list_of_dicts_to_csv
from utils.pdf_ops import extract_markdown_from_pdf, extract_text_from_pdf
from utils.svd_ops import parse_svd, extract_peripheral_xml_blocks
from generate_code import generate_struct_code, generate_accessor_methods, generate_subfield_accessor_methods, start_struct_impl, end_struct_impl
import llm_generated_scripts
import config
import json
import os
import pipeline_runner

# Set up your OpenAI API key
client = OpenAI()

def call_openai_api(prev_prompts_and_replies, prompt):
    """
    Function to call OpenAI's API and generate a response based on the prompt.
    """
    # build the messages
    messages = []

    # messages.append({ "role": "system", "content": output_format_prompt })
    
    # add the previous questions and answers
    for p, r in prev_prompts_and_replies:
        messages.append({ "role": "user", "content": p })
        messages.append({ "role": "assistant", "content": r })
    
    # add the new question
    messages.append({ "role": "user", "content": prompt })

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=False
    )
    
    content = completion.choices[0].message.content
    # if it starts with ```, remove the first and the last line.
    if content.startswith("```"):
        content = content.split("\n")[1:-1]
        content = "\n".join(content)

    # even if it doen't start with ```, the last line may so check and remove
    if content.endswith("```"):
        content = content.split("\n")[:-1]
        content = "\n".join(content)

    return content


if __name__ == "__main__":
    # datasheet = extract_text_from_pdf("/Users/ramla/Projects/stm32-rs/ref_manual/stm32f405_stm32f415_stm32f407_stm32f417_stm32f427_stm32f437_stm32f429_stm32f439.pdf")
    peripherals = extract_peripheral_xml_blocks("/Users/ramla/Projects/stm32-rs/svd/stm32f407.svd")
    print(len(peripherals))
    input("Press Enter to continue...")

    for peripheral in peripherals:
        # For each peripheral, create a prompt to check for errors/inconsistencies in the datasheet.
        peripheral_name = ""
        import xml.etree.ElementTree as ET
        try:
            # Try to extract the peripheral name from the XML block
            elem = ET.fromstring(peripheral)
            name_elem = elem.find("name")
            if name_elem is not None:
                peripheral_name = name_elem.text.strip()
            else:
                peripheral_name = "UNKNOWN_PERIPHERAL"
        except Exception:
            peripheral_name = "UNKNOWN_PERIPHERAL"

        print(peripheral_name)

        result = client.vector_stores.search(
            vector_store_id=config.VECTOR_STORE_ID["stm32f407"],
            query = "Find information about " + peripheral_name + " in the datasheet",
            max_num_results=1
        )
        # print(result.data[0].content[0].text)
        # input("Press Enter to continue...")
       
        prompt = prompts.find_errors_in_svd(peripheral, result.data[0].content[0].text)
        messages = []
        # add the new question
        messages.append({ "role": "user", "content": prompt })
        completion = client.beta.chat.completions.parse(
            model="gpt-4.1",
            messages=messages,
            response_format=prompts.SVDError
        )
        errors = completion.choices[0].message.content

        # Append the errors output to a file for each peripheral
        with open("output/svd_errors.txt", "a") as f:
            f.write(f"Peripheral: {peripheral_name}\n")
            f.write(f"{errors}\n\n")
