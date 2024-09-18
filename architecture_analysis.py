import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
from regex_ban import analyze_prompt
from perceptron import classiffier
from image_analysis import LLM_DiagramAnalyzer
from PIL import Image
import PIL
import os
import dotenv
from dotenv import load_dotenv

text_out = ""

os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
st.set_page_config(
    page_title="Architecture analysis",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed")

col1, col2 = st.columns([1,1])

with col1:
    with st.form("Space_1"):
        image_input = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=False)
        text_input = st.text_area(label="Enter a short description of the diagram", height=60)
        buttom_check = st.form_submit_button(label="Submit")
        if image_input is not None:
            file_details = {"FileName": image_input.name, "FileType": image_input.type}
            st.write(file_details)
            st.image(image_input)
            print(image_input.name)
            with open(os.path.join("uploaded_images", image_input.name), "wb") as f:
                f.write(image_input.getbuffer())
            st.success("Saved File")


with col2:
    if buttom_check and text_input:
        st.write(text_out)
