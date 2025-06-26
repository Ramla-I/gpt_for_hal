from openai import OpenAI
import prompts
from utils.file_ops import read_file, write_file, read_csv, append_to_file, write_list_of_dicts_to_csv
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


def main():
    datasheet = config.get_datasheet()
    driver = config.get_driver()

    # Create output directory of driver_name/config.RUN/config.run_num. If it already exists, return an error.
    output_dir = os.path.join(config.DRIVER_NAME, str(config.RUN_CATEGORY), str(config.RUN_NUM))
    if os.path.exists(output_dir):
        raise FileExistsError(f"Output directory '{output_dir}' already exists.")
    else:
        os.makedirs(output_dir)


    initial_inputs = {
        "driver": config.get_driver(),
        "datasheet": config.get_datasheet(),
    }

    pipeline_runner.run_pipeline(output_dir, "prompts.json", initial_inputs)

    # Increment RUN_NUM
    config.RUN_NUM += 1

    # # Extract the used registers from the existing driver.
    # driver = read_file(driver_path)
    # prompt = prompts.extract_regs_from_driver(driver)
    # registers_list = call_openai_api([], prompt)
    # write_file("output/registers_list_e1000.txt", registers_list)

    # Prompt GPT to extract information about those registers.
    # The output should be in a table format.
    # prompt = prompts.extract_table_data(registers_list, datasheet)
    # registers_table = call_openai_api([], prompt)
    # write_file("output/registers_table.csv", registers_table)

    # reg_table = read_csv("output/registers_table.csv")

    # remove any reg with offest set to NA
    # reg_table = [reg for reg in reg_table if reg["Offset"] != "NA"]

    # remove duplicate regs -> move to prompt
    # reg_table = [dict(t) for t in {tuple(d.items()) for d in reg_table}]

    # # Now prompt GPT to find enums for each register.
    # for reg in reg_table:
    #     prompt = prompts.extract_enum_info(reg["Abbreviation"], datasheet)
    #     messages = []
    #     # add the new question
    #     messages.append({ "role": "user", "content": prompt })

    #     completion = client.beta.chat.completions.parse(
    #         model="gpt-4o",
    #         messages=messages,
    #         response_format=prompts.RegisterInfo
    #     )
    #     enum_information = completion.choices[0].message.content
    #     write_file(f"output/{reg['Abbreviation']}_enum_info.csv", enum_information)
    
    # Generate Read/Write masks for each register.
    # for reg in reg_table:
    #     reg["RO mask"] = create_bitmask(reg["RO subfields"])
    #     reg["WO mask"] = create_bitmask(reg["WO subfields"])
    #     reg["RW mask"] = create_bitmask(reg["RW subfields"])

    # # for every ref, if an enum is required for a field, remove it from the write mask.
    # # currently keep it in the read mask.
    # reg_enum_info = {}
    # for reg in reg_table:
    #     # print(reg["Abbreviation"])
    #     enum_info = read_csv(f"output/{reg['Abbreviation']}_enum_info.csv")
    #     # print(enum_info)
    #     # remove all lines with the subfield name "NA" or "Reserved", or if the valid values are "NA"
    #     enum_info = [subfield for subfield in enum_info if (subfield["Subfield name abbreviation"] != "NA") & (subfield["Subfield name abbreviation"] != "Reserved") & (subfield["Valid values"] != "NA")]

    #     for subfield in enum_info:
    #         # print(subfield)
    #         subfield_range = subfield["Subfield range"]
    #         subfield_range = subfield_range.split(":")
    #         # print(subfield_range)
    #         if len(subfield_range) == 1:
    #             subfield_range.append(subfield_range[0])
    #         start, end = map(int, subfield_range)
    #         # print(start, end)
    #         if start > end: # swap
    #             start, end = end, start
    #         for bit in range(start, end + 1):
    #             # print(bit)
    #             reg["WO mask"] &= ~(1 << bit)
    #             reg["RW mask"] &= ~(1 << bit)
        
    #     # print(enum_info)
    #     reg_enum_info[reg["Abbreviation"]] = enum_info
            
    # order registers based on offset
    # ordered_regs = sorted(reg_table, key=lambda x: int(x["Offset"], 16))

    # Run a script to create the register struct from the table.
    # struct_code = generate_struct_code(ordered_regs)
    # write_file("output/registers_struct.rs", struct_code)

    # # As well as the access methods.
    # methods_code = generate_accessor_methods(ordered_regs)
    # append_to_file("output/registers_struct.rs", methods_code)

    # # Now write the per-field access methods where an enum is required
    # enum_defs = ""
    # enum_methods_code = start_struct_impl()
    # for reg in ordered_regs:
    #     enum_defs, enum_methods_code = generate_subfield_accessor_methods(enum_defs, enum_methods_code, reg["Abbreviation"], reg_enum_info[reg["Abbreviation"]])
    #     # print(reg_enum_info[reg["Abbreviation"]])
    #     # print(enum_methods_code)
    #     # print(enum_defs)
    #     # input("Press Enter to continue...")

    # enum_methods_code += end_struct_impl()
    # append_to_file("output/registers_struct.rs", enum_defs)
    # append_to_file("output/registers_struct.rs", enum_methods_code)


    # # Now prompt GPT to divide datasheet by sections
    # prompt = prompts.script_to_divide_datasheet_by_sections(datasheet)
    # messages = []
    # # add the new question
    # messages.append({ "role": "user", "content": prompt })
    # completion = client.beta.chat.completions.parse(
    #     model="gpt-4.1",
    #     messages=messages,
    # )
    # script_divide_datasheet = completion.choices[0].message.content
    # output_path = "llm_generated_scripts/divide_datasheet_into_sections_e1000.py"
    # with open(output_path, "w") as f:
    #     f.write(script_divide_datasheet)
    
    # # Now prompt GPT to find dependencies between registers.
    # # registers_list = read_file("output/registers_list1.txt")
    # datasheet_sections = llm_generated_scripts.split_datasheet_sections(datasheet)
    # print(len(datasheet_sections))
    # for i, section in enumerate(datasheet_sections):
    #     prompt = prompts.identify_inter_register_dependencies(section)
    #     messages = []
    #     # add the new question
    #     messages.append({ "role": "user", "content": prompt })
    #     completion = client.beta.chat.completions.parse(
    #         model="gpt-4.1",
    #         messages=messages,
    #         response_format=prompts.DependencyInfo
    #     )
    #     dependency_information = completion.choices[0].message.content
    #     # print(dependency_information)
    #     append_to_file("output/dependency_information_e1000", dependency_information + "\n")


    # # Read JSON objects from the specified file
    # dependency_info_path = "/Users/ramla/Projects/gpt_for_hal/output/dependency_information_relevant_regs_e1000"
    # with open(dependency_info_path, "r") as f:
    #     dependency_json_objects = [json.loads(line) for line in f if line.strip()]

    # prompt = prompts.categorize_dependencies(dependency_json_objects)
    # messages = []
    # # add the new question
    # messages.append({ "role": "user", "content": prompt })
    # completion = client.beta.chat.completions.parse(
    #     model="gpt-4.1",
    #     messages=messages,
    # )
    # categorized_dependencies = completion.choices[0].message.content
    # print(categorized_dependencies)

    # output_path = "output/categorized_dependencies_e1000.json"
    # with open(output_path, "w") as f:
    #     f.write(categorized_dependencies)

    # #  # Read JSON objects from the specified file
    # dependency_info_path = "/Users/ramla/Projects/gpt_for_hal/output/categorized_dependencies_sw_e1000.json"
    # with open(dependency_info_path, "r") as f:
    #     dependency_json_objects = [json.loads(line) for line in f if line.strip()]

    # prompt = prompts.lt_dependencies(dependency_json_objects)
    # messages = []
    # messages.append({ "role": "user", "content": prompt })
    # completion = client.beta.chat.completions.parse(
    #     model="gpt-4.1",
    #     messages=messages,
    # )
    # categorized_dependencies = completion.choices[0].message.content

    ## Don't like this because I can't control what is queried
    # categorized_dependencies = client.responses.create(
    #     model="gpt-4o",
    #     input=prompt,
    #     tools=[{
    #         "type": "file_search",
    #         "vector_store_ids": ["vs_685c5d3b1e248191833767a593335567"]
    #     }]
    # )
    # print(categorized_dependencies)


    # output_path = "output/lt_dependencies_e1000_2ex_no_vs.json"
    # with open(output_path, "w") as f:
    #     f.write(categorized_dependencies)

    # # INSERT_YOUR_CODE
    # # Create (and clear) the output file before appending results
    # output_path = "output/lt_dependencies_e1000_vs.json"
    # f_out = open(output_path, "w")
    # vector_store_id = "vs_685c5d3b1e248191833767a593335567"
    # # query for each JSON object
    # with open(dependency_info_path, "r") as f:
    #     for line in f:
    #         if line.strip():
    #             dependency_json_object = json.loads(line)
    #             dependent_register = dependency_json_object.get("dependent_register")
    #             dependee_register = dependency_json_object.get("dependee_register")
    #             # query vector store
    #             result = client.vector_stores.search(
    #                 vector_store_id=vector_store_id,
    #                 query = "find information related to " + str(dependee_register) + " and " + str(dependent_register),
    #                 max_num_results=1
    #             )

    #             # print(result.data[0].content[0].text)
    #             prompt = prompts.lt_dependency(dependency_json_object, result.data[0].content[0].text)
    #             messages = []
    #             # add the new question
    #             messages.append({ "role": "user", "content": prompt })
    #             completion = client.beta.chat.completions.parse(
    #                 model="gpt-4.1",
    #                 messages=messages,
    #             )
                
    #             categorized_dependency = completion.choices[0].message.content
    #             f_out.write(categorized_dependency.strip() + "\n")
                                
    
if __name__ == "__main__":
    main()