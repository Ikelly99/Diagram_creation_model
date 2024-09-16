import os
import json
import datetime
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken
import task as task
#from db_vector_v3 import DBvector
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

# Load environment variables from .env file
load_dotenv()

# Set environment variables for OpenAI and Azure OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def get_prompt(user_prompt:str):
    """
    Generate a prompt for the model based on user input.

    Args:
        user_prompt (str): The user's input.

    Returns:
        str: The generated prompt.
    """
    prompt = (f"""you are a software architecture expert, you must create a diagram following the next indications '{user_prompt}'
               using the 'diagrams' python package, the code should be runnable""")
    
    return prompt

class Agent:
    def __init__(self,, client=OpenAI(), max_iter=3) -> None:
        """
        Initialize the Agent class.

        Args:
            client (OpenAI): The OpenAI client.
            max_iter (int): Maximum number of iterations for revising responses.
        """
        self.max_iter = max_iter
        self.client = client
        self.token_count = 0
        
        
    def initial_answer(self)->str:
        """
        Generate the initial answer based on the user input.

        Returns:
            str: The initial answer.
        """
        prompt_qa = """"you are a software architecture expert, you must create a diagram following the next indications: '{user_input}',
                        using the 'diagrams' python package, the code should be runnable"""

        initial_completion = self.client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_qa}],
            model="gpt-3.5-turbo-0613"
        )
        return initial_completion.choices[0].message.content

    def revise_response(self, initial_message):
        """
        Revise the initial response to ensure it is runnable and meets the diagram requirements.

        Args:
            initial_message (str): The initial message to be revised.

        Returns:
            str: The revised response.
        """
        messages = [
                {"role": "system", "content": "you are a software architecture expert"},
                {"role": "system", "content": "you must revise that the next code is runnable and makes sense with the diagram requisites"},
                {"role": "system", "content": "respond with True if they follow the previous indications; if they do not follow the indications, respond with improvements that must be made, add from the new information if you need"},
                {"role": "user", "content": str(initial_message)}
        ]
        
        revisor_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0613",)
        
        revisor_response = revisor_completion.choices[0].message.content
        
        self.token_count += task.get_token_count(revisor_completion)
        
        return revisor_response

    def check_answer(self, first_response,improvements):
        """
        Check the initial response and make improvements based on the given instructions.

        Args:
            first_response (str): The initial response.
            improvements (str): The improvements to be made.

        Returns:
            str: The improved response.
        """
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
        """
        Answer human feedback by making improvements to the test cases.

        Args:
            response (str): The initial response.
            improvements (str): The improvements to be made.

        Returns:
            str: The improved response based on human feedback.
        """
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
        """
        Loop through the revision process until the response is correct or the maximum iterations are reached.

        Args:
            first_response (str): The initial response.
            revisor_response (str): The response from the revisor.

        Returns:
            str: The final revised response.
        """
        
        total_iter = 0
        
        last_response = first_response
        
        response = bool(revisor_response)
        
        if response != True:
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
        """
        Generate the final response after revisions.

        Returns:
            tuple: The final response and the token count.
        """
        
        first_response = self.initial_answer()
        
        revisor_response = self.revise_response(first_response)
        
        final_answer= self.revise_loop(first_response, revisor_response)
        
        return final_answer, self.token_count
