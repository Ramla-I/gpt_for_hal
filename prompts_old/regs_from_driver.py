## ChatGPT Prompt: "create a python file in which we use openAI API to call gpt-40 and asks it to find the registers accessed with a driver file that we attach in the message"

from openai import OpenAI
from utils.file_ops import read_file

client = OpenAI()

def analyze_registers(driver_content, output_file):
    """
    Uses OpenAI's GPT-4 to analyze the driver file and identify accessed registers.
    """
    prompt = (
        "Analyze the following driver file content and identify any hardware registers "
        "accessed. If the register offset is only listed, but not used in the code, do not include it in the list."
        "Please only provide the name of the registers, one on each line. Do not include any additional information."
        # Please provide a summary listing each register accessed "
        # "and, if possible, the context in which it is accessed.\n\n"
        "Driver Content:\n\n" + driver_content
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing device drivers and low-level hardware interactions."},
                {"role": "user", "content": prompt}
            ],
            # max_tokens=1500  # Adjust based on the length of expected output
            # temperature=0.5  # Adjust based on the desired creativity vs accuracy
        )
        
        analysis_result = response.choices[0].message.content.strip()

         # Write the analysis to the output file with one register per line
        with open(output_file, 'w') as file:
            # Split the response into lines, assuming each register is listed in the output
            for line in analysis_result.splitlines():
                file.write(line + "\n")

        print(f"Analysis written to {output_file}")

    except Exception as e:
        print("Error during API call:", e)
        return None

def main():
    # Replace with the path to your driver file
    driver_file_path = "../drivers/e1000_ebb2314.rs"
    # Specify the output file for the analysis
    output_file = "../output/register_list.txt"

    driver_content = read_file(driver_file_path)
    
    if driver_content:
        analyze_registers(driver_content, output_file)
    else:
        print("Failed to read the driver file.")

if __name__ == "__main__":
    main()
