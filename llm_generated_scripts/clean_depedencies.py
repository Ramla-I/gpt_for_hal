import json
import sys

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        deps = obj.get("dependencies", [])
        if not deps:
            continue  # skip lines with no dependencies
        for dep in deps:
            json.dump(dep, outfile)
            outfile.write("\n")

print(f"Processed file written to {output_file}")
