from openai import OpenAI
 
client = OpenAI()
assistant_id = "asst_yjWCTfYncyyWXSfF9gVERTRa" # from openAI dashboard

# # Upload the user provided file to OpenAI
# message_file = client.files.create(
#   file=open("edgar/aapl-10k.pdf", "rb"), purpose="assistants"
# )
 
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
    #   "content": "Tell me how a packet is sent witht he 82599 intel ethernet device. BE very clear. \
    #         Assume the device is initialized and ready to send a packet. \
    #         Tell me which regsiters and packet descriptor feilds are read/written to.\
    #         make sure the order is correct.",
      "content": "Write the Rust data structure for a Transmit descriptor, both legacy and advanced.", # gets the name of the fields right, but issue with number of bits per fields

      # Attach the new file to the message.
      # "attachments": [
      #   { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      # ],
    }
  ]
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
    instructions="Please give completely accurate information.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()