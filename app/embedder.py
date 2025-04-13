import os

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
        try:
            embeddings = self.client.embeddings.create(
                input=input,
                model=os.getenv('EMBEDDING_MODEL')
            )
            return [emb.embedding for emb in embeddings.data]
        except Exception as e:
            print(f"Error generating document embeddings: {e}")
            return []

    def embed_query(self, text: str|Documents) -> Embeddings:
        try:
            # Return the first embedding for a single query
            return self.embed_documents(text)[0]
        except IndexError:
            print(f"Error generating embeddings for query {text}.")
            return []
