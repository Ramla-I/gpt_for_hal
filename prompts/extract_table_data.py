table_name = "Registers Summary PF — BAR 0"
table_header = "Offset,Abbreviation,Name,Block,RW,Reset,Page"

output_table_header = " Name,Name in List,Abbreviation,Offset,R/W restrictions,RO subfields,WO subfields,RW subfields,Page"
table_header_fields = output_table_header.split(",")

def extract_table_data(registers_list, datasheet):
    """ Prompt for extracting data from the datasheet in CSV format """

    prompt = f"""
        The given PDF text is from a datasheet.
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        Identify and extract the following information for the registers in {registers_list}.
        Note that the name in this list and in the datasheet may not match exactly.
        For each register you must identify the following fields: 
            1. Name. Put the name as it is given in the datasheet 
            2. Name as given in the register list we provide.
            3. Abbreviation of the register
            4. Offset in the address space
            5. If the register is Read-Only, Write-Only or Read/Write.
            6. RO subfields of the register. Write the ranges between 0 and 31 that are RO, with a space between the ranges. Put an NA if there are no RO subfields.
            7. WO subfields of the register. Write the ranges between 0 and 31 that are WO, with a space between the ranges. Put an NA if there are no WO subfields.
            8. RW subfields of the register. Write the ranges between 0 and 31 that are RW, with a space between the ranges. Put an NA if there are no RW subfields.
            9.Page number that the register table is located at.     
        Then write this information in a CSV format with the following headers:
            {output_table_header}
        The first line should be the table header followed by the table in csv format, nothing else should be in the output.
        If any information is missing, put a NA in the corresponding field.

        datasheet: {datasheet}

    """

    return prompt