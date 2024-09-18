from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn 
from RAG import send_query
from AGENT import agent

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    query:str
    
@app.post('/rag/query')
def get_response(req:Query):
    response=send_query(req.query)
    return{"Response":response}

@app.post('/agent/query')        
def get_response(req:Query):
    response=agent(req.query)
    return{"Response":response}

uvicorn.run(app,host="127.0.0.1",port=8000)        