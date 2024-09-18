import streamlit as st 
from PIL import Image
import requests
from io import BytesIO
from input_validator import LLMConnect
from class_model_diagram import LLM_Diagram
from diagram_image_generation_test import run_code_and_return_image
from regex_ban import analyze_prompt
from perceptron import classiffier


#st.title("Architecture generation")

global text_out

text_out = ""

col1, col2 = st.columns([3.33,6.66])

with col1:
    #with st.container():
    with st.form("Space_1"):
        option = st.selectbox("Select a cloud platform:" , ("AWS", "GCP", "Azure"))
        st.write("You selected:", option)
        text_input = st.text_area(label="Enter the specifications")
        buttom_check = st.form_submit_button(label="Submit")

with col2:
    if buttom_check and option == 'AWS' and text_input:
        text_input = text_input + f", using only {option} services"
        
        # perceptron layer
        cla = classiffier([text_input])
        if analyze_prompt(text_input) == "Allowed" and cla == 1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
            
            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation,\
                    service_connections, image_file_name = LLM_Diagram(text_input).diagram_first_answer()
                
                run_code_and_return_image(python_diagram_runnable, image_file_name)
                
                image_path = str(image_file_name) + ".png"
                text_out = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
                st.image(image_path, caption=str(image_path))
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="Download architecture image",
                        data=file,
                        file_name=str(image_path),
                        mime="image/png",
                    )

            else:
                message = f" Your message was flagged as malicious: {cla}"
                st.write(message)

        else:
            message = f"Your message was flagged as malicious: {cla}"
            st.write(message)


    elif buttom_check and option == 'GCP' and text_input:
        text_input = text_input + f", using only {option} services"

        # perceptron layer
        cla = classiffier([text_input])
        if analyze_prompt(text_input) == "Allowed" and cla == 1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()

            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation, \
                    service_connections, image_file_name = LLM_Diagram(text_input).diagram_first_answer()

                run_code_and_return_image(python_diagram_runnable, image_file_name)

                image_path = str(image_file_name) + ".png"
                text_out = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
                st.image(image_path, caption=str(image_path))
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="Download architecture image",
                        data=file,
                        file_name=str(image_path),
                        mime="image/png",
                    )

            else:
                message = f" Your message was flagged as malicious: {cla}"
                st.write(message)

        else:
            message = f"Your message was flagged as malicious: {cla}"
            st.write(message)


    elif buttom_check and option == 'Azure' and text_input:
        text_input = text_input + f", using only {option} services"

        # perceptron layer
        cla = classiffier([text_input])
        if analyze_prompt(text_input) == "Allowed" and cla == 1:
            topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()

            if allowed == "allowed":
                arch_requisites, python_diagram_runnable, explanation, \
                    service_connections, image_file_name = LLM_Diagram(text_input).diagram_first_answer()

                run_code_and_return_image(python_diagram_runnable, image_file_name)

                image_path = str(image_file_name) + ".png"
                text_out = "explanation: " + explanation + "\n Service connnections: " + service_connections + "\n Architecture requisites: " + arch_requisites
                st.image(image_path, caption=str(image_path))
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="Download architecture image",
                        data=file,
                        file_name=str(image_path),
                        mime="image/png",
                    )

            else:
                message = f" Your message was flagged as malicious: {cla}"
                st.write(message)

        else:
            message = f"Your message was flagged as malicious: {cla}"
            st.write(message)

st.write(text_out)
