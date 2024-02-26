import os
import json
import time
from openai import AzureOpenAI

### Test Azure Open AI Assistant — Code interpreter ###
### 2024-02-26 FB

#API Version Preview!
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

#Din Key
AZURE_OPENAI_API_KEY = ""

#Din URL
AZURE_OPENAI_ENDPOINT_URL = ""

#Namnet på din egen model i Azure AI Studio
AZURE_OPENAI_MODEL_NAME = "gpt4" 

### Din fråga ###
USER_QUESTION = f"Create a C# that calculates the sum of all squares"

##################################
##################################

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,  
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT_URL
    )

assistant = client.beta.assistants.create(
    name="Code Generator",
    instructions=f"You are a helpful AI assistant who makes code suggestions based on questions. "
    f"You have access to a sandboxed environment for writing and testing code.",
    tools=[{"type": "code_interpreter"}],
    model=AZURE_OPENAI_MODEL_NAME
)

#print(assistant.model_dump_json(indent=2))
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=USER_QUESTION
)

thread_messages = client.beta.threads.messages.list(thread.id)
#print(thread_messages.model_dump_json(indent=2))

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

status = run.status

# Vänta på status completed
while status not in ["completed", "cancelled", "expired", "failed"]:
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    status = run.status

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.model_dump_json(indent=2))