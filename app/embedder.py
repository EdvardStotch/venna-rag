import os
import requests
import json

from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import AzureOpenAI


class CustomEmbedder(EmbeddingFunction):
    def __init__(self):
        super().__init__()
        self.client = AzureOpenAI(
            api_version=os.getenv('API_VERSION'),
            azure_endpoint=os.getenv('API_ENDPOINT'),
            api_key=os.getenv('API_KEY')
        )

    def embed_documents(self, input: Documents) -> Embeddings:
        
        embeddings = self.client.embeddings.create(
            input=input,
            model=os.getenv('EMBEDDING_MODEL')
        )

        res = []
        for emb in embeddings.data:
            res.append(emb.embedding)

        return res

    def embed_query(self, text):
        return self.embed_documents(text)[0]
