import streamlit as st 
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
import regex_ban
# from perceptron import classiffier
from typing import List
from dotenv import load_dotenv
import os
from utils import page_response

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

st.set_page_config(
    page_title="Architecture generation",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed")
 
response = ""
text_out= ""
col1, col2 = st.columns([1,1])

with col1:
    #with st.container():
    with st.form("Space_1"):
        option = st.selectbox("Select a cloud platform:" , ("AWS", "GCP", "Azure"))
        st.write("You selected:", option)
        text_input = st.text_area(label="Enter the specifications", height=60)
        buttom_check = st.form_submit_button(label="Submit")

with col2:
    if buttom_check and option == 'AWS' and text_input:
        response = page_response(text_input=text_input, option="AWS")

    elif buttom_check and option == 'GCP' and text_input:
        response = page_response(text_input = text_input, option="GCP")

    elif buttom_check and option == 'Azure' and text_input:
        response = page_response(text_input = text_input, option = "Azure")

st.write(response)