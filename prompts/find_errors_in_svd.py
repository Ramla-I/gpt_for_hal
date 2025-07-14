from pydantic import BaseModel

class SVDError (BaseModel):
    error_type: str
    error_description: str
    error_location: str
    peripheral_name: str
    register_name: str

class SVDErrorValidated (BaseModel):
    error_type: str
    error_description: str
    error_location: str
    peripheral_name: str
    register_name: str
    validated: bool
    explanation: str




def find_errors_in_svd(svd, peripheral_info_from_datasheet):
    """ Prompt for identifying inter-register dependencies """

    prompt = f"""
    You are an expert in embedded systems and microcontroller documentation. You are given the following peripheral SVD XML block and the some datasheet information about the peripheral.

    Peripheral SVD XML:
    {svd}

    Peripheral information from datasheet:
    {peripheral_info_from_datasheet}

    Your task is to check for errors/inconsistencies in the SVD file.

    Return a list of errors/inconsistencies in the following format:

    [
        {{
            "error_type": "error_type",
            "error_description": "error_description",
            "error_location": "error_location",
            "peripheral_name": "peripheral_name",
            "register_name": "register_name"
        }}
    ]

    The error_type should be one of the following:

    - "missing_register"
    - "missing_field"
    - "missing_enum"
    - "missing_description"
    - "incorrect_description"
    - "incorrect_register_name"
    - "incorrect_field_name"
    - "incorrect_enum_name"
    - "incorrect_enum_value"
    - "incorrect_enum_description"
    - "incorrect_enum_range"
    - "other"

    
    The error location should be the name of the register, field, or enum that is in error.
    Do not make up any information. Only use the information provided in the datasheet. If there are no errors, return an empty list.
    """
    return prompt


