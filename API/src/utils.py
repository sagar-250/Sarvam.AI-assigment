from langchain.document_loaders import PyMuPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings


def load_pdf(data):
    loader=DirectoryLoader(data,
                           glob="*.pdf",   
                           loader_cls=PyMuPDFLoader)
    documents = loader.load()
    return documents

def text_split(extracted_data,chunk_size=200,chunk_overlap = 20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap = chunk_overlap)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def download_hugging_face_embedings():
    embeddings = HuggingFaceEmbeddings(model_name="sangmini/msmarco-cocondensor-MiniLM-L12_en-ko-ja")
    return embeddings
