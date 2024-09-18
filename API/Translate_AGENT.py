from langchain.tools import Tool
from langchain.agents import initialize_agent,AgentType
from RAG import send_query
from mcqgenerator.MCQGenerator import question ,generate_quiz
from langchain_groq import ChatGroq

import requests
# from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

import os
load_dotenv()

import pathlib
import json
root_dir = pathlib.Path(__file__).parent
print(root_dir)
config_file_path=str(root_dir /'config'/'config.json' )
with open(config_file_path, 'r') as config_file:
    config_data = json.load(config_file)


os.environ['GROQ_API_KEY']=config_data['GROQ_API_KEY']


llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
url = "https://api.sarvam.ai/translate"

def template_generator(text,tlc):
    return({
        "source_language_code": "en-IN",
        "input": text,
        "target_language_code": tlc,
        "model": "mayura:v1",
        "enable_preprocessing": False,
        "mode": "code-mixed"
    })
  

def translate_hindi(text):
    payload = template_generator(text,"hi-IN")    
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return response.text

def translate_bengali(text):
    payload = template_generator(text, "bn-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Kannada (kn-IN)
def translate_kannada(text):
    payload = template_generator(text, "kn-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Malayalam (ml-IN)
def translate_malayalam(text):
    payload = template_generator(text, "ml-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Marathi (mr-IN)
def translate_marathi(text):
    payload = template_generator(text, "mr-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Odia (od-IN)
def translate_odia(text):
    payload = template_generator(text, "od-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Punjabi (pa-IN)
def translate_punjabi(text):
    payload = template_generator(text, "pa-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Tamil (ta-IN)
def translate_tamil(text):
    payload = template_generator(text, "ta-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Telugu (te-IN)
def translate_telugu(text):
    payload = template_generator(text, "te-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text

# Function to translate to Gujarati (gu-IN)
def translate_gujarati(text):
    payload = template_generator(text, "gu-IN")
    headers = {
        "api-subscription-key": "392c8f90-fa24-4682-82e7-359331fa0a23",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    return response.text


from langchain.tools import Tool

# Tool for translating to Hindi
translate_hindi_tool = Tool.from_function(
    func=translate_hindi,
    name="translate_hindi",
    description="Retrieves text in English and translates it to Hindi, returning the translated text as dict translayed text:."
)

# Tool for translating to Bengali
translate_bengali_tool = Tool.from_function(
    func=translate_bengali,
    name="translate_bengali",
    description="Retrieves text in English and translates it to Bengali, returning the translated text as dict translayed text:."
)

# Tool for translating to Kannada
translate_kannada_tool = Tool.from_function(
    func=translate_kannada,
    name="translate_kannada",
    description="Retrieves text in English and translates it to Kannada, returning the translated text as dict translayed text:."
)

# Tool for translating to Malayalam
translate_malayalam_tool = Tool.from_function(
    func=translate_malayalam,
    name="translate_malayalam",
    description="Retrieves text in English and translates it to Malayalam, returning the translated text as dict translayed text:."
)

# Tool for translating to Marathi
translate_marathi_tool = Tool.from_function(
    func=translate_marathi,
    name="translate_marathi",
    description="Retrieves text in English and translates it to Marathi, returning the translated text as dict translayed text:."
)

# Tool for translating to Odia
translate_odia_tool = Tool.from_function(
    func=translate_odia,
    name="translate_odia",
    description="Retrieves text in English and translates it to Odia, returning the translated text as dict translayed text:."
)

# Tool for translating to Punjabi
translate_punjabi_tool = Tool.from_function(
    func=translate_punjabi,
    name="translate_punjabi",
    description="Retrieves text in English and translates it to Punjabi, returning the translated text as dict translayed text:."
)

# Tool for translating to Tamil
translate_tamil_tool = Tool.from_function(
    func=translate_tamil,
    name="translate_tamil",
    description="Retrieves text in English and translates it to Tamil, returning the translated text as dict translayed text:."
)

# Tool for translating to Telugu
translate_telugu_tool = Tool.from_function(
    func=translate_telugu,
    name="translate_telugu",
    description="Retrieves text in English and translates it to Telugu, returning the translated text  as dict translayed text:."
)

# Tool for translating to Gujarati
translate_gujarati_tool = Tool.from_function(
    func=translate_gujarati,
    name="translate_gujarati",
    description="Retrieves text in English and translates it to Gujarati, returning the translated text as as dict."
)

tools = [
    translate_hindi_tool,
    translate_bengali_tool,
    translate_kannada_tool,
    translate_malayalam_tool,
    translate_marathi_tool,
    translate_odia_tool,
    translate_punjabi_tool,
    translate_tamil_tool,
    translate_telugu_tool,
    translate_gujarati_tool
]

Translate_agent=initialize_agent(
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm) 


    