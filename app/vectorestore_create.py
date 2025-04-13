import os
import bs4
from bs4 import BeautifulSoup

from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from embedder import CustomEmbedder

def vectors_database_from_htmls(directory: str):
    """
    Processes HTML files in the given directory, extracts content, splits it into chunks,
    and stores it in a vector database.

    Args:
        directory (str): Path to the directory containing HTML files.
    """
    html_files = os.listdir(directory)
    for html in html_files:
        file_path = f'{directory}/{html}'
        _, extension = os.path.splitext(file_path)
        if extension != '.html':
            continue
        
        try:
            with open(file_path, encoding='utf-8') as file:
                html_data = file.read()
            soup = BeautifulSoup(html_data, 'html.parser')
        except Exception as e:
            continue

        # Extract content
        content = soup.find('div', class_='md-content')
        if not content or len(content.text) < 100:
            continue

        try:
            loader = BSHTMLLoader(file_path, bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("md-content")
                )
            ))

            data = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            splits = text_splitter.split_documents(data)

            Chroma.from_documents(documents=splits, embedding=CustomEmbedder(), persist_directory='./chroma_db')
        except Exception as e: 
            print(f"Error processing {file_path}: {e}")
            continue

## Testing
# vectors_database_from_htmls('knowledge_base/processed')