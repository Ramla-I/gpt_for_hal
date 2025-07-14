# Configuration file for project parameters
from utils.pdf_ops import extract_text_from_pdf, extract_markdown_from_pdf
from utils.file_ops import read_file

# Example: 'e1000' or 'ixgbe'
DRIVER_NAME = "e1000"

# Dictionary mapping driver names to their paths
DRIVER_PATHS = {
    "e1000": "drivers/e1000_ebb2314.rs",
    "ixgbe": "drivers/ixgbe_4a124f4.rs",
}

# Dictionary mapping driver names to their datasheet paths
DATASHEET_PATHS = {
    "e1000": "datasheet/82579/82579_datasheet_143_229.pdf",
    "ixgbe": "datasheet/82599/pf_regs.pdf",
}

VECTOR_STORE_ID = {
    "stm32f407": "vs_687140fd45ec8191810dbb64c4a2dfa0", #file-5gAhRQpG8wXBPgmEkGewac
}

def get_driver_path():
    return DRIVER_PATHS[DRIVER_NAME]

def get_datasheet_path():
    return DATASHEET_PATHS[DRIVER_NAME]

# You can add more configuration parameters as needed 
RUN_CATEGORY = "baseline"
RUN_NUM = 1

DATASHEET_ENCODING = "markdown"

def get_datasheet():
    path = get_datasheet_path()

    if DATASHEET_ENCODING == "text":
        datasheet = extract_text_from_pdf(path)
    elif DATASHEET_ENCODING == "markdown":
        datasheet = extract_markdown_from_pdf(path)
    else:
        raise ValueError(f"Unknown DATASHEET_ENCODING: {DATASHEET_ENCODING}")
    
    return datasheet

def get_driver():
    path = get_driver_path()
    return read_file(path)

BRAKE_AT_EVERY_STEP = "true"