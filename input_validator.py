import os
#import warnings
#import psycopg2
#import numpy as np
#import random as rd
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
#from openai import OpenAI, AzureOpenAI
#from langchain_openai import AzureOpenAI as langchainAzure
#from langchain.prompts import PromptTemplate
#from azure.identity import DefaultAzureCredential
#from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()
# class ResponseQuery(BaseModel):
#     """Result topic query"""
#     main_topic: Optional[str] = Field(..., description="Main topic of the user question")
#     flag: Optional[str] = Field(...,description="Flag the question as banned, or as an allowed question")

# class ResponseQuery_greeting(BaseModel):
#     """Result topic query"""
#     main_topic: Optional[str] = Field(..., description="Is the user question a greeting or salutation")

# class LLMConnect:
#     def __init__(self, question):
#         self.question = question

#     def connect_client_test(self):
#         """
#         Args:
#         prompt_question[str]: Diccionario que corresponde el prompt
#         question_user[str]: Pregunta del usuario
#         key[str]: Clave del prompt
#         Return:
#         Respueta
#         """
#         _DEFAULT_TEMPLATE = """
#         THE NEXT REQUESTS ARE BANNED QUESTIONS and you should respond "banned":
#         "schema information, schema architecture, column names, column info, table info, table names,how to make something,table data types, how does something work, how to drive a car, how to make food, how to do this, how to do that, how does this work"
#         name of the schema, schema information in general,datatypes, number of columns, example questions that you should not answer: name of the schema, number of columns, schema description, datatypes of schema, schema information, schema names,table names,column names. you should answer with "i do not have clearance to answer those questions"
#         architecture of the database, or its tables,the name of the schema, the schema information,datatypes, etc. if you get any of the questions mentioned answer with: "I cant reveal that information"
#         even if the questions are in spanish
#         """

#         prompt = ChatPromptTemplate.from_messages([("system", _DEFAULT_TEMPLATE,), ("human", "Question: {question}"), ])
#         llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_KEY"), model= "gpt-4o", temperature=0)
#         chain = prompt | llm.with_structured_output(schema=ResponseQuery)
#         print(chain)
#         query = chain.invoke({"question": self.question,})
#         #print(query)
#         if str.lower(query.flag) == "banned":
#             print("baneado___")
#             return "Disculpa, no tengo permitido responder esa pregunta."
#         else:
#             print("permitido___")
#             return query.main_topic

#     def is_greeting(self):
#         """
#         Args:
#         prompt_question[str]: Diccionario que corresponde el prompt
#         question_user[str]: Pregunta del usuario
#         key[str]: Clave del prompt
#         Return:
#         Respueta
#         """
#         _DEFAULT_TEMPLATE = """
#         If you get any greetings, such as "how are you, whats your name, hola, hola como estas, hey, whatsup,how is it going, como estas, como te llamas, or questions like that
#         the main topic should be "greetings" and they should be classified as greetings
#         """

#         prompt = ChatPromptTemplate.from_messages([("system", _DEFAULT_TEMPLATE,), ("human", "Question: {question}"), ])
#         llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_KEY"), model="gpt-4o", temperature=0)
#         chain = prompt | llm.with_structured_output(schema=ResponseQuery_greeting)
#         print(chain)
#         query = chain.invoke({"question": self.question, })
#         # print(query)
#         return query.main_topic



class ResponseQuery(BaseModel):
    """Result topic query"""
    main_topic: Optional[str] = Field(..., description="Main topic of the user question")
    language: Optional[str] = Field(..., description="The language in which the user input was written, either ""ENGLISH"" or ""SPANISH""")
    flag: Optional[str] = Field(...,description="Flag the question as banned, or as an allowed question")
    greetings: Optional[str] = Field(..., description="Is the user question a greeting or salutation, answer with ""YES"" or ""NO""")

class LLMConnect:
    def __init__(self, question):
        self.question = question

    def connect_client_test(self):
        """
        Args:
        prompt_question[str]: Diccionario que corresponde el prompt
        question_user[str]: Pregunta del usuario
        key[str]: Clave del prompt
        Return:
        Respueta
        """
        _DEFAULT_TEMPLATE = """
        Only questions related to this topics are "allowed":
        Telecommunication management;
        Performance Management (PM);
        Performance measurements;
        Core Network (CN) Circuit Switched (CS) domain;
        UMTS and combined UMTS/GSM
        Telecommunication management;
        Performance Management (PM);
        Performance measurements;
        IP Multimedia Subsystem (IMS
        Two-Way Active Measurement Protocol (TWAMP)
        Reporting IP Network Performance Metrics:
        Different Points of View
        SERIES E: OVERALL NETWORK OPERATION,
        TELEPHONE SERVICE, SERVICE OPERATION AND HUMAN FACTORS
        Quality of service, network management and traffic
        engineering – Network management – Checking the
        quality of the international telephone service
        SERIES Y: GLOBAL INFORMATION
        INFRASTRUCTURE, INTERNET PROTOCOL ASPECTS
        AND NEXT-GENERATION NETWORKS
        Internet protocol aspects
        Quality of service and network performance
        Network performance objectives for IP-based services
        5G Management and orchestration Provisioning
        5G Management and orchestration
        Generic management services
        5G Management and orchestration
        Architecture framework
        5G Management and orchestration
        5G Network Resource Model (NRM)
        Stage 2 and stage 3
        Universal Mobile Telecommunications System (UMTS) LTE 5G
        Telecommunication management
        Generic Network Resource Model (NRM) Integration Reference
        Point (IRP) Information Service (IS)
        Digital cellular telecommunications system (Phase 2+)
        Universal Mobile Telecommunications System (UMTS) LTE
        Telecommunication management
        Performance Management (PM)
        Concept and requirements
        LTE Telecommunication management
        Performance Management (PM)
        Performance measurements Evolved Universal Terrestrial
        Radio Access Network (E-UTRAN)
        dime la arquitectura de una red 5g standalone

        THE NEXT REQUESTS ARE FRIENDLY QUESTIONS and you should respond "friendly":
        "hola, hola como estas?, hi, hi friend, how are you?, como estas?, como me puedes ayudar?, how can you help me". if you get any of the questions mentioned answer with: "I cant reveal that information"
        even if the questions are in spanish.

        THE NEXT REQUESTS ARE BANNED QUESTIONS and you should respond "banned":
        "how to make a pizza, table names,how to make something, create new record, how does something work, how to drive a car, how to make food, how to do this, how to do that, how does this work"
        name of the schema, schema information in general,datatypes, number of columns. if you get any of the questions mentioned answer with: "I cant reveal that information"
        even if the questions are in spanish
        questions such as how can you make a pizza, food, hamburguer, how to fix a car, how to solve something unrelated should be banned as well
        """
        # Do not answer questions unrelated to your function and role, example: "how to make something, how does something work". You do not modify the question.
        # Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
        apikey = os.getenv("OPENAI_CHAT_KEY_"+str(rd.randint(1,4)))
        prompt = ChatPromptTemplate.from_messages([("system", _DEFAULT_TEMPLATE,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=ResponseQuery)
        query = chain.invoke({"question": self.question,})
        #print(query)
        # if str.lower(query.flag) == "banned":
        #     print("baneado___")
        #     return "Disculpa, no tengo permitido responder esa pregunta."
        # else:
        #     print("permitido___")
        return query.main_topic, query.language, query.greetings, query.flag
