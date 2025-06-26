from pydantic import BaseModel

def script_to_divide_datasheet_by_sections(datasheet):
    """ Prompt for extracting per-register section headers """

    prompt = f"""
        The given text is from a datasheet with tables and normal text.
        Write a python script that divides a datasheet into its sections.
        Think about the identification to use for a section header.
        Find the least common denominator between section headers that is not too restrictive and misses corner cases.
        It should also not result into many false positives.
        Keep in mind that sections can be referenced in other parts of the text with their number and name, and those should be ignored.
        The python script takes as input the text from a datasheet, and returns the text for each section in a list.
        The first line of each section text should be the section header containing the full name of the register.
        Give an explanation of your criteria for identifying headers, then return the Python script.

        The datasheet text is: : {datasheet}
    """
    return prompt
