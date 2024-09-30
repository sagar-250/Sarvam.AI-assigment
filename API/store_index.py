from src.utils import load_pdf,text_split,download_hugging_face_embedings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
import pathlib

root_dir = pathlib.Path(__file__).parent
folder_path=str(root_dir /'data')

os.environ['PINECONE_API_ENV'] = 'gcp-starter'
os.environ['PINECONE_API_KEY'] = "5bc0816a-acea-4c28-8a52-a8fe49820e79"
pinecone_api="5bc0816a-acea-4c28-8a52-a8fe49820e79"
def store_index():
    extracted_data= load_pdf(folder_path)

    text_chunks = text_split(extracted_data,chunk_size=100,chunk_overlap = 10)
    print("length of my chunks", len(text_chunks))
    
    embeddings=download_hugging_face_embedings()
    
    vectorstore = PineconeVectorStore.from_texts(
                    texts=[t.page_content for t in text_chunks],    
                    index_name="sarvamrag",
                    pinecone_api_key = pinecone_api, 
                    embedding=embeddings)

store_index()    
