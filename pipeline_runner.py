import json
import re
import importlib
import prompts
from main import call_openai_api
from utils.file_ops import read_csv

# List of modules to search for process functions
PROCESS_MODULES = [
    "llm_generated_scripts",
    "dependencies",
    "utils.file_ops",
    "utils.pdf_ops",
    "utils.pdf_to_registers",
    # Add more as needed
]

def import_process_function(function_name):
    """Try to import a function from known modules."""
    for module_name in PROCESS_MODULES:
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            return func
        except (ImportError, AttributeError):
            continue
    raise ImportError(f"Process function '{function_name}' not found in known modules.")

def extract_template_vars(s):
    """Return a list of template variables in the string."""
    return re.findall(r"\{(\w+)\}", s)

def expand_template(s, context):
    """Replace {var} in s with context[var]."""
    for var in extract_template_vars(s):
        s = s.replace(f"{{{var}}}", str(context[var]))
    return s

def get_source_list(results, template_vars):
    """
    Find a list of dicts in results that contains all template_vars as keys.
    Returns (list, key) or (None, None) if not found.
    """
    for k, v in results.items():
        if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            if all(any(var in x for x in v) for var in template_vars):
                return v, k
    return None, None

def run_pipeline(output_dir, pipeline_path, initial_inputs):
    # Load pipeline steps
    with open(pipeline_path) as f:
        steps = [json.loads(line) for line in f if line.strip()]
    results = dict(initial_inputs)

    for step in steps:
        step_type = step['type']
        output_key = step['saved_output']
        input_templates = step.get('input', [])

        # Check for template variables in inputs or output
        template_vars = set()
        for inp in input_templates:
            template_vars.update(extract_template_vars(inp))
        template_vars.update(extract_template_vars(output_key))

        if template_vars:
            # Find the source list in results (e.g., from a CSV or previous step)
            source_list, source_key = get_source_list(results, template_vars)
            if not source_list:
                # Try to load from CSV if available
                # (e.g., for reg_name, reg_abbreviation from a register table)
                if "reg_table.csv" in results:
                    source_list = read_csv(results["reg_table.csv"])
                    source_key = "reg_table.csv"
                elif "reg_table_pre.csv" in results:
                    source_list = read_csv(results["reg_table_pre.csv"])
                    source_key = "reg_table_pre.csv"
                else:
                    raise ValueError(f"Could not find source list for template variables {template_vars} in step {step}")

            for item in source_list:
                context = {var: item.get(var) or item.get(var.replace("reg_", "")) or item.get(var.replace("_abbreviation", "Abbreviation")) or item.get(var.replace("_name", "Name in List")) for var in template_vars}
                # Fallback: try common field names
                for var in template_vars:
                    if not context[var]:
                        if var == "reg_name":
                            context[var] = item.get("Name in List") or item.get("reg_name")
                        elif var == "reg_abbreviation":
                            context[var] = item.get("Abbreviation") or item.get("reg_abbreviation")
                # Prepare inputs
                inputs = []
                for inp in input_templates:
                    if "{" in inp:
                        inputs.append(expand_template(inp, context))
                    else:
                        inputs.append(results[inp])
                # Run the step
                if step_type == 'prompt':
                    prompt_func = getattr(prompts, step['prompt_name'])
                    prompt = prompt_func(*inputs)
                    result = call_openai_api([], prompt)
                elif step_type == 'process':
                    func = import_process_function(step['function_name'])
                    result = func(*inputs)
                else:
                    raise ValueError(f"Unknown step type: {step_type}")
                # Save output
                output_name = expand_template(output_key, context)
                results[output_name] = result
                print(f"Step '{step.get('prompt_name') or step.get('function_name')}' for {context} complete. Output saved as '{output_name}'.")
        else:
            # No template variables, run as before
            inputs = [results[inp] for inp in input_templates]
            if step_type == 'prompt':
                prompt_func = getattr(prompts, step['prompt_name'])
                prompt = prompt_func(*inputs)
                result = call_openai_api([], prompt)
            elif step_type == 'process':
                func = import_process_function(step['function_name'])
                result = func(*inputs)
            else:
                raise ValueError(f"Unknown step type: {step_type}")
            results[output_key] = result
            print(f"Step '{step.get('prompt_name') or step.get('function_name')}' complete. Output saved as '{output_key}'.")

    return results

# Example usage:
if __name__ == "__main__":
    import config
    initial_inputs = {

        # Add more if needed
    }
    results = run_pipeline("prompts.json", initial_inputs)
    # Now results contains all intermediate and final outputs