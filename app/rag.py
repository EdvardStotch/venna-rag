from langchain.schema import HumanMessage, SystemMessage

from app.config import TEMPLATES

def retrival(query: str, vectorstore, k=3) -> str:
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in results)

def augment_query(query: str, model):
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
    return response.content
