from langchain.tools import Tool
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent,AgentType
from RAG import send_query
from mcqgenerator.MCQGenerator import question ,generate_quiz
from langchain.memory import ConversationBufferMemory
from Translate_AGENT import Translate_agent

from dotenv import load_dotenv
import os
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
llm2=ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


tempt1='''give answer to the genral question according to the {query} '''

p=PromptTemplate(
    input_variables=["query"],
    template=tempt1
)


llm_chain=LLMChain(llm=llm,prompt=p)


#=============================================

template="""
check wether the extracted information from document: {information} is actually usefull for the {question} question asked by user or somewhat related,if not ask to again fetch from document or try general llm,else return the information as it is without adding any extra info or your opinion
"""

prompt=PromptTemplate(
    input_variables=["information","question"],
    template=template
)




relavence_checker = LLMChain(llm=llm,prompt=prompt,output_key="information")



genral_llm_tool=Tool.from_function(
    func=llm_chain.run,
    name="genral_question_tool",
    description="return response of querry asked to genrl llm or say hi back to as response if greeted "
)
def greet(query):
    return"hello i am an agent bot"
greeting_tool=Tool.from_function(
    func=greet,
    name="greeting",
    description="when greeted greet back "
)

Rag_tool = Tool.from_function(
    func=send_query,
    name="RAG for Sound",
    description=" if questions about sound to retrive and extract info about the document,which is on sound "
)


quiz_generate_tool = Tool.from_function(
    func=generate_quiz,
    name="Quiz_generator_using extracted info",
    description="if asked to generate quiz,this can be used.Dont always genrate quiz only when aksed"
)

def quiz_from_rag(query:str):
    res=question(query)
    res=Rag_tool.run(res)
    quiz=quiz_generate_tool(res)
    q="make the quiz("+quiz+") in proper english article with space and newline"
    quiz=genral_llm_tool.run(q)
    return {quiz}
    
    
quiz_from_rag_tool=Tool.from_function(
    func=quiz_from_rag,
    name="quiz_from_rag",
    description="only used if quiz mentioned is related to sound document .retrive information from document on sound before genrating quiz"
)

def translate(query):
    q= "from the query ("+query+") determine the text to be translated and language to which it shiuld be translated"
    res=genral_llm_tool.run(q)
    res=Translate_agent.run(res)
    return res

Translator_tool=Tool.from_function(
    func=translate,
    name="Translator_tool",
    description=" return dictionary as translated language name: translated text  FOR ANY TRANSLATION TASK ALWAYS USE THISSS provide the language to be translated to and  "
)

def agent(query):
    def relevece(information):
        relavence_checker.run({"information":information,"question":query})
    memory = ConversationBufferMemory(memory_key="chat_history")    
    agent_1 = initialize_agent(
    tools=[greeting_tool,Translator_tool,quiz_from_rag_tool,genral_llm_tool,Rag_tool],
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # Conversational agent
    memory=memory,
    llm=llm2,
    verbose=True
    )
    response=agent_1.run(query)
    print(response)
    return response
