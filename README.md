# Venna-RAG

Venna-RAG is a Retrieval-Augmented Generation (RAG) system designed to process and retrieve information from [Venna-AI GitHub](https://github.com/vanna-ai/vanna) repositories and [Venna-AI documentation](https://vanna.ai/docs/). It generates responses using a language model and integrates vector databases, document loaders, and embeddings to provide accurate and context-aware answers.

## Features
- **Document Retrieval**: Retrieves relevant documents from a vector database.
- **Query Augmentation**: Enhances user queries for better context understanding.
- **Knowledge Base Integration**: Processes and stores knowledge base documents for efficient retrieval.
- **FastAPI Integration**: Provides an API endpoint for querying the system.

---

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/venna-rag.git
   cd venna-rag
   ```

2. **Create a `.env` File**
   Create a `.env` file in the root directory or copy the provided `.env.example` file:
   ```bash
   cp .env.example .env
   ```
   Populate the `.env` file with the required values or place your existing `.env` file in the root directory.

3. **Build and Start the Application**
   Use Docker Compose to build and start the application:
   ```bash
   docker-compose up -d
   ```

---

## Usage

### API Endpoint
The API is accessible at:
```
http://localhost:8000/
```

You can open the Swagger interface at `http://localhost:8000/docs` to test the API or send a POST request to the `/ask` endpoint with the following JSON payload:
```json
{
    "question": "Your query here"
}
```

---

## Timings

- **Embedding**: The embedding process was performed on Venna-AI GitHub repositories and a subset of Venna-AI documentation (`knowledge_base/processed`). This process took approximately **2 minutes**.
- **Response Generation**: Generating a response for a query takes less than **10 seconds**.

---

### Why `text-embedding-ada-002` and ChromaDB?

- **Model Choice**: The `text-embedding-ada-002` model was selected due to its efficiency and suitability for small, domain-specific knowledge bases. Higher-dimensional models like `text-embedding-3-large-1` were tested but did not yield better results.
- **ChromaDB**: A local SQLite-based ChromaDB was chosen for its simplicity and ease of use in small-scale projects.


---

## Future Improvements

- **Preprocess Additional Documents**: Extend the knowledge base by preprocessing the remaining scraped documents from the `knowledge_base/extra` folder to include more comprehensive information.
- **Document Reranking**: Implement a document reranking mechanism to improve the quality of retrieved documents and ensure better relevance for user queries.
- **Extract and process media files and not only texts**
---