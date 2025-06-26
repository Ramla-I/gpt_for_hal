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

        methods_code += f"    pub fn {snake_case(reg['Abbreviation'])}_read(&self) -> u32 {{\n"
        methods_code += f"        self.{snake_case(reg['Abbreviation'])}.read() && 0x{read_mask:X} \n"
        methods_code += "    }\n\n"
        methods_code += f"    pub fn {snake_case(reg['Abbreviation'])}_write(&mut self, value: u32) {{\n"
        methods_code += f"        self.{snake_case(reg['Abbreviation'])}.write(value && 0x{write_mask:X}) \n"
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
        enum_name = pascal_case(reg_name) + pascal_case(subfield['Subfield name abbreviation'])
        enum_variants = subfield['Valid values'].split(";")
        #split a string based on =
        enum_variants = [variant.split("=") for variant in enum_variants]
        # print(enum_variants)
       
        # To Do: subfield mask and shift

        enum_defs += f"#[derive(Clone, Copy, Debug, PartialEq)]\npub enum {enum_name} {{\n"
        for variant in enum_variants:
            enum_defs += f"    {pascal_case(variant[0])} = {pascal_case(variant[1])},\n"
        enum_defs += "}\n"

        enum_methods_code += f"    pub fn {snake_case(reg_name)}_{snake_case(subfield["Subfield name abbreviation"])}_write(&mut self, value: {enum_name}) {{\n"
        enum_methods_code += f"        self.{snake_case(reg_name)}.write(value as u32) \n"
        enum_methods_code += "    }\n\n"

    return enum_defs, enum_methods_code