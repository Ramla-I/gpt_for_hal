import csv, re
# File paths
registers_summary_path = './registers_summary.csv'
registers_info_path = './register_info'

def snake_case(s):
    """Convert a string to snake_case."""
    return s.replace(" ", "_").replace("/", "_").replace("-", "_").lower()

def camel_case(s):
    """Convert a string to camelCase."""
    # Split the string into words using non-alphanumeric characters as delimiters
    words = re.split(r'[^a-zA-Z0-9]', s)
    
    # Capitalize each word except the first one, and join them back together
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def pascal_case(s):
    """Convert a string to PascalCase."""
    # Split the string into words using non-alphanumeric characters as delimiters
    words = re.split(r'[^a-zA-Z0-9]', s)
    
    # Capitalize each word except the first one, and join them back together
    return ''.join(word.capitalize() for word in words)


def calculate_padding(offset1, offset2):
    """Calculate the padding size between two offsets."""
    return offset2 - offset1 - 4


def get_start_end_from_range(bit_range: str) -> tuple[int, int]:
    bit_range = bit_range.strip()
    if bit_range.isdigit():
        bit = int(bit_range)
        return (bit, bit)

    if ":" in bit_range or "-" in bit_range or "," in bit_range:
        sep = ":" if ":" in bit_range else "-" if "-" in bit_range else ","
        high, low = map(int, bit_range.split(sep))
        return (min(high, low), max(high, low))
    else:
        raise ValueError(f"Invalid bit range: {bit_range}")


def bit_shift_from_range(bit_range: str) -> int:
    (low, high) = get_start_end_from_range(bit_range)
    return low


def create_bitmask(bit_ranges):
    """
    Creates a 32-bit mask with specified bits set to 1.
    
    :param bit_ranges: String with inclusive bit ranges (e.g., "0-1 3 7:9 4,6")
    :return: 32-bit integer mask
    """
    mask = 0
    # print(bit_ranges)
    ranges = bit_ranges.split()
    for r in ranges:
        if 'NA' in r:
            continue

        (low, high) = get_start_end_from_range(r)
        for bit in range(low, high + 1):
            mask |= (1 << bit)

    return mask

def parse_to_int(value: str) -> int | None:
    try:
        value = value.strip().lower()
        if value.endswith("b"):  # e.g., "10b"
            return int(value[:-1], 2)
        elif value.startswith("0b"):  # e.g., "0b10"
            return int(value, 2)
        elif value.startswith("0x"):  # e.g., "0xA"
            return int(value, 16)
        elif value.isdigit():  # Decimal
            return int(value)
        else:
            return None
    except Exception:
        return None

def generate_dependencies():
    dependencies = "extern crate volatile;\n"
    dependencies += "use volatile::{Volatile, ReadOnly, WriteOnly};\n\n"
    return dependencies

def generate_struct_code(registers_list, register_struct_name="Registers"):
    """Generate Rust struct code based on the register summary and detailed info."""
    struct_code = "#[repr(C)]\npub struct " + register_struct_name + " {\n"
    
    previous_offset = 0
    field_type = None
    padding_num = 0

    for reg in registers_list:
        offset = int(reg['Offset'], 16)
        name = snake_case(reg['Abbreviation'])
        rw_type = reg['R/W restrictions']

        if rw_type == "RW":
            field_type = "Volatile<u32>"
        elif rw_type == "RO":
            field_type = "ReadOnly<u32>"
        elif rw_type == "WO":
            field_type = "WriteOnly<u32>"
        else:
            field_type = "u32"

        padding = offset - previous_offset - 4;
        # print(f"Name: {name}, Offset: {offset}, Padding: {padding}")
        if padding > 0:
            struct_code += f"    _padding{padding_num}: [u8; {padding}], // 0x{offset:X} - 0x{previous_offset + 4:X}\n"
            padding_num += 1
        struct_code += f"    {name}: {field_type}, //0x{offset:X}\n"
        
        previous_offset = offset

    struct_code += "}\n"
    return struct_code

def generate_accessor_methods(registers_list, register_struct_name="Registers"):
    """Generate Rust struct code based on the register summary and detailed info."""
    methods_code = "impl " + register_struct_name + " {\n"
    
    for reg in registers_list:
        read_mask = int(reg['RO mask']) | int(reg['RW mask'])
        write_mask = int(reg['WO mask']) | int(reg['RW mask'])

        if reg["R/W restrictions"] == "RO" or reg["R/W restrictions"] == "RW":
            methods_code += f"    pub fn {snake_case(reg['Abbreviation'])}_read(&self) -> u32 {{\n"
            methods_code += f"        self.{snake_case(reg['Abbreviation'])}.read() & 0x{read_mask:X} \n"
            methods_code += "    }\n\n"
        
        if reg["R/W restrictions"] == "WO" or reg["R/W restrictions"] == "RW":
            methods_code += f"    pub fn {snake_case(reg['Abbreviation'])}_write(&mut self, value: u32) {{\n"
            methods_code += f"        self.{snake_case(reg['Abbreviation'])}.write(value & 0x{write_mask:X}) \n"
            methods_code += "    }\n\n"

    methods_code += "}\n"
    return methods_code

def start_struct_impl(register_struct_name="Registers"):
    return "impl " + register_struct_name + " {\n"

def end_struct_impl(): 
    return "}\n"

def generate_subfield_accessor_methods(enum_defs, enum_methods_code, reg_name, subfields_list):
    """Generate Rust struct code based on the register summary and detailed info."""
    # print(subfields_list)
    for subfield in subfields_list:
        sf_abbr = subfield['subfield_name_abbreviation']
        sf_type = subfield["type"]

        enum_name = pascal_case(reg_name) + pascal_case(sf_abbr)
        enum_variants = []
        for v in subfield['valid_values']:
            # Each v is expected to be a dict with 'name' and 'value' keys
            enum_variants.append((v['name'], v['value']))
       
        # To Do: subfield mask and shift
        sf_mask = create_bitmask(subfield["bit_range"])
        bitshift = bit_shift_from_range(subfield["bit_range"])

        enum_defs += f"#[derive(Clone, Copy, Debug, PartialEq)]\npub enum {enum_name} {{\n"
        for variant in enum_variants:
            enum_defs += f"    {pascal_case(variant[0])} = {variant[1]},\n"
        enum_defs += "}\n"

        if sf_type == "RO" or sf_type == "RW":
            print("Warning: still need to generate read methods for enums")

        if sf_type == "WO" or sf_type == "RW":
            enum_methods_code += f"    pub fn {snake_case(reg_name)}_{snake_case(sf_abbr)}_write(&mut self, value: {enum_name}) {{\n"
            enum_methods_code += f"        self.{snake_case(reg_name)}.write((self.{snake_case(reg_name)}.read() & !0x{sf_mask:X}) | ((value as u32) << {bitshift}))\n"
            enum_methods_code += "    }\n\n"

    return enum_defs, enum_methods_code