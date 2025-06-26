table_name = "Registers Summary PF — BAR 0"
table_header = "Offset,Abbreviation,Name,Block,RW,Reset,Page"

# output_table_header = " Name,Name in List,Abbreviation,Offset,R/W restrictions,RO subfields,WO subfields,RW subfields,Page"
output_table_header = "Offset,Abbreviation,Name,RW"
table_header_fields = output_table_header.split(",")

def create_script(registers_list, datasheet, old_script):
    """ Prompt for extracting data from the datasheet in CSV format """

    prompt = f"""
        The given PDF text is from a datasheet: {datasheet}.
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        Write a python function which will have the following features:
        - It's input will be the path to the datasheet and a list of registers
        - The output will be a CSV file with the following headers {output_table_header}

        Consider the format of the table in the datasheet to write the script correctly. Use another tool besides pdfplumber.

        This is the old script you generated which had the error "AttributeError: module 'tabula' has no attribute 'read_pdf'": {old_script}
        Make sure the new script improves on this error.

    """

    return prompt

        # The python code must identify the registers from the datasheet and extract the following information:
        #     1. Name
        #     3. Abbreviation of the register
        #     4. Offset in the address space
        #     5. If the register is Read-Only, Write-Only or Read/Write.
        #     6. RO subfields of the register. Write the ranges between 0 and 31 that are RO, with a space between the ranges. Put an NA if there are no RO subfields.
        #     7. WO subfields of the register. Write the ranges between 0 and 31 that are WO, with a space between the ranges. Put an NA if there are no WO subfields.
        #     8. RW subfields of the register. Write the ranges between 0 and 31 that are RW, with a space between the ranges. Put an NA if there are no RW subfields.
        #     9. Page number that the register table is located at.     