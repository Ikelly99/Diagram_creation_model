from datetime import datetime
import polars as pl


def get_values(user_input, lang_response, lang_answer, image):

    values_dic = {
                    'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                    'User_input': user_input, 
                    'Response': lang_response, 
                    'diagram_code': lang_answer,
                    'diagram_image': image
                  }
    pl_dic = pl.DataFrame(values_dic)

    pl_dic.write_csv("first_test.csv")
    
    return "All working"

user_input_p = "I add a some prompt about web architecture"

lang_response = "Here is the explanation of the architecture"

lang_answer = """print("Hello world")"""

image = "some thing"

first_test = get_values(user_input_p, lang_response, lang_answer, image)

print(pl.read_csv("first_test.csv"))
