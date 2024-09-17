import streamlit as st 
from PIL import Image
import requests
from io import BytesIO


st.title("Lorem ipsum dolor sit amet")

col1, col2 = st.columns(2)

with col1:
    with st.form("Space_1"):
        option = st.selectbox(
        "Select a cloud platform:",
        ("AWS", "GCP", "Azure"),
        )
        
        st.write("You selected:", option)
        
        text_input = st.text_input(
        "Enter the required specifications",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )
        
        buttom_check = st.form_submit_button(label="Submit")

with col2:
    if buttom_check and option == 'AWS' and text_input:
        
        url= "https://github.com/Ikelly99/Diagram_creation_model/blob/main/front_src/paper_plane.jpg"
        
        response = requests.get(url, verify=False)
        
        image = Image.open(BytesIO(response.content))

        st.image(image, caption="A little paper plane thinking big.")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")
        
    elif buttom_check and option == 'GCP' and text_input:
        url = "https://github.com/Ikelly99/Diagram_creation_model/blob/main/front_src/paper_planes.jpg"
        
        response = requests.get(url)
        
        image = Image.open(BytesIO(response.content))

        st.image(image, caption="Some paper planes flying")

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


    
    
