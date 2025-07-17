from utils.file_ops import read_file, write_file, read_csv, append_to_file, write_list_of_dicts_to_csv
from generate_code import generate_dependencies, generate_struct_code, generate_accessor_methods, generate_subfield_accessor_methods, start_struct_impl, end_struct_impl, create_bitmask, parse_to_int
import llm_generated_scripts
import config
import json
from guardrails import guardrail_overlapping_masks, guardrail_valid_bitrange

driver_name = config.DRIVER_NAME
driver_path = config.get_driver_path()
datasheet_path = config.get_datasheet_path()



def main():
    datasheet = config.get_datasheet()
    driver = config.get_driver()


    reg_table = read_csv("output/e1000/registers_table_human_verified.csv")

    # remove any reg with offest set to NA
    # LLM UPDATE -> could reprompt to see if hallucination and recover missing address
    reg_table = [reg for reg in reg_table if reg["Offset"] != "NA"]

    # # remove duplicate regs and keep in the same order as before
    # # LLM UPDATE -> prompt should request no duplicates
    # seen = set()
    # unique_reg_table = []
    # for reg in reg_table:
    #     reg_tuple = tuple(reg.items())  # tuple() converts the dict items to an immutable sequence so it can be added to a set for deduplication
    #     if reg_tuple not in seen:
    #         seen.add(reg_tuple)
    #         unique_reg_table.append(reg)
    # reg_table = unique_reg_table
    
    # Generate Read/Write masks for each register.
    for reg in reg_table:
        reg["RO mask"] = create_bitmask(reg["RO subfields"])
        reg["WO mask"] = create_bitmask(reg["WO subfields"])
        reg["RW mask"] = create_bitmask(reg["RW subfields"])

        # guardrail
        wo, rw = guardrail_overlapping_masks(reg["RO mask"], reg["WO mask"], reg["RW mask"], reg["Abbreviation"])
        reg["WO mask"] = wo
        reg["RW mask"] = rw
        
        # # Print reg, but print the mask fields in hex
        # reg_print = reg.copy()
        # for mask_field in ["RO mask", "WO mask", "RW mask"]:
        #     reg_print[mask_field] = hex(reg_print[mask_field])
        # print(reg_print)

    # print(reg_table)

    ## add guard rail if RO and there's a non zero write mask
    
    # for every reg, if an enum is required for a field, remove it from the write mask.
    # currently keep it in the read mask.
    for reg in reg_table:
        try:
            with open(f"output/e1000/enum_human_checked/{reg['Abbreviation']}_enum_info.json", "r") as f:
                enum_info = json.load(f)
        except FileNotFoundError:
            # print(f"Info: File not found for register {reg['Abbreviation']}: output/e1000/enum/{reg['Abbreviation']}_enum_info.json")
            continue
            
        if not enum_info["subfields"]:
            # print(f"Register {reg['Abbreviation']} has no candidate subfields for enum extraction.")
            continue

        print(f"Info: Writing enums for register {reg['Abbreviation']}")

        # filter out invalid formats, could be false negatives but thats ok
        # subfields = [sf for sf in enum_info["subfields"] 
        #     if sf["subfield_name_abbreviation"] != "NA"
        #     and sf["subfield_name_abbreviation"].lower() != "reserved" 
        #     and guardrail_valid_bitrange(sf["bit_range"]) 
        #     and sf["valid_values"]
        #     and sf["valid_values"] != "NA"
        #     and all(v["value"].isdigit() for v in sf["valid_values"])
        # ] 

        subfields = []
        for sf in enum_info["subfields"]:
            if (
                sf["subfield_name_abbreviation"] != "NA"
                and sf["subfield_name_abbreviation"].lower() != "reserved"
                and guardrail_valid_bitrange(sf["bit_range"], reg["Abbreviation"], sf["subfield_name_abbreviation"])
                and sf.get("valid_values")
                and sf["valid_values"] != "NA"
            ):
                parsed_values = []
                seen_names = set()
                valid = True
                for v in sf["valid_values"]:
                    name = v["name"].lower()
                    if name in seen_names:
                        valid = False  # Duplicate name found
                        break
                    seen_names.add(name)

                    parsed = parse_to_int(v["value"])
                    if parsed is None:
                        valid = False
                        break

                    v["value"] = parsed
                    parsed_values.append(v)

                if valid and len(parsed_values) > 1:
                    sf["valid_values"] = parsed_values
                    subfields.append(sf)


        if not subfields:
            # print(f"After formatting, register {reg['Abbreviation']} has no candidate subfields for enum extraction.")
            continue
    
        # don't allow generic writes to these bits anymore
        for sf in subfields:
            sf_range = create_bitmask(sf["bit_range"])
            if sf["type"] == "RW":
                reg["RW mask"] &= ~sf_range
            elif sf["type"] == "RO":
                reg["RO mask"] &= ~sf_range
            elif sf["type"] == "WO":
                reg["WO mask"] &= ~sf_range
            else:
                print("Warning: Invalid subfield type")

        reg["subfields"] = subfields
            
    # order registers based on offset
    ordered_regs = sorted(reg_table, key=lambda x: int(x["Offset"], 16))

    output_file = "output/e1000/registers_struct_human_checked.rs"

    # write dependencies
    dependencies = generate_dependencies();
    write_file(output_file, dependencies)

    # Run a script to create the register struct from the table.
    struct_code = generate_struct_code(ordered_regs)
    append_to_file(output_file, struct_code)

    # As well as the access methods.
    methods_code = generate_accessor_methods(ordered_regs)
    append_to_file(output_file, methods_code)

    # Now write the per-field access methods where an enum is required
    enum_defs = ""
    enum_methods_code = start_struct_impl()
    for reg in ordered_regs:
        if reg.get("subfields"):
            enum_defs, enum_methods_code = generate_subfield_accessor_methods(enum_defs, enum_methods_code, reg["Abbreviation"], reg["subfields"])
    enum_methods_code += end_struct_impl()
    append_to_file(output_file, enum_defs)
    append_to_file(output_file, enum_methods_code)

    
if __name__ == "__main__":
    main()