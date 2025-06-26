from pydantic import BaseModel

def categorize_dependencies(dependencies_json):
    """ Prompt for extracting per-register section headers """

    prompt = f"""
       Given a file of JSON entries of dependee and dependent registers, look at the relevant sentence and assess if the dependency is something that can be encoded in software or it is enforced by hardware.
       If it is not clear then label it as other.
       Return the list of JSON objects with one extra field at the end which categorizes the dependency.

        The list is: : {dependencies_json}
    """
    return prompt
