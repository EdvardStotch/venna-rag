import os
import requests
import json

from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import AzureOpenAI


class CustomEmbedder(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        client = AzureOpenAI(
            api_version=os.getenv('API_VERSION'),
            azure_endpoint=os.getenv('API_ENDPOINT'),
            api_key=os.getenv('API_KEY')
        )

        embeddings = client.embeddings.create(
            input=input,
            model=os.getenv('EMBEDDING_MODEL')
        )
        return embeddings