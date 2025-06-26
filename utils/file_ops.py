import tiktoken
from utils.pdf_ops import extract_text_from_pdf
import csv

def read_file(file_path):
    """
    Reads the content of the file to be analyzed.
    """
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """
    Writes the content to a file.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def append_to_file(file_path, content):
    """
    Appends the content to a file.
    """
    with open(file_path, 'a') as file:
        file.write(content)
        
def count_gpt_tokens_in_file(file_path, model_name='gpt-4o'):
    """
    Counts the number of GPT tokens in a file.
    
    Args:
        file_path (str): Path to the file to be tokenized.
        model_name (str): Name of the OpenAI model for tokenization. Default is 'gpt-4'.

    Returns:
        int: Number of tokens in the file.
    """
    
    # Load the file content
    file_content = extract_text_from_pdf(file_path)
    return count_gpt_tokens(file_content, model_name)
        

def count_gpt_tokens(text, model_name='gpt-4o'):
    """
    Counts the number of GPT tokens in a string.
    
    Args:
        text (str): Th text to be tokenized.
        model_name (str): Name of the OpenAI model for tokenization. Default is 'gpt-4'.

    Returns:
        int: Number of tokens in the file.
    """
    try:        
        # Initialize the tokenizer
        encoding = tiktoken.encoding_for_model(model_name)
        
        # Tokenize the content
        tokens = encoding.encode(text)
        
        # Return the token count
        return len(tokens)
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def read_csv(file_path):
    """
    Reads a CSV file and stores each row as a dictionary with column headers as keys.
    
    :param file_path: Path to the CSV file
    :return: List of dictionaries representing rows from the CSV file
    """
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data


def write_list_of_dicts_to_csv(data: list, file_path: str):
    """
    Write a list of dictionaries to a CSV file.
    
    Parameters:
        data (list): A list of dictionaries, where keys are column headers and values are row data.
        file_path (str): The file path for the CSV file.
    """
    if not data:
        print("The data list is empty. Nothing to write.")
        return

    try:
        # Get the headers from the keys of the first dictionary
        headers = data[0].keys()

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Write the header row
            writer.writerows(data)  # Write the data rows
            
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Replace 'your_file.txt' with the path to your file
    file_path = input("Enter the file path: ").strip()
    model_name = input("Enter the model name (default 'gpt-4'): ").strip() or "gpt-4"
    token_count = count_gpt_tokens(file_path, model_name)
    
    if token_count is not None:
        print(f"Total tokens in the file: {token_count}")
