def extract_regs_from_driver(driver_text):
    """
    A prompt to analyze the driver file and identify accessed registers.
    This is to narrow the scope of the HAL.
    """

    prompt = f"""
        Analyze the following driver file content and identify any hardware registers accessed. 
        If the register offset is only listed, but not used in the code, do not include it in the list.
        Only provide the name of the registers, one on each line.
        If a register is accessed multiple times, list it only once.
        If there is a standard prefix to every register, e.g., "REG_", remove it.
        Do not include any additional information."
        Driver Content: 
        {driver_text}
    """

    return prompt