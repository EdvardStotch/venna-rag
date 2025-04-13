import os

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma 
from langchain_openai import AzureChatOpenAI

from app.embedder import CustomEmbedder
from app.rag import generate
from app.helpers import unzip
from app.config import EXTRA_FILES

# Constants for paths
EXTRACT_PATH = "app"
KNOWLEDGE_BASE_PATH = './app/knowledge_base'
CHROMA_DB_PATH = './app/chroma_db'

# Ensure the knowledge base and vector database folders exist
def ensure_directory_exists(path: str, zip_file: str):
    if not os.path.exists(path):
        try:
            unzip(zip_file, EXTRACT_PATH)
        except Exception as e:
            print(f"Error downloading or unzipping the file: {e}")

ensure_directory_exists(KNOWLEDGE_BASE_PATH, EXTRA_FILES['KB'])
ensure_directory_exists(CHROMA_DB_PATH, EXTRA_FILES['VS'])
    
# Initialize the vector store
vectorstore = Chroma(
    embedding_function=CustomEmbedder(),
    persist_directory=CHROMA_DB_PATH
)

# Initialize the Azure OpenAI model
model = AzureChatOpenAI(
    openai_api_version=os.getenv('API_VERSION'),
    azure_deployment=os.getenv('LLM_MODEL'),
    azure_endpoint=os.getenv('API_ENDPOINT'),
    api_key=os.getenv('API_KEY'),
    temperature=0
)

# FastAPI app
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def create_item(query: Query):
    response, retrived_info = generate(query.question, vectorstore, model)
    return {
        "response": response, 
        "kb": retrived_info
    }