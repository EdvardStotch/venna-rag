import requests

from chromadb import Documents, EmbeddingFunction, Embeddings


class Embedder(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = requests.post('https://ai-proxy.lab.epam.com/openai/deployments/text-embedding-3-large-1/embeddings')