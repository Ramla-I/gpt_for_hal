from pydantic import BaseModel

class RegisterInfo (BaseModel):
    register_name: str
    subfield_name_abbreviation: str
    bit_range: str
    value: str

class RegisterDependencies (BaseModel):
    dependee_register: RegisterInfo
    dependent_register: RegisterInfo

class DependencyInfo (BaseModel):
    dependencies: list[RegisterDependencies]

def identify_inter_register_dependencies(datasheet, registers_list):
    """ Prompt for identifying inter-register dependencies """

    prompt = f"""
        The given PDF text is from a datasheet: {datasheet}
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        It details explicit dependencies between registers. 
        I will give some examples of such dependencies, and then state the task.

        ** Example 1 ** 
        For the RDH register the datasheet states:
            "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
        This means there is a dependency between the RDH and CTRL registers and between the RDH and RCTL registers.
        The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "CTRL",
                        "subfield_name_abbreviation": "SWRST",
                        "bit_range": "26"
                        "value": "1"}},
                    "dependent_register":
                        {{"register_name": "RDH",
                        "subfield_name_abbreviation": "RDH",
                        "bit_range": "15:0"
                        "value": "N/A"}}
                }},
                {{
                    "dependee_register": 
                        {{"register_name": "RDH",
                        "subfield_name_abbreviation": "RDH",
                        "bit_range": "15:0"
                        "value": "N/A"}},
                    "dependent_register":
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "1"}}
                }}]
            }}
        ** Example 1 end **

        ** Example 2 **
        For the RXCSUM register the datasheet states: 
            "This register should only be initialized (written) when the receiver is not enabled (e.g. only write this register when RCTL.EN = 0)"
        This means there is a dependency between the RXCSUM register and the RCTL.EN bit.

         The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "0"}},
                    "dependent_register":
                        {{"register_name": "RXCSUM",
                        "subfield_name_abbreviation": "RXCSUM",
                        "bit_range": "31:0"
                        "value": "N/A"}}
                }}]
            }}
        ** Example 2 end **

        ** Example 3 **
        For the MRQC register the datasheet states: 
            "This field can be modified only when receive to host is not enabled (RCTL.EN = 0)"
        This means there is a dependency between the MRQC register and the RCTL.EN bit.

         The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "0"}},
                    "dependent_register":
                        {{"register_name": "MRQC",
                        "subfield_name_abbreviation": "MRxQueue",
                        "bit_range": "1:0"
                        "value": "N/A"}}
                }}]
            }}
        ** Example 3 end **

        ** Example 4 ** 
        For the TDH register the datasheet states:
            "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the transmit function (TCTL.EN)"
        This means there is a dependency between the TDH and CTRL registers and between the TDH and TCTL registers.
        The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "CTRL",
                        "subfield_name_abbreviation": "SWRST",
                        "bit_range": "26"
                        "value": "1"}},
                    "dependent_register":
                        {{"register_name": "TDH",
                        "subfield_name_abbreviation": "TDH",
                        "bit_range": "15:0"
                        "value": "N/A"}}
                }},
                {{
                    "dependee_register": 
                        {{"register_name": "TDH",
                        "subfield_name_abbreviation": "TDH",
                        "bit_range": "15:0"
                        "value": "N/A"}},
                    "dependent_register":
                        {{"register_name": "TCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "1"}}
                }}]
            }}
        ** Example 4 end **

        ** Task **
        Find all such explicit inter-register dependencies for the CTRL register in the given datasheet and list them.
        An explicit dependency means that a register subfield must be updated before another register subfield can be updated.

    """
    return prompt


"must also set"
"must be set"
" The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
"This register should only be initialized (written) when the receiver is not enabled (e.g. only write this register when RCTL.EN = 0)."
"This field can be modified only when receive to host is not enabled (RCTL.EN = 0)"
"BSIZE is only used when DTYP – 00"
"BSIZE is not relevant when the FLXBUF is other than 0"
"he only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the transmit function (TCTL.EN)"
"If Padding of short packets is allowed, the value in TX descriptor length field should be not less than 17 bytes."
