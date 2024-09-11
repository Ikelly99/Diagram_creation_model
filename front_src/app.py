import streamlit as st 
from PIL import Image

st.title("Lorem ipsum dolor sit amet")

col1, col2 = st.columns(2)

with col1:
    with st.form("Space_1"):
        option = st.selectbox(
        "Select a cloud platform:",
        ("AWS", "GCP", "Azure"),
        )
        
        st.write("You selected:", option)
        
        buttom_check = st.form_submit_button(label="Submit")

with col2:
    if buttom_check and option == 'AWS':
        image1 = Image.open("C:/Users/rlagunaj/Desktop/FRONT/Entorno/src/paper_plane.jpg")

        st.image(image1, caption="A little plane thinking big.")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")
        
    elif buttom_check and option == 'GCP':
        image1 = Image.open("C:/Users/rlagunaj/Desktop/FRONT/Entorno/src/paper_planes.jpg")

        st.image(image1, caption="Some paper planes flying")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")
        
    elif buttom_check and option == 'Azure':
        image1 = Image.open("C:/Users/rlagunaj/Desktop/FRONT/Entorno/src/a_lot_of_paper_planes.jpg")

        st.image(image1, caption="A lot of paper planes")

        txt = st.text_area(
            "Analysis:",
            """There are a little explaining about your question, please read all.
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet 
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet""")


    
    
