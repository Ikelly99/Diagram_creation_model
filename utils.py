from perceptron import classiffier
import regex_ban
from input_validator import LLMConnect
import os
from dotenv import load_dotenv
from image_analysis import LLM_DiagramAnalyzer
from class_model_diagram import LLM_Diagram
import streamlit as st
from diagram_image_generation_test import run_code_and_return_image


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def filter(text_input):    
    cla = classiffier([text_input])[0]
    analyze_prompt = regex_ban.analyze_prompt(text_input)
    topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
    
    allowed = 1 if allowed == "allowed" else 0

    analyze_prompt = 1  if analyze_prompt.lower() == "allowed" else 0

    filter_sum = int(cla) + int(analyze_prompt) + int(allowed)

    return filter_sum,  f"{allowed}, {analyze_prompt}, {cla}"


def page_response(text_input: str, option: str):
    global text_out
    tech = option
    filter_sum, str_filter = filter(text_input)
    
    if filter_sum < 2:
        st.write(f"Your text was flagged as malicious, {str_filter}")
    else:
        arch_requisites, python_diagram_runnable, explanation, \
            service_connections, image_file_name = LLM_Diagram(text_input, tech).diagram_first_answer()
        flag = 0
        while True:
            try:
                run_code_and_return_image(python_diagram_runnable, image_file_name)
            except:
                arch_requisites, python_diagram_runnable, explanation, \
                    service_connections, image_file_name = LLM_Diagram(text_input, tech).diagram_first_answer()
                flag += 1
                if flag == 3:
                    st.write(f"We have a problem trying to make your diagram, plese try later")
                    break
            else:
                break

        image_path = image_file_name if image_file_name[-4:] == ".png" else str(image_file_name) + ".png"
        
        st.image(image_path, caption=str(image_path))
        st.write(text_out)

        with open(image_path, "rb") as file:
            st.download_button(
                label="Download architecture image",
                data=file,
                file_name=str(image_path),
                mime="image/png")
            
        text_out = "explanation: " + explanation + "\n Service connections: " + service_connections + "\n Architecture requisites: " + arch_requisites

        return text_out
