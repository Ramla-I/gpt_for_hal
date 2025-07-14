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
    # peripherals = extract_peripheral_xml_blocks("/Users/ramla/Projects/stm32-rs/svd/stm32f407.svd")
    output_file = read_file("output/svd_errors.txt").split("\n")

    # Store the next line after the name (i.e., the error description for each peripheral)
    peripheral_errors = {}
    last_peripheral = None
    for idx, line in enumerate(output_file):
        if line.startswith("Peripheral:"):
            last_peripheral = line.split(":", 1)[1].strip()
            # The next line is the error description (if it exists and is not empty)
            if idx + 1 < len(output_file):
                error_line = output_file[idx + 1].strip()
                if error_line:
                    peripheral_errors[last_peripheral] = error_line

    for e in peripheral_errors:
        # print(e)
        # print(peripheral_errors[e])

        result = client.vector_stores.search(
            vector_store_id=config.VECTOR_STORE_ID["stm32f407"],
            query = "Find information related to this reported errot in the SVD file:" + peripheral_errors[e],
            max_num_results=1
        )


        prompt = "validate the error discovered for the peripheral " + e + " in the SVD file:" + peripheral_errors[e] + "with the following information from the datasheet:" + result.data[0].content[0].text + "and return the error in the original format with an additional field 'validated' which is true if the error is valid and false if it is invalid and a field 'explanation' which is the explanation for the validation"
        messages = []
        # add the new question
        messages.append({ "role": "user", "content": prompt })
        completion = client.beta.chat.completions.parse(
            model="gpt-4.1",
            messages=messages,
            response_format=prompts.SVDErrorValidated
        )
        errors = completion.choices[0].message.content

        # Append the errors output to a file for each peripheral
        with open("output/svd_errors_validated.txt", "a") as f:
            f.write(f"Peripheral: {e}\n")
            f.write(f"{errors}\n\n")
