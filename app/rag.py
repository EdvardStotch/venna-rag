import os
import bs4
import re

from langchain import hub
from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
from embedder import CustomEmbedder
load_dotenv()

loader = BSHTMLLoader('knowledge_base/test.html', bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
        class_=("md-content")
    )
))
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=splits, embedding=CustomEmbedder(), persist_directory='./chroma_db')

retriever = vectorstore.as_retriever()

def query_documents(question, n_results=2):
    results = vectorstore.similarity_search(question, k=n_results)
    return "\n\n".join(doc.page_content for doc in results)

def post_process(docs):
    return "\n\n".join(doc.page_content for doc in docs)


template = """
    You are helpful assistent to answer questions based on the context {context}. Answer to {question}
"""

model = AzureChatOpenAI(
    openai_api_version=os.getenv('API_VERSION'),
    azure_deployment=os.getenv('LLM_MODEL'),
    azure_endpoint=os.getenv('API_ENDPOINT'),
    api_key=os.getenv('API_KEY'),
    temperature=0
)

relevants = query_documents("Tell me about venna ai")
print(relevants)

print('-' * 15)
# rag_chain = (
#     {"context": relevants, "question": "Tell me about venna ai"}
#     | template
#     | model
#     | StrOutputParser()
# )
response = model.invoke(
    [
        HumanMessage(
            content=f"You are helpful assistent to answer questions based on the context {relevants}. Answer to 'Tell me about venna ai'"
        )
    ]
)

print(response)