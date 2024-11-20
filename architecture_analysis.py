import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
import regex_ban
# from perceptron import classiffier  # Uncomment if perceptron-based classification is needed
from image_analysis import LLM_DiagramAnalyzer
from PIL import Image
import PIL
import os
import dotenv
from dotenv import load_dotenv
from utils import filter
import logging

# Initialize output text variable
text_out = ""

# Set environment variables for OpenAI API key and type
os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Streamlit page layout
st.set_page_config(
    page_title="Architecture analysis",  # Title of the page
    page_icon="🧊",  # Icon of the page
    layout="wide",  # Layout type: full-width
    initial_sidebar_state="collapsed"  # Sidebar is collapsed by default
)

# Create two equally sized columns for layout
col1, col2 = st.columns([1, 1])

# Column 1: Input form for file upload and text description
with col1:
    with st.form("Space_1"):  # Define form inside column 1
        # File uploader: Accepts png, jpeg, jpg image files
        image_input = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=False)

        # Text area for user to enter a short description of the diagram
        text_input = st.text_area(label="Enter a short description of the diagram", height=60)

        # Submit button for the form
        buttom_check = st.form_submit_button(label="Submit")

        # If an image is uploaded, show file details and display the image
        if image_input is not None:
            file_details = {"FileName": image_input.name, "FileType": image_input.type}  # Gather file details
            st.write(file_details)  # Display file details
            st.image(image_input)  # Display uploaded image
            logging.info(f"Uploaded image: {image_input.name}")  # Log the image name

            # Save the uploaded image to the "uploaded_images" directory
            with open(os.path.join("uploaded_images", image_input.name), "wb") as f:
                f.write(image_input.getbuffer())  # Save the file buffer to disk
            st.success("Saved File")  # Show success message
            logging.info(f"Image {image_input.name} saved successfully.")  # Log image save success

# Column 2: Processing and displaying the analysis results
with col2:
    # If the user submits text input and the submit button is pressed
    if buttom_check and text_input:
        logging.info("Submit button pressed and text input provided.")  # Log form submission
        # Apply a filtering function to check for malicious content in the text input
        filter_sum, str_filter = filter(text_input)
        logging.info(f"Filter result: {filter_sum}, {str_filter}")  # Log filter results

        # If the filter detects potentially malicious content, show a warning message
        if filter_sum < 2:
            st.write(f"Your text was flagged as malicious, {str_filter}")
            logging.warning(f"Text flagged as malicious: {str_filter}")  # Log malicious text detection
        else:
            # Analyze the diagram using the provided image and text description
            components, service_connections, explanation, is_viable, Advantages_disadvantages = LLM_DiagramAnalyzer(
                os.path.join("uploaded_images", image_input.name), text_input).diagram_analysis()
            logging.info("Diagram analysis completed.")  # Log analysis completion

            # Format the output into markdown with headings for various analysis sections
            text_out = f"""
                        ### Components
                        {components}

                        ### Service connections
                        {service_connections}

                        ### Explanation
                        {explanation}

                        ### Is viable
                        {is_viable}

                        ### Advantages and Disadvantages
                        {Advantages_disadvantages}
                        """
            # Display the formatted analysis results in the app
            st.markdown(text_out)
            logging.info("Analysis results displayed.")  # Log display of results
