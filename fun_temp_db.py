from datetime import datetime
import polars as pl


def get_values(user_input, lang_response, lang_answer, image):
  route = "C:/Users/rlagunaj/Desktop/FRONT/git/Diagram_creation_model/local_data/first_test.csv" 
  values_dic = {
                'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                'User_input': user_input, 
                'Response': lang_response, 
                'diagram_code': lang_answer,
                'diagram_image': image
                }
  df_new = pl.DataFrame(values_dic)
  
  df_new.write_csv(route)
    
  return "All working"