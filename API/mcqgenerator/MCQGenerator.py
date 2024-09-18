import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import pathlib


from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

root_dir = pathlib.Path(__file__).parent
print(root_dir)
response_dir=str(root_dir /'Response.json' )


os.environ['GROQ_API_KEY']='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'

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

extract_template="""
    Query:{question}
    find what querry to ask for information retrival from sound doument ,it should be proper english question demanding for detailed explanation according to the Querry question and related topics
    
 """

prompt = PromptTemplate(
input_variables=["question"],
template=extract_template
)

extract_chain = LLMChain(
    llm=llm,
    prompt=prompt
)





template="""
Text:{retrived_document_information}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  {number} multiple choice questions for given subject students in given tone.
take refrence from {response_json} 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
every question should have 4 option followed by providing its correct answer
Ensure to make given number of  MCQs


"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["retrived_document_information", "response_json"],
    template=template)


quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)


template2="""

QUiz:{quiz}

Check from an expert English Writer of the above quiz 

convert the object to string which will have new line espcape sequence so it prints beautifully
 proper article quiz no object


"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["quiz"], template=template2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)


generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["retrived_document_information","number", "response_json"],output_variables=["quiz", "review"], verbose=True,)

with open(response_dir, 'r') as file:
    RESPONSE_JSON = json.load(file)
    
    
    
def question(question):
    response = extract_chain.run(question)
    return response

    
def generate_quiz(information):
    response=generate_evaluate_chain(
                    {
                    "retrived_document_information":information,
                    "number":5,
                    "response_json": json.dumps(RESPONSE_JSON)
                        }
                )
    
    return response.get("quiz")