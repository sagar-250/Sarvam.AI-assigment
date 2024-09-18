from src.utils import download_hugging_face_embedings
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os 
from src.prompt import *
load_dotenv()

import pathlib
import json
root_dir = pathlib.Path(__file__).parent
print(root_dir)
config_file_path=str(root_dir /'config'/'config.json' )
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)


os.environ['GROQ_API_KEY']=config_data['GROQ_API_KEY']
os.environ['PINECONE_API_ENV'] = config_data['PINECONE_API_ENV']
os.environ['PINECONE_API_KEY'] = config_data['PINECONE_API_KEY']

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

embeddings = download_hugging_face_embedings()

index_name = "rag"

docsearch=Pinecone.from_existing_index(index_name, embeddings)

prompt = PromptTemplate(
input_variables=["context","prompt"],
template=prompt_template
)
chain_type_kwargs = {"prompt": prompt}

qa=RetrievalQA.from_chain_type(llm=llm,
                                       chain_type="stuff",
                                       retriever=docsearch.as_retriever(search_kwargs={"k":50}),
                                       return_source_documents=True,
                                     chain_type_kwargs=chain_type_kwargs
                                    )

def send_query(query):
    result=qa({"query":query})
    response=result["result"]
    print("Response : ", response)
    return response

# send_query("what is the document about")