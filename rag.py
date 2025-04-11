import bs4

from langchain import hub
from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from langchain.prompts import ChatPromptTemplate

from embedder import Embedder

loader = BSHTMLLoader('knowledge_base/test.html')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=splits, embedding=Embedder())

template = """
    You are helpful assistent to answer questions based on the context {context}
"""