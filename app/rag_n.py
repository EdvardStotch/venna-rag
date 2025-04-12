import os
import bs4
import re

from langchain import hub
from langchain_community.vectorstores import Chroma 
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from embedder import CustomEmbedder
load_dotenv()

model = AzureChatOpenAI(
    openai_api_version=os.getenv('API_VERSION'),
    azure_deployment=os.getenv('LLM_MODEL'),
    azure_endpoint=os.getenv('API_ENDPOINT'),
    api_key=os.getenv('API_KEY'),
    temperature=0
)

vectorstore = Chroma(embedding_function=CustomEmbedder(), persist_directory='./chroma_db')

def retrival(query, k=3):
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in results)



# relevants = retrival('Tell me about vanna ai github file structure')
# print(relevants)

def augment_query(query):
    prompt = """You are a helpful expert to answer questions about github repository content. 
    Provide an example answer to the given question, that might be found in a repository 
    or docs. max: 5 sentences"""
    response = model.invoke([
        SystemMessage(
            content=prompt
        ),
        HumanMessage(
            content=query
        )
    ])
    return response.content

def generate(query):
    hypothetical_answer = augment_query(query)
    join_query = f'{query} {hypothetical_answer}'
    retrived_info = retrival(join_query)

    response = model.invoke(
        [
            SystemMessage(
                content="You are helpful expert to answer questions about github repository. If the context does not contains relevant information say NOT INFORMATION found and nothing more"
            ),
            HumanMessage(
                content=f"Based on only context {retrived_info}. {query}"
            )
        ]
    )

    print(response.content)

# print(augment_query('Tell me about vanna ai github file structure', model))
# print(';' * 55)
# exit()
# print('1' * 55)
# # chain = template | model.invoke() | StrOutputParser()
# response = model.invoke(
#     [
#         HumanMessage(
#             content=f"You are helpful assistent to answer questions based on the context {relevants}. Tell me about vanna ai github file structure'"
#         )
#     ]
# )

# print(response)
# # print(chain.invoke({"context": relevants, "question": "Tell me about vanna ai github file structure"}))


generate('Tell me about vanna ai')