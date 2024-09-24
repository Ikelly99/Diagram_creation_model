import os
import sys
import logging
import source.utils as getkey
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableSet
    collections.MutableSet = collections.abc.MutableSet
    collections.MutableMapping = collections.abc.MutableMapping
from typing import Optional
from dotenv import load_dotenv
from source.template_prompt import TEMPLATE_CLASSIFICATION
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
logging.info("Environment variables loaded.")

class ResponseQuery(BaseModel):
    """
    Model for detecting elements in the response from a ChatOpenAI model.

    Attributes:
        main_topic (Optional[str]): Main topic of the user question.
        language (Optional[str]): The language in which the user input was written, either 'ENGLISH' or 'SPANISH'.
        flag (Optional[str]): Flags the question as banned or allowed.
        greetings (Optional[str]): Indicates if the user's question is a greeting, answering with 'YES' or 'NO'.
    """
    
    main_topic: Optional[str] = Field(..., description="Main topic of the user question")
    
    language: Optional[str] = Field(..., description="The language in which the user input was written, either 'ENGLISH' or 'SPANISH' ")
    
    flag: Optional[str] = Field(...,description="Flag the question as banned, or as an allowed question")
    
    greetings: Optional[str] = Field(..., description="Is the user question a greeting or salutation, answer with 'YES' or 'NO' ")

class LLMConnect:
    def __init__(self, question):
        """
        Initializes the class with the users question.

        Args:
            question (str): Users question.
        """
        self.question = question
        logging.info(f"LLMConnect initialized with question: {question}")

    def connect_client_test(self):
        """
        Connects to the LLM client to validate the user's question.

        Returns:
            Tuple: Contains main_topic, language, greetings, and flag.
        """
        
        #  Create the prompt for the model
        prompt = ChatPromptTemplate.from_messages([(
                "system", TEMPLATE_CLASSIFICATION,), 
               ("human", "Question: {question}") 
            ])
        logging.info("Chat prompt template created.")
        
        # Get the OpenAI API key
        apikey = getkey.get_key_openai("OPENAI_API_KEY")
        logging.info("OpenAI API key retrieved.")
        
        # Initialize the ChatOpenAI model with the API key and specified model
        llm = ChatOpenAI(openai_api_key=os.getenv(apikey), model= "gpt-4o", temperature=0)
        logging.info("ChatOpenAI instance created.")
        
        # Create the processing chain with the prompt and the model
        chain = prompt | llm.with_structured_output(schema=ResponseQuery)
        logging.info("LLM chain created.")
        
        # Invoke the chain with the user's question
        query = chain.invoke({"question": self.question,})
        logging.info("LLM chain invoked with question.")
        
        # Return the results of the query
        return query.main_topic, query.language, query.greetings, query.flag
