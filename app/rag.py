import os
import bs4

from langchain import hub
from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage

from dotenv import load_dotenv
from embedder import CustomEmbedder
load_dotenv()

loader = BSHTMLLoader('knowledge_base/test.html')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)

# vectorstore = Chroma.from_documents(documents=splits, embedding=CustomEmbedder())

# retriever = vectorstore.as_retriever()
# template = """
#     You are helpful assistent to answer questions based on the context {context}
# """

model = AzureChatOpenAI(
    openai_api_version=os.getenv('API_VERSION'),
    azure_deployment="gpt-4.5-preview-2025-02-27",
    azure_endpoint=os.getenv('API_ENDPOINT'),
    api_key=os.getenv('API_KEY')
)

response = model.invoke(
    [
        HumanMessage(
            content="Hello!"
        )
    ]
)

print(response)