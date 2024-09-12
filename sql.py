from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, LargeBinary, insert
from datetime import datetime

# Create engine db
engine = create_engine('db_url')

# Connect engine
conn = engine.connect()

# Set metadata
metadata = MetaData()

# Table
inputs = Table(
    'inputs', metadata,
    Column('Id', Integer, primary_key=True),
    Column('Timestamp', String(255), nullable=False),
    Column('User_input', String(255), nullable=False),
    Column('Response', String(255)),
    Column('diagram_code', Text, default=''),
    Column('diagram_image', LargeBinary, default=None)
)

# Crear todas las tablas en la base de datos
metadata.create_all(engine)

# Insertar datos
query = insert(inputs)

def get_values(user_input, lang_answer, image):
    values_list = [
        {'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
         'User_input': user_input, 'Response': False, 
         'diagram_code': lang_answer,
         'diagram_image': image}]
    
    return values_list
    
values_list = get_values()
result = conn.execute(query, values_list)

# Cerrar la conexión
conn.close()
 