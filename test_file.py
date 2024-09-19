# @FerMoreno @Kelly
import os
import source.task as task
import readMD
import streamlit as st
from langsmith import Client
from dbvector import DBvector
from pinecone import Pinecone
from dotenv import load_dotenv
from langsmith import traceable
from source.graph_index import reponse_graph as index_books
# from input_validator import LLMConnect
from validator import LLMConnect
from langchain.chains import RetrievalQA
from source.task import split_pdf, process_page
from langchain import memory as lc_memory
from langchain_openai import OpenAIEmbeddings
from streamlit_feedback import streamlit_feedback
from langchain.memory import ConversationBufferMemory
from langchain_core.tracers.context import collect_runs
from langchain.vectorstores import Pinecone as pinelang
from langchain.vectorstores.utils import DistanceStrategy
load_dotenv()


#os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
#os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
#os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
#os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_CHAT_KEY_4")
#os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

def response_generator(user_input:str):
    input_validator_response = LLMConnect(user_input).connect_client_test()
    if (input_validator_response[-1]).lower() == "banned":
        return """Hola soy Arquitecto de soluciones , mi objetivo es ofrecerte diagramas de arquitectura de datos.
        Pero no tengo permitido contestar este tipo de preguntas {}
        """.format(user_input)
    else:
        if input_validator_response[2] == "YES" or user_input==None:
            response = task.greet_the_user(user_input)
            return response.content
        else: # generate response
            if index_books(user_question=user_input, tempetature_llm=0.1) == True:
                response = first_response(user_input)
                improved_response = task.improve_response(response[0].page_content,
                                                        user_language= input_validator_response[1],
                                                        aditional_question=user_input)
                return improved_response.content
            else:
                return """Hola en este momento no te puedo contestar {} porque no tengo información acerca de ese tema""".format(user_input)