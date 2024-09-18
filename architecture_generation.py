import streamlit as st 
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
from regex_ban import analyze_prompt
from perceptron import classiffier
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

def page_response(text_input:str, option:str):
    tech = option
    global text_out
    
    text_input_user = text_input
    text_input = text_input + f", using only {option} services"
    
    # perceptron layer
    cla = classiffier([text_input_user])
    if analyze_prompt(text_input_user) == "Allowed" and cla == 1:
        topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
            
        if allowed == "allowed":
            arch_requisites, python_diagram_runnable, explanation,\
            service_connections, image_file_name = LLM_Diagram(text_input, tech).diagram_first_answer()
                
            run_code_and_return_image(python_diagram_runnable, image_file_name)

            if image_file_name[-4:] == ".png":
                image_path = image_file_name
            else: image_path = str(image_file_name) + ".png"

            text_out = "explanation: " + explanation + "\n Service connections: " + service_connections + "\n Architecture requisites: " + arch_requisites
            st.image(image_path, caption=str(image_path))
            with open(image_path, "rb") as file:
                st.download_button(
                label="Download architecture image",
                data=file,
                file_name=str(image_path),
                mime="image/png",
                )

        else:
            text_out = f" Your message was flagged as malicious: {cla}"
            st.write(text_out)

    else:
        text_out = f"Your message was flagged as malicious: {cla}"
        st.write(text_out)

st.set_page_config(
    page_title="Architecture generation",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed")
 
text_out = ""

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
        page_response(text_input=text_input, option="AWS")

    elif buttom_check and option == 'GCP' and text_input:
        page_response(text_input = text_input, option="GCP")

    elif buttom_check and option == 'Azure' and text_input:
        page_response(text_input = text_input, option = "Azure")

st.write(text_out)
