import os

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma 
from langchain_openai import AzureChatOpenAI

from app.embedder import CustomEmbedder
from app.rag import generate
from app.helpers import unzip
from app.config import EXTRA_FILES

extract_path = "app"

# Download and unzip the knowledge base and vector database folder if they dont't exist
if not os.path.exists('./app/knowledge_base'):
    try:
        unzip(EXTRA_FILES['KB'], extract_path)
    except Exception as e:
        print(f"Error downloading or unzipping the file: {e}")

if not os.path.exists('./app/chroma_db'):
    try:
        unzip(EXTRA_FILES['VS'], extract_path)
    except Exception as e:
        print(f"Error downloading or unzipping the file: {e}")
    
# Initialize the vector store and model
vectorstore = Chroma(embedding_function=CustomEmbedder(), persist_directory='./app/chroma_db')

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
    response = generate(query.question, vectorstore, model)
    return response