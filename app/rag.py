from typing import Any
from langchain.schema import HumanMessage, SystemMessage
from app.config import TEMPLATES

def retrival(query: str, vectorstore: Any, k=3) -> str:
    """
    Retrieves the most similar documents from the vector store.

    Args:
        query (str): The query string.
        vectorstore (Any): The vector store instance.
        k (int): Number of top results to retrieve.

    Returns:
        str: Concatenated content of the retrieved documents.
    """
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in results)

def augment_query(query: str, model):
    """
    Augments the query using the model and a predefined prompt.

    Args:
        query (str): The query string.
        model (Any): The language model instance.

    Returns:
        str: Augmented query response.
    """
    prompt = TEMPLATES['AUGMENT']
    response = model.invoke([
        SystemMessage(
            content=prompt
        ),
        HumanMessage(
            content=query
        )
    ])
    return response.content

def generate(query, vectorstore, model):
    """
    Generates a response based on the query, vector store, and model.

    Args:
        query (str): The query string.
        vectorstore (Any): The vector store instance.
        model (Any): The language model instance.

    Returns:
        str: Generated response content.
    """
    try:
        hypothetical_answer = augment_query(query, model)
        join_query = f'{query} {hypothetical_answer}'
        retrived_info = retrival(join_query, vectorstore)

        response = model.invoke(
            [
                SystemMessage(
                    content=TEMPLATES['SYSTEM_GENERATE']
                ),
                HumanMessage(
                    content=f"Based on only context \n\n Context: {retrived_info}.\n\n {query}"
                )
            ]
        )
        return response.content, retrived_info
    except Exception as e:
        return f"An error occurred during response generation: {str(e)}"
