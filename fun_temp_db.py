from datetime import datetime
import polars as pl
import os

def get_values(user_input, lang_response, lang_answer, image):
  route = os.path.abspath(os.getcwd()) + r"\local_data\first_test.csv"
  values_dic = {
                'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                'User_input': user_input, 
                'Response': lang_response, 
                'diagram_code': lang_answer,
                'diagram_image': str(image)
                }
  df_new = pl.DataFrame(values_dic)
  
  df_new.write_csv(route)
    
  return "All working"