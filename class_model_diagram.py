import logging
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
from strings_azure_gcp.strings_azure_gcp import dic_tech
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
    image_file_name: Optional[str] = Field(..., description="image filename, specified in the code")

class Response_diagram_improvements(BaseModel):
    Improvements: Optional[str] = Field(..., description="Improved that could be made to the diagram or the explanation")
    python_diagram_runnable_improved: Optional[str] = Field(...,description="the improved diagram architecture made into runnable code made with the python ""diagram"" package and documentation")
class LLM_Diagram:
    def __init__(self, question, tech):
        self.question = question
        self.tech = tech
    def diagram_first_answer(self):
        template = """you are a software architecture expert, you must create a diagram following the next indications {user_input}"
             f"using the ""diagrams"" python package""" + f",with the following documentation{dic_tech[self.tech]} the code should be runnable, correctly write the names and illustrations of the components in the generated code"

        apikey = os.getenv("OPENAI_API_KEY")
        prompt = ChatPromptTemplate.from_messages([("system", template,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=Response_diagram)
#        print(self.question)
        diagram_answer = chain.invoke({"question": template, "user_input": self.question})
        #print(diagram_answer.python_diagram_runnable)
        return (diagram_answer.arch_requisites,
                diagram_answer.python_diagram_runnable,
                diagram_answer.explanation,
                diagram_answer.service_connections,
                diagram_answer.image_file_name)

    def diagram_improve_response_reflexor(self, python_diagram_runnable, arch_requisites, service_connections, explanation):
        template = f"""you are a software architecture expert, you are given python code to generate a diagram 
        f"using the ""diagrams"" python package, the code should be runnable, and comply with the client expectations, 
        revise that the code is runnable and goes in accordance with the architecture {dic_tech[self.tech]},
        diagram code: {python_diagram_runnable},
        explanation {explanation},{arch_requisites},{service_connections}""" + """
        the explanation is accurate and the client needs are met, client description: {user_input}, dont forget to add essential 
        components of the architecture such as:
        1. **Presentation Layer**: The user interface for interaction (web, mobile, desktop).
2. **Business Logic Layer**: Manages the core functionality and rules of the system.
3. **Data Layer**: Handles data storage and retrieval (SQL/NoSQL databases).
4. **Integration Layer**: Facilitates communication between services and external APIs.
5. **Security Layer**: Ensures system protection with authentication, encryption, and security controls.
6. **Infrastructure Layer**: Physical/virtual resources for deploying and running the system (servers, cloud, containers).
7. **Monitoring and Observability**: Tracks performance, errors, and logs for system health and diagnostics.
8. **Development and Deployment (DevOps)**: Automates software delivery and infrastructure management (CI/CD, testing).
9. **Scalability and Performance**: Ensures the system can handle growth and maintain high performance.
10. **Backup and Disaster Recovery**: Protects against data loss and ensures recovery in failure scenarios.
11. **Compliance and Governance**: Ensures adherence to legal and regulatory standards.
12. **User Experience (UX) and Accessibility**: Focuses on interface design and making the system accessible to all users."""

        apikey = os.getenv("OPENAI_API_KEY")
        prompt = ChatPromptTemplate.from_messages([("system", template,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=Response_diagram_improvements)
        #print(self.question)
        diagram_answer = chain.invoke({"question": template, "user_input": self.question})
        return diagram_answer.Improvements, diagram_answer.python_diagram_runnable_improved

    def diagram_answer_improved(self, improvements, python_diagram_runnable_improved):
        template = """you are a software architecture expert, you must create a diagram following the next indications {user_input}"
            f"using the ""diagrams"" python package""" + f",with the following documentation{dic_tech[self.tech]} " + """
            the code should be runnable, correctly write the names and illustrations of the components in the generated code""" + f"""
            Take into account the next improvement considerations {improvements}, and make improvements to this code {python_diagram_runnable_improved}
            """

        apikey = os.getenv("OPENAI_API_KEY")
        prompt = ChatPromptTemplate.from_messages([("system", template,), ("human", "Question: {question}"), ])
        llm = ChatOpenAI(openai_api_key=apikey, model="gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=Response_diagram)
        #        print(self.question)
        diagram_answer = chain.invoke({"question": template, "user_input": self.question})
        #print(diagram_answer.python_diagram_runnable)
        return (diagram_answer.arch_requisites,
                diagram_answer.python_diagram_runnable,
                diagram_answer.explanation,
                diagram_answer.service_connections,
                diagram_answer.image_file_name)
def final_answer(user_input:str, tech:str):
    arch_requisites,python_diagram_runnable,explanation,service_connections,image_file_name = LLM_Diagram(user_input, tech).diagram_first_answer()
    logging.info("llm_diagram: diagram_first_answer")
    improvements, python_diagram_runnable_improved = LLM_Diagram(
        user_input, tech).diagram_improve_response_reflexor(
        arch_requisites = arch_requisites, python_diagram_runnable= python_diagram_runnable, explanation= explanation, service_connections=service_connections)
    logging.info("llm_diagram: diagram_improve_response_reflexor")
    arch_requisites,python_diagram_runnable,explanation,service_connections,image_file_name = LLM_Diagram(
        user_input, tech).diagram_answer_improved(improvements, python_diagram_runnable_improved)

    return arch_requisites,python_diagram_runnable,explanation,service_connections,image_file_name












