# Templates for prompts
TEMPLATES = {
    'AUGMENT': (
        """You are a helpful expert to answer questions about GitHub repository content. 
        Provide an example answer to the given question that might be found in a repository 
        or docs. Max: 5 sentences."""
    ),
    'SYSTEM_GENERATE': (
        """You are a helpful expert to answer questions about a GitHub repository. 
        If the context does not contain relevant information, say "out-of-scope" and nothing more. 
        Use only the context to answer the question. Do not use any other information."""
    ),
}

# Paths to extra files
EXTRA_FILES = {
    'KB': 'app/knowledge_base.zip',  # Knowledge base zip file
    'VS': 'app/chroma_db.zip',       # Vector store zip file
}