import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
import regex_ban
# from perceptron import classiffier  # Uncomment if perceptron-based classification is needed
from typing import List
from dotenv import load_dotenv
import os
from utils import page_response  # Utility function for handling the response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from a .env file (e.g., for API keys)
load_dotenv()

# Set the OpenAI API key as an environment variable (from the .env file)
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# Configure the Streamlit page layout and appearance
st.set_page_config(
    page_title="Architecture generation",  # Title of the page
    page_icon="🧊",  # Icon of the page
    layout="wide",  # Layout style: wide for more space
    initial_sidebar_state="collapsed"  # Sidebar starts collapsed by default
)

# Initialize variables for output and user responses
response = ""
text_out = ""

# Create two equally sized columns for layout
col1, col2 = st.columns([1, 1])

# Column 1: User input form
with col1:
    # Form to capture user input (cloud platform selection and specifications)
    with st.form("Space_1"):
        # Dropdown menu for selecting a cloud platform (AWS, GCP, Azure)
        option = st.selectbox("Select a cloud platform:", ("AWS", "GCP", "Azure"))
        st.write("You selected:", option)  # Display selected cloud platform
        logging.info(f"Cloud platform selected: {option}")

        # Text area for entering the specifications (e.g., architecture description)
        text_input = st.text_area(label="Enter the specifications", height=60)

        # Submit button for the form
        buttom_check = st.form_submit_button(label="Submit")

# Column 2: Processing user input and generating the response based on cloud platform
with col2:
    # Check if the submit button was clicked, the selected option is AWS, and text input is provided
    if buttom_check and option == 'AWS' and text_input:
        logging.info("Submit button pressed with AWS selected and text input provided.")
        # Call page_response function for AWS-specific architecture generation
        response = page_response(text_input=text_input, option="AWS")

    # Check if the submit button was clicked, the selected option is GCP, and text input is provided
    elif buttom_check and option == 'GCP' and text_input:
        logging.info("Submit button pressed with GCP selected and text input provided.")
        # Call page_response function for GCP-specific architecture generation
        response = page_response(text_input=text_input, option="GCP")

    # Check if the submit button was clicked, the selected option is Azure, and text input is provided
    elif buttom_check and option == 'Azure' and text_input:
        logging.info("Submit button pressed with Azure selected and text input provided.")
        # Call page_response function for Azure-specific architecture generation
        response = page_response(text_input=text_input, option="Azure")

# Display the generated response (diagram or architecture details)
st.write(response)
logging.info("Response displayed.")
