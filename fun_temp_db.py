from datetime import datetime
import polars as pl
import os

def get_values(user_input, lang_response, lang_answer, image):
    """
    This function takes four parameters: user_input, lang_response, lang_answer and image.
    It creates a dictionary with these values along with a current timestamp.
    It then converts this dictionary into a DataFrame and saves it to a CSV file.

    Parameters:
    user_input (str): User input.
    lang_response (str): Response generated explaining the diagram.
    lang_answer (str): generated diagram code.
    image (str): Image of the diagram in string format.

    Returns:
    str: Confirmation message indicating that everything is working.
    """
    # Gets the absolute path to the CSV file where the data will be stored
    route = os.path.abspath(os.getcwd()) + r"\local_data\first_test.csv"
    
    # Creates a dictionary with the values provided and a timestamp
    values_dic = {
        'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
        'User_input': user_input, 
        'Response': lang_response, 
        'diagram_code': lang_answer,
        'diagram_image': str(image)
    }
    
    # Converts the dictionary to a DataFrame
    df_new = pl.DataFrame(values_dic)
    
    # Writes the DataFrame to a CSV file
    df_new.write_csv(route)
    
    return "All working"
