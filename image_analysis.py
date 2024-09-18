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
    def __init__(self, image_path, question):
        self.image_path = image_path
        self.question = question

    def diagram_analysis(self):
        # Template for analyzing a diagram
        template = """You are an expert in analyzing software architecture diagrams. 
                      You are provided with an image and the following question:
                      Analyze the diagram, identify the architectural components, services, and explain their connections.
                      Provide a detailed response."""

        apikey = os.getenv("OPENAI_API_KEY")
        # Creating prompt template and API access
        prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", "Image: {image_path}, Question: {question}")
        ])

        # Use GPT-4 for processing
        llm = ChatOpenAI(openai_api_key=apikey, model="gpt-4", temperature=0)

        # Define output schema to structure responses
        class Image_ResponseDiagram(BaseModel):
            components: Optional[str] = Field(..., description="List of components presented in the image")
            service_connections: Optional[str] = Field(...,
                                             description="All the connections present in the image")
            explanation: Optional[str] = Field(...,
                                             description="Robust explanation of all the components presented in the image")
            is_viable: Optional[str] = Field(...,description="Robust explanation of why the diagram could be viable or not viable")
            Advantages_disadvantages: Optional[str] = Field(...,description="Robust list of advantages and disadvantages of the solution provided")

        # Chain prompt template with the LLM and structured output
        chain = prompt | llm.with_structured_output(schema= Image_ResponseDiagram)

        # Pass image and question to the chain for processing
        result = chain.invoke({
            "image_path": self.image_path,
            "question": self.question
        })

        # Extract response data
        return (result.components,
                result.service_connections,
                result.explanation,
                result.is_viable,
                result.Advantages_disadvantages)

# Example usage
if __name__ == "__main__":
    diagram_analyzer = LLM_DiagramAnalyzer(image_path=r"C:\Users\ikellyra\PycharmProjects\Diagram_creation_model\generated_images\complex_web_architecture.png",
                                           question="What are the main services in this architecture?")

    components, service_connections, explanation, is_viable, Advantages_disadvantages = diagram_analyzer.diagram_analysis()

    print(f"Components Identified: {components}")
    print(f"Service Connections: {service_connections}")
    print(f"Explanation: {explanation}")
    print(f"is_viable: {is_viable}")
    print(f"Advantages_disadvantages: {Advantages_disadvantages}")

