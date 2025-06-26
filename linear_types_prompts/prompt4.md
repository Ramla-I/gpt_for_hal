Change: Use structured outputs

Prompt:

The given PDF text is from a datasheet.
It contains a table that lists all the registers and their offsets.
It also contains a per-table register with information about the register subfields.
For each pair of registers, identify if there is an explicit dependency between them.
That means the value of one register must be set to a specific value before the other register can be set to a specific value.
For example, for the RDH register the datasheet states that "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
This means there is a dependency between the RDH and CTRL registers and between the RDH and RCTL registers.
The output would be formatted as: 
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
               {{"register_name": "RCTL",
               "subfield_name_abbreviation": "EN",
               "bit_range": "1"
               "value": "1"}}
         }}]
   }}
   datasheet: {datasheet}

Response:
{"dependencies":[{"dependee_register":{"register_name":"CTRL","subfield_name_abbreviation":"SWRST","bit_range":"26","value":"1"},"dependent_register":{"register_name":"RDH","subfield_name_abbreviation":"N/A","bit_range":"N/A","value":"N/A"}},{"dependee_register":{"register_name":"RDH","subfield_name_abbreviation":"N/A","bit_range":"N/A","value":"N/A"},"dependent_register":{"register_name":"RCTL","subfield_name_abbreviation":"EN","bit_range":"1","value":"1"}}]}

Note:
Again, same examples as input