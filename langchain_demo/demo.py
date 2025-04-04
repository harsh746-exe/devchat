import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Set Hugging Face API token from environment variable
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

# Initialize the LLM
llm = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    model_kwargs={
        "temperature": 0.7,
        "max_length": 200,
        "do_sample": True
    }
)

# Create memory for the conversation
memory = ConversationBufferMemory()

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Start the conversation
response = conversation.predict(input="Hi! How can you help me with coding?")
print(response) 