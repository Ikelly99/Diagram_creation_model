import os
import source.utils as getkey
from typing import Optional
from dotenv import load_dotenv
from source.template_prompt import TEMPLATE_CLASSIFICATION
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class ResponseQuery(BaseModel):
    """
    Deteccion de elementos en la respuesta del modelo ChatOpenAI
    """
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
        prompt = ChatPromptTemplate.from_messages([("system", TEMPLATE_CLASSIFICATION,), ("human", "Question: {question}"), ])
        apikey = getkey.get_key_openai("OPENAI_CHAT_KEY_")
        llm = ChatOpenAI(openai_api_key=os.getenv(apikey), model= "gpt-4o", temperature=0)
        chain = prompt | llm.with_structured_output(schema=ResponseQuery)
        query = chain.invoke({"question": self.question,})
        return query.main_topic, query.language, query.greetings, query.flag
