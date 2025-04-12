import os
import bs4
from bs4 import BeautifulSoup

from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 
from dotenv import load_dotenv
from embedder import CustomEmbedder
load_dotenv()

def vectors_database_from_htmls(directory):

    html_files = os.listdir(directory)
    
    for html in html_files:
        file_path = f'{directory}/{html}'
        _, extension = os.path.splitext(file_path)
        if extension != '.html':
            continue
        
        html_data = open(file_path, encoding='utf-8').read()
        soup = BeautifulSoup(html_data, 'html.parser')

        content = soup.find('div', class_='md-content')

        if not content or len(content.text) < 100:
            continue

        loader = BSHTMLLoader(file_path, bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("md-content")
            )
        ))

        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(data)

        try:
            Chroma.from_documents(documents=splits, embedding=CustomEmbedder(), persist_directory='./chroma_db')
        except:
            continue

vectors_database_from_htmls('knowledge_base/processed')