import streamlit as st 
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
from regex_ban import analyze_prompt
st.title("Lorem ipsum dolor sit amet")
from perceptron import *

col1, col2 = st.columns(2)

with col1:
    with st.form("Space_1"):
        option = st.selectbox(
        "Select a cloud platform:",
        ("AWS", "GCP", "Azure"),
        )
        
        st.write("You selected:", option)
        
        text_input = st.text_input("Enter the required specifications",)
        buttom_check = st.form_submit_button(label="Submit")

with col2:
    if buttom_check and option == 'AWS' and text_input:
        option_message = f", using only {option} services"
        text_input = text_input + option_message
        cla = phrase_clasiffier(text_input)
        if analyze_prompt(text_input) == "Allowed" and cla==1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation, service_connections, image_file_name = LLM_Diagram(
                    text_input).diagram_first_answer()
                print(python_diagram_runnable)
                run_code_and_return_image(python_diagram_runnable, image_file_name)
                message = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
            else:
                message = " Your message was flagged as malicious"
        else:
            message = "Your message was flagged as malicious"
        image_path = str(image_file_name) + ".png"
        image = Image.open(image_path)
        st.image(image, caption=image_path)
        txt = st.text_area(message)
        
    elif buttom_check and option == 'GCP' and text_input:
        option_message = f", using only {option} services"
        text_input = text_input + option_message
        cla = phrase_clasiffier(text_input)
        if analyze_prompt(text_input) == "Allowed" and cla==1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation, service_connections, image_file_name = LLM_Diagram(
                    text_input).diagram_first_answer()
                print(python_diagram_runnable)
                run_code_and_return_image(python_diagram_runnable, image_file_name)
                message = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
            else:
                message = " Your message was flagged as malicious"
        else:
            message = "Your message was flagged as malicious"
        image_path = str(image_file_name) + ".png"
        image = Image.open(image_path)
        st.image(image, caption=image_path)
        txt = st.text_area(message)

    elif buttom_check and option == 'Azure' and text_input:
        option_message = f", using only {option} services"
        text_input = text_input + option_message
        cla = phrase_clasiffier(text_input)
        if analyze_prompt(text_input) == "Allowed" and cla==1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation, service_connections, image_file_name = LLM_Diagram(
                    text_input).diagram_first_answer()
                print(python_diagram_runnable)
                run_code_and_return_image(python_diagram_runnable, image_file_name)
                message = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
            else:
                message = " Your message was flagged as malicious"
        else:
            message = "Your message was flagged as malicious"
        image_path = str(image_file_name) + ".png"
        image = Image.open(image_path)
        st.image(image, caption=image_path)
        txt = st.text_area(message)
    else:
        st.write("You have not entered the specifications")


    
    
