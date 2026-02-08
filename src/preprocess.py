from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(file_path):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    documents = loader.load()
    
    # Industry Standard: Larger chunks (2000) for better context 
    # Smaller overlap (200) to save on API tokens
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Each chunk now contains .page_content AND .metadata (e.g., {'page': 1})
    return text_splitter.split_documents(documents)