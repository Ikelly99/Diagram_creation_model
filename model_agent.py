import os
import json
import datetime
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken
import task as task
from db_vector_v3 import DBvector
from langsmith import traceable
from collections import defaultdict
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langgraph.graph import END, MessageGraph
from langchain_core.messages import ToolMessage
from langchain.pydantic_v1 import BaseModel, Field
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureOpenAIEmbeddings, AzureOpenAI, AzureChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
load_dotenv()
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
os.environ["AZURE_OPENAI_SERVICE"] = os.getenv("AZURE_OPENAI_SERVICE")
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["OPENAI_API_VERSION"] = os.getenv("AZURE_OPENAI_VERSION")
os.environ["AZURE_OPENAI_GPT_DEPLOYMENT"] = os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["azure_deployment"] = os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT")

def get_prompt(user_prompt:str):
    prompt = (f"you are a software architecture expert, you must create a diagram following the next indications {total_scenarios}"
             f"using the ""diagrams"" python package, the code should be runnable")
    return prompt

class Agent:
    def __init__(self,, client=OpenAI(), max_iter=3) -> None:
        self.max_iter = max_iter
        self.client = client
        self.token_count = 0
    def initial_answer(self)->str:
        prompt_qa = """"you are a software architecture expert, you must create a diagram following the next indications {user_input}"
             f"using the ""diagrams"" python package, the code should be runnable"""

        return initial_completion

    def revise_response(self, initial_message):
        messages = [
                {"role": "system", "content": "you are a software architecture expert"},
                {"role": "system", "content": "you must revise that the next code is runnable and makes sense with the diagram requisites"},
                {"role": "system", "content": "respond with True if they follow the previous indications; if they do not follow the indications, respond with improvements that must be made, add from the new information if you need"},
                {"role": "user", "content": str(initial_message)},
                #{"role": "user", "content": "new information:"+str(query_result)}
        ]
        revisor_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0613",)
        revisor_response = revisor_completion.choices[0].message.content
        self.token_count += task.get_token_count(revisor_completion)
        return revisor_response

    def check_answer(self, first_response,improvements):
        messages = [
            {"role": "system", "content": "You are a QA tester"},
            {"role": "system",
             "content": f"Given a series of test cases, make improvements to the cases following the next instructions and using the new information:"},
            {"role": "user", "content": "improvements: "+str(improvements)},
            {"role": "user", "content": "test cases: "+str(first_response)},
        ]
        improved_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0613", )
        improved_response = improved_completion.choices[0].message.content
        self.token_count += task.get_token_count(improved_response)
        return improved_response

    def answer_human_feedback(self, response,improvements):
        messages = [
            {"role": "system", "content": "You are a QA tester"},
            {"role": "system",
             "content": f"Given a series of test cases, make improvements to the cases following the next instructions and using the new information:"},
            {"role": "user", "content": "improvements: "+str(improvements)},
            {"role": "user", "content": "test cases: "+str(response)},
        ]
        improved_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0613", )
        improved_response = improved_completion.choices[0].message.content
        self.token_count += task.get_token_count(improved_response)
        return improved_response

    def revise_loop(self, first_response, revisor_response):
        total_iter = 0
        last_response = first_response
        response = bool(revisor_response)
        while response is not True and self.max_iter > total_iter:
            total_iter += 1
            print("RESPUESTA INCORRECTA")
            improved_response = self.check_answer(first_response, revisor_response)
            revisor_response= self.revise_response(improved_response)
            last_response= revisor_response
        else:
            print("RESPUESTA CORRECTA - iteraciones: "+str(total_iter))
        return last_response

    def generate_response(self):
        first_response = self.initial_answer()
        revisor_response = self.revise_response(first_response)
        final_answer= self.revise_loop(first_response, revisor_response)
        return final_answer, self.token_count