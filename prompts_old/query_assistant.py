from openai import OpenAI
 
from pydantic import BaseModel

class RegisterInfo (BaseModel):
    register_name: str
    subfield_name_abbreviation: str
    bit_range: str
    value: str

class RegisterDependencies (BaseModel):
    dependee_register: RegisterInfo
    dependent_register: RegisterInfo

class DependencyInfo (BaseModel):
    dependencies: list[RegisterDependencies]

client = OpenAI()
assistant_id_ixgbe = "asst_yjWCTfYncyyWXSfF9gVERTRa" # from openAI dashboard
assistant_id_stm = "asst_WbWuQMFb1bWVtcfsxbVxin4r"
assistant_id_e1000 = "asst_tn2wZm75b0ht5AoHwBGq1vYF"


assistant_id = assistant_id_e1000
# Upload the user provided file to OpenAI
message_file = client.files.create(
  file=open("../datasheet/stm32F407/STM32F407.xml", "rb"), purpose="assistants"
)
 

def identify_inter_register_dependencies():
    """ Prompt for identifying inter-register dependencies """

    prompt = f"""
        You have access to a datasheet for the 82579 intel ethernet device.
        It contains a table that lists all the registers and their offsets.
        It also contains a per-table register with information about the register subfields.
        It details explicit dependencies between registers. 
        I will give some examples of such dependencies, and then state the task.

        ** Example 1 ** 
        For the RDH register the datasheet states:
            "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the receive function (RCTL.EN)."
        This means there is a dependency between the RDH and CTRL registers and between the RDH and RCTL registers.
        The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "CTRL",
                        "subfield_name_abbreviation": "SWRST",
                        "bit_range": "26"
                        "value": "1"}},
                    "dependent_register":
                        {{"register_name": "RDH",
                        "subfield_name_abbreviation": "RDH",
                        "bit_range": "15:0"
                        "value": "N/A"}}
                }},
                {{
                    "dependee_register": 
                        {{"register_name": "RDH",
                        "subfield_name_abbreviation": "RDH",
                        "bit_range": "15:0"
                        "value": "N/A"}},
                    "dependent_register":
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "1"}}
                }}]
            }}
        ** Example 1 end **

        ** Example 2 **
        For the RXCSUM register the datasheet states: 
            "This register should only be initialized (written) when the receiver is not enabled (e.g. only write this register when RCTL.EN = 0)"
        This means there is a dependency between the RXCSUM register and the RCTL.EN bit.

         The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "0"}},
                    "dependent_register":
                        {{"register_name": "RXCSUM",
                        "subfield_name_abbreviation": "RXCSUM",
                        "bit_range": "31:0"
                        "value": "N/A"}}
                }}]
            }}
        ** Example 2 end **

        ** Example 3 **
        For the MRQC register the datasheet states: 
            "This field can be modified only when receive to host is not enabled (RCTL.EN = 0)"
        This means there is a dependency between the MRQC register and the RCTL.EN bit.

         The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "RCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "0"}},
                    "dependent_register":
                        {{"register_name": "MRQC",
                        "subfield_name_abbreviation": "MRxQueue",
                        "bit_range": "1:0"
                        "value": "N/A"}}
                }}]
            }}
        ** Example 3 end **

        ** Example 4 ** 
        For the TDH register the datasheet states:
            "The only time that software should write to this register is after a reset (hardware reset or CTRL.SWRST) and before enabling the transmit function (TCTL.EN)"
        This means there is a dependency between the TDH and CTRL registers and between the TDH and TCTL registers.
        The output for this dependency would be formatted as: 
            {{"dependencies": [{{
                    "dependee_register": 
                        {{"register_name": "CTRL",
                        "subfield_name_abbreviation": "SWRST",
                        "bit_range": "26"
                        "value": "1"}},
                    "dependent_register":
                        {{"register_name": "TDH",
                        "subfield_name_abbreviation": "TDH",
                        "bit_range": "15:0"
                        "value": "N/A"}}
                }},
                {{
                    "dependee_register": 
                        {{"register_name": "TDH",
                        "subfield_name_abbreviation": "TDH",
                        "bit_range": "15:0"
                        "value": "N/A"}},
                    "dependent_register":
                        {{"register_name": "TCTL",
                        "subfield_name_abbreviation": "EN",
                        "bit_range": "1"
                        "value": "1"}}
                }}]
            }}
        ** Example 4 end **

        ** Task **
        Find all such explicit inter-register dependencies for registers in the datasheet and list them.
        An explicit dependency means that a register subfield must be updated before another register subfield can be updated.

    """
    return prompt

prompt = identify_inter_register_dependencies()
messages = []
# add the new question
messages.append({ "role": "user", "content": prompt })

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages= messages,
  # response_format=DependencyInfo

  # [
    # {
    #   "role": "user",
    #   "content": "Tell me how a packet is sent with the 82599 intel ethernet device. BE very clear. \
    #         Assume the device is initialized and ready to send a packet. \
    #         Tell me which regsiters and packet descriptor feilds are read/written to.\
    #         make sure the order is correct.",
    #   "content": "Write the Rust data structure for a Transmit descriptor, both legacy and advanced.", # gets the name of the fields right, but issue with number of bits per fields
    #   "content": "What read or writes to other registers is the fctrl register dependent on.", # gets rxctrl dependency
    #   "content": "What other registers is the rxcsum register dependent on.", # gets rxctrl dependency
    #   "content": "What are the restrictions to reading or writing to the tdh register.", # gets ctrl and tdxctl
      # "content": "What are the reserved bits of the ctrl register", # gets ctrl and tdxctl
      # "content":  "The STM32F407 device has multiple peripherals. For each peripheral, the datasheet lists its registers and their read/ write restrictions."
                  # "I have attached the device system view description file written in xml."
                  # "Search for every register in the xml file and check that its description in xml matches what is given in the datasheet."
                  # "If there is any discrepancy report it, list the line number in the attached file and the page number in the document where the discrepancy takes place.",
                  # "In addition, the datasheet mentions states that a peripheral can be in. For example the GPIO pins can be in input and output modes"
                  # "It might not refer to them as states, rather as modes."
                  # "Find all mentions of peripherals that can be in multiple modes."
                  # "Give the peripheral name, then write the modes it can be in with a description of each mode."
                  # "Do not leave any information out.",
                  # "List all the registers in the CRC peripheral",
      

      # Attach the new file to the message.
      # "attachments": [
      #   { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      # ],
    # }
  # ]
)
 
# # The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI
 
client = OpenAI()
 
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant_id,
    instructions="Please give completely accurate information. Do not give extra information but be complete. Only answer the question that was asked.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()