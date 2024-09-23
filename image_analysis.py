import os
#import warnings
#import psycopg2
import numpy as np
#import random as rd
import collections
import sys
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableSet
    collections.MutableSet = collections.abc.MutableSet
    collections.MutableMapping = collections.abc.MutableMapping
else:
    from collections import MutableSet, MutableMapping
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
load_dotenv()

os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class LLM_DiagramAnalyzer:
    """
    Class to analyze software architecture diagrams using a software architecture model (LLM).

    Attributes:
    image_path (str): Path of the diagram image.
    question (str): Question related to the diagram.

    Methods:
    __init__(self, image_path, question):
        Initializes the image_path and question attributes.

    diagram_analysis(self):
        Analyzes the diagram using a large language model (LLM) and returns the components, 
        service connections, explanation, feasibility and advantages/disadvantages of the diagram.
    """
    
    def __init__(self, image_path, question):
        """
        Initializes an instance of LLM_DiagramAnalyzer.

        Parameters:
        image_path (str): Path of the diagram image.
        question (str): Question related to the diagram.
        """
        self.image_path = image_path
        self.question = question

    def diagram_analysis(self):
        """
        Analyzes the diagram using a large language model (LLM).

        Uses a prompt template to generate a request to the language model, 
        which parses the diagram and provides a detailed response.

        Returns:
        tuple: contains the diagram components, service connections, explanation, feasibility and advantages/disadvantages.
        """
        # Template to analyze a diagram
        template = """You are an expert in analyzing software architecture diagrams. 
                      You are provided with an image and the following question:
                      Analyze the diagram, identify the architectural components, services, and explain their connections.
                      Provide a detailed response."""

        apikey = os.getenv("OPENAI_API_KEY")
        
        # Creation of the prompt template and access to the API
        prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", "Image: {image_path}, Question: {question}")
        ])

        llm = ChatOpenAI(openai_api_key=apikey, model="gpt-4", temperature=0)

        # Definition of the output scheme for structuring responses
        class Image_ResponseDiagram(BaseModel):
            components: Optional[str] = Field(..., description="Lista de componentes presentados en la imagen")
            service_connections: Optional[str] = Field(..., description="Todas las conexiones presentes en la imagen")
            explanation: Optional[str] = Field(..., description="Explicación detallada de todos los componentes presentados en la imagen")
            is_viable: Optional[str] = Field(..., description="Explicación detallada de por qué el diagrama podría ser viable o no viable")
            advantages_disadvantages: Optional[str] = Field(..., description="Lista detallada de ventajas y desventajas de la solución proporcionada")

        # Linking the prompt template to the LLM and the structured output
        chain = prompt | llm.with_structured_output(schema=Image_ResponseDiagram)

        # Pass image and query to the chain for processing
        result = chain.invoke({
            "image_path": self.image_path,
            "question": self.question
        })

        return (result.components,
                result.service_connections,
                result.explanation,
                result.is_viable,
                result.advantages_disadvantages)






