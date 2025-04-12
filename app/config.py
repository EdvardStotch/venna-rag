TEMPLATES = {
    "AUGMENT": """You are a helpful expert to answer questions about github repository content. 
        Provide an example answer to the given question, that might be found in a repository 
        or docs. max: 5 sentences""",
    "SYSTEM_GENERATE": """You are helpful expert to answer questions about github repository. 
        If the context does not contains relevant information say "NO INFORMATION" and nothing more.
        Use only the context to answer the question. Do not use any other information""",
}

EXTRA_FILES = {
    "KB": "app/knowledge_base.zip",
    "VS": 'app/chroma_db.zip',
}