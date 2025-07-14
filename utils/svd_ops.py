import xml.etree.ElementTree as ET

def parse_svd(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # SVD files are usually in the CMSIS-SVD schema
    namespace = {'ns': 'http://www.w3.org/2001/XMLSchema-instance'}

    # Print the device name
    device_name = root.findtext('name')
    print(f"Device: {device_name}\n")

    # Loop over peripherals
    for peripheral in root.findall('peripherals/peripheral'):
        pname = peripheral.findtext('name')
        pdesc = peripheral.findtext('description')
        base_addr = peripheral.findtext('baseAddress')
        print(f"Peripheral: {pname}")
        print(f"  Description: {pdesc}")
        print(f"  Base Address: {base_addr}")

        # Loop over registers
        registers = peripheral.find('registers')
        if registers is not None:
            for register in registers.findall('register'):
                rname = register.findtext('name')
                roffset = register.findtext('addressOffset')
                rdesc = register.findtext('description')
                print(f"    Register: {rname}")
                print(f"      Offset: {roffset}")
                print(f"      Description: {rdesc}")

                # Loop over fields
                fields = register.find('fields')
                if fields is not None:
                    for field in fields.findall('field'):
                        fname = field.findtext('name')
                        fdesc = field.findtext('description')
                        bit_offset = field.findtext('bitOffset')
                        bit_width = field.findtext('bitWidth')
                        print(f"        Field: {fname}")
                        print(f"          Offset: {bit_offset}")
                        print(f"          Width: {bit_width}")
                        print(f"          Description: {fdesc}")
        print("")
    return root


def extract_peripheral_xml_blocks(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    peripherals = root.findall('peripherals/peripheral')
    peripheral_blocks = []

    for peripheral in peripherals:
        xml_text = ET.tostring(peripheral, encoding='unicode')
        peripheral_blocks.append(xml_text)

    return peripheral_blocks

if __name__ == "__main__":
    # Replace with the path to your SVD file
    parse_svd("../stm32-rs/svd//stm32f407.svd")
