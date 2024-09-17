import streamlit as st 
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
st.title("Lorem ipsum dolor sit amet")

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
        topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
        if allowed == "allowed":
            arch_requisites, python_diagram_runnable, explanation, service_connections, image_file_name = LLM_Diagram(
                text_input).diagram_first_answer()
            print(python_diagram_runnable)
            run_code_and_return_image(python_diagram_runnable, image_file_name)
            message = explanation
        else:
            message = " Your message was flagged as malicious"
        #url= "https://github.com/Ikelly99/Diagram_creation_model/blob/main/front_src/paper_plane.jpg"
        
        #response = requests.get(url, verify=False)
        image_path = str(image_file_name) + ".png"
        image = Image.open(image_path)
        st.image(image, caption= image_path)
        txt = st.text_area(message)
        
    elif buttom_check and option == 'GCP' and text_input:
        url = "https://github.com/Ikelly99/Diagram_creation_model/blob/main/front_src/paper_planes.jpg"
        
        #response = requests.get(url)
        
        #image = Image.open(BytesIO(response.content))

        #st.image(image, caption="Some paper planes flying")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")
        
    elif buttom_check and option == 'Azure' and text_input:
        url = "https://github.com/Ikelly99/Diagram_creation_model/blob/main/front_src/a_lot_of_paper_planes.jpg"
        
        response = requests.get(url)
        
        image = Image.open(BytesIO(response.content))

        st.image(image, caption="A lot of paper planes")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")
        
    else:
        st.write("You have not entered the specifications")


    
    
