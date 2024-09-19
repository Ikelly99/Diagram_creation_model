from perceptron import classiffier
import regex_ban
from input_validator import LLMConnect
import os
from dotenv import load_dotenv
from image_analysis import LLM_DiagramAnalyzer
from class_model_diagram import LLM_Diagram
import streamlit as st

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def filter(text_input):
    cla = classiffier([text_input])[0]
    analyze_prompt = regex_ban.analyze_prompt(text_input)
    topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
    if allowed == "allowed":
        allowed = 1
    else:
        allowed = 0
    if analyze_prompt.lower() == "allowed":
        analyze_prompt = 1
    else:
        analyze_prompt = 0
    filter_sum = int(cla) + int(analyze_prompt) + int(allowed)
    return filter_sum,  f"{allowed}, {analyze_prompt}, {cla}"


def page_response(text_input: str, option: str):
    tech = option
    global text_out

    text_input_user = text_input
    text_input = text_input + f", using only {option} services"
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
                    break
            else:
                break

        if image_file_name[-4:] == ".png":
            image_path = image_file_name
        else:
            image_path = str(image_file_name) + ".png"

        text_out = "explanation: " + explanation + "\n Service connections: " + service_connections + "\n Architecture requisites: " + arch_requisites
        st.image(image_path, caption=str(image_path))
        st.write(text_out)
        with open(image_path, "rb") as file:
            st.download_button(
                label="Download architecture image",
                data=file,
                file_name=str(image_path),
                mime="image/png",
            )
        return text_out