import json
import sys

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <json_input_file> <register_list_file>")
    sys.exit(1)

json_input_file = sys.argv[1]
register_list_file = sys.argv[2]

# Load valid register names into a set
with open(register_list_file, "r") as reg_file:
    valid_registers = set(line.strip() for line in reg_file if line.strip())

# Process and filter JSON lines
with open(json_input_file, "r") as infile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            dep = obj.get("dependee_register", {})
            depd = obj.get("dependent_register", {})
            if depd.get("register_name") in valid_registers or dep.get("register_name") in valid_registers:
                print(json.dumps(obj))
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON: {e}", file=sys.stderr)
