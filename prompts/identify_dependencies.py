from pydantic import BaseModel

class RegisterInfo (BaseModel):
    register_name: str
    subfield_name_abbreviation: str
    bit_range: str
    value: str

class RegisterDependencies (BaseModel):
    dependee_register: RegisterInfo
    dependent_register: RegisterInfo
    relevant_sentence: str

class DependencyInfo (BaseModel):
    dependencies: list[RegisterDependencies]

def identify_inter_register_dependencies(datasheet):
    """ Prompt for identifying inter-register dependencies """

    prompt = f"""
        The given markdown text is from a datasheet with tables and normal text.
        It contains information about device registers.
        Identify dependencies between registers using the information given in the document.
        Here is an example:
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
                    "value": "N/A"}},
                "relevant_sentence": "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
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
                    "value": "1"}},
                "relevant_sentence": "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
            }}]
        }}
    The datasheet text is: : {datasheet}
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
