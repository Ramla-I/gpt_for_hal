from pydantic import BaseModel

output_table_header = "Subfield name abbreviation,Subfield range,Valid values"
table_header_fields = output_table_header.split(",")

class ValidValue (BaseModel):
    name: str
    value: str

class SubfieldInfo (BaseModel):
    bit_range: str
    subfield_name_abbreviation: str
    valid_values: list[ValidValue]

class RegisterInfo (BaseModel):
    register_name_abbreviation: str
    subfields: list[SubfieldInfo]

def extract_enum_info(register_name, datasheet):
    """ Prompt for extracting data from the datasheet in CSV format """

    prompt = f"""
        The given PDF text is from a datasheet.
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        Identify and extract the following information for the register: {register_name}.
        Do not include any reserved subfields, read-only (RO) subfields, or subfields that have a bit range with a length of 1, meaning there is no : in the Bit column.
        For this register you must identify the following information: 
            1. The bit range of each subfield, found in the Bit column of the table. If it's missing, put a "NA".
            2. The name abbreviation of the subfields of the register, found in the Description column. If it's missing, put a "NA".
            3. The valid values that can be written to each subfield, found in the Description column. Output this in the format "name of val1=val1;name of val2=val2;...". The name should be on the left of the equal sign and the numerical value on the right.
        datasheet: {datasheet}

    """

    return prompt


    prompt_csv = f"""
        The given PDF text is from a datasheet.
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        Identify and extract the following information for the register: {register_name}.
        For this register you must identify the following information: 
            1. The bit range of each subfield, found in the Bit column of the table. If it's missing, put a "NA".
            2. The name abbreviation of the subfields of the register, found in the Description column. If it's missing, put a "NA".
            3. The valid values that can be written to each subfield, found in the Description column. Output this in the format "name of val1=val1;name of val2=val2;...". The name should be on the left of the equal sign and the numerical value on the right. If it's missing, put a "NA".
        Then write this information in a CSV format with the following headers:
            {output_table_header}
        The first line should be the table header followed by the table in csv format, nothing else should be in the output.

        datasheet: {datasheet}

    """

# Notes:
# - asking GPT to leave out subfields with only one bit in the bit range is not working. It's still returning them.
# - moving the restrictions on the output (which subfields not to include) to earlier in the prompt doesn't seem to make a difference