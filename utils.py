from perceptron import classiffier
import regex_ban
from input_validator import LLMConnect
import os
from dotenv import load_dotenv
from image_analysis import LLM_DiagramAnalyzer
from class_model_diagram import LLM_Diagram, final_answer
import streamlit as st
from diagram_image_generation_test import run_code_and_return_image
from fun_temp_db import get_values
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
logging.info("OpenAI API key set.")

def filter(text_input):    
    """
    Filters text input to determine whether it is allowed or disallowed.

    Parameters:
    text_input (str): The text input provided by the user.

    Returns:
    tuple: A tuple containing the sum of the filters and a string containing the filter results.
    """
    logging.info("Starting text input filtering.")
    cla = classiffier([text_input])[0]
    logging.info(f"Classifier result: {cla}")
    
    analyze_prompt = regex_ban.analyze_prompt(text_input)
    logging.info(f"Regex analysis result: {analyze_prompt}")
    
    topic, language, is_greeting, allowed = LLMConnect(text_input).connect_client_test()
    logging.info(f"LLMConnect results - Topic: {topic}, Language: {language}, Greeting: {is_greeting}, Allowed: {allowed}")
    
    allowed = 1 if allowed == "allowed" else 0
    analyze_prompt = 1 if analyze_prompt.lower() == "allowed" else 0

    filter_sum = int(cla) + int(analyze_prompt) + int(allowed)
    logging.info(f"Filter sum: {filter_sum}")

    return filter_sum, f"{allowed}, {analyze_prompt}, {cla}"

def page_response(text_input: str, option: str):
    """
    Generates a page response based on the text input and the selected option.

    Parameters:
    text_input (str): The text input provided by the user.
    option (str): The selected technical option.

    Returns:
    str: A response generated based on the text input and the selected option.
    """
    global text_out
    tech = option
    logging.info(f"Generating page response for option: {tech}")
    
    filter_sum, str_filter = filter(text_input)
    logging.info(f"Filter results: {str_filter}")
    
    if filter_sum < 2:
        st.write(f"Your text was flagged as malicious, {str_filter}")
        logging.warning("Text input flagged as malicious.")
    else:
        arch_requisites, python_diagram_runnable, explanation, \
            service_connections, image_file_name = final_answer(text_input, tech)
        logging.info("Final answer generated.")
        
        flag = 0
        while True:
            try:
                run_code_and_return_image(python_diagram_runnable, image_file_name)
                logging.info("Diagram image generated successfully.")
            except Exception as e:
                logging.error(f"Error generating diagram image: {e}")
                arch_requisites, python_diagram_runnable, explanation, \
                    service_connections, image_file_name = final_answer(text_input, tech)
                flag += 1
                if flag == 3:
                    st.write(f"We have a problem trying to make your diagram, please try later")
                    logging.error("Failed to generate diagram after 3 attempts.")
                    break
            else:
                break

        image_path = image_file_name if image_file_name[-4:] == ".png" else str(image_file_name) + ".png"
        try:
            st.image(image_path, caption=str(image_path))
            logging.info(f"Image displayed: {image_path}")
        except Exception as e:
            st.write("There was an error generating your image, please try later")
            logging.error(f"Error displaying image: {e}")

        with open(image_path, "rb") as file:
            st.download_button(
                label="Download architecture image",
                data=file,
                file_name=str(image_path),
                mime="image/png")
            logging.info("Download button created for image.")

        text_out = "explanation: " + explanation + "\n Service connections: " + service_connections + "\n Architecture requisites: " + arch_requisites
        
        with open(image_path, "rb") as file:
            get_values(text_input, text_out, python_diagram_runnable, file)
            logging.info("Values saved to temporary database.")
        
        return text_out
