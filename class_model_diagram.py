import os
#import warnings
#import psycopg2
#import numpy as np
#import random as rd
import collections
import sys
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableSet
    collections.MutableSet = collections.abc.MutableSet
    collections.MutableMapping = collections.abc.MutableMapping

else:
    from collections import MutableSet, MutableMapping

from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
#from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class Response_diagram(BaseModel):
    """Result topic query"""
    arch_requisites: Optional[str] = Field(..., description="technical requistions for the architecture")
    #language: Optional[str] = Field(..., description="The language in which the user input was written, either ""ENGLISH"" or ""SPANISH""")
    python_diagram_runnable: Optional[str] = Field(...,description="the diagram architecture made into runnable code made with the python ""diagram"" package")
    explanation: Optional[str] = Field(..., description="Explanation of the Diagram architecture generated")
    service_connections: Optional[str] = Field(..., description="Explanation of the connections between the hyperscaler services")

class Response_diagram_improvements(BaseModel):


class LLM_Diagram:
    def __init__(self, question):
        self.question = question
    def diagram_first_answer(self):
        template = """you are a software architecture expert, you must create a diagram following the next indications {user_input}"
             f"using the ""diagrams"" python package, the code should be runnable"""

        apikey = os.getenv("OPENAI_API_KEY")
        prompt = ChatPromptTemplate.from_messages([("system", template,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=Response_diagram)
        print(self.question)
        diagram_answer = chain.invoke({"question": template, "user_input": self.question})
        return diagram_answer.arch_requisites, diagram_answer.python_diagram_runnable, diagram_answer.explanation

    def diagram_improve_response(self):
        template = """you are a software architecture expert, you are given python code to generate a diagram 
        f"using the ""diagrams"" python package, the code should be runnable, and comply with the client expectations, 
        revise that the code is runnable, the description is accurate and the client needs are met"""

        apikey = os.getenv("OPENAI_API_KEY")
        prompt = ChatPromptTemplate.from_messages([("system", template,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=Response_diagram_improvements)
        print(self.question)
        diagram_answer = chain.invoke({"question": template, "user_input": self.question})
        return diagram_answer.arch_requisites, diagram_answer.python_diagram_runnable, diagram_answer.explanation

user_input_example = """A user accesses the web application via the Load Balancer (ELB).
The load balancer distributes incoming traffic among a cluster of EC2 Web Servers.
The web servers interact with a relational database (RDS) to retrieve and store data.
The web servers also use S3 for storing files."""

answer = LLM_Diagram(user_input_example).diagram_first_answer()
print(answer)









