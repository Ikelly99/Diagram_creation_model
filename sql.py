from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, LargeBinary, insert
from datetime import datetime

# Create the database engine
engine = create_engine('db_url')

# Connect to the engine
conn = engine.connect()

# Set metadata
metadata = MetaData()

# Define the 'inputs' table
inputs = Table(
    'inputs', metadata,
    Column('Id', Integer, primary_key=True),
    Column('Timestamp', String(), nullable=False),
    Column('User_input', String(), nullable=False),
    Column('Response', String()),
    Column('diagram_code', Text, default=''),
    Column('diagram_image', LargeBinary, default=None)
)

# Create all tables in the database
metadata.create_all(engine)

# Insert data query
query = insert(inputs)

def get_values(user_input, lang_answer, image):
    """
    Prepare the values to be inserted into the 'inputs' table.

    Args:
        user_input (str): The user's input.
        lang_answer (str): The language answer or code.
        image (bytes): The image data in binary format.

    Returns:
        list: A list of dictionaries containing the values to be inserted.
    """
    values_list = [
        {
            'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
            'User_input': user_input, 
            'Response': False, 
            'diagram_code': lang_answer,
            'diagram_image': image
        }
    ]
    
    return values_list

# Example usage of get_values function
user_input = "Example input"
lang_answer = "Example code"
image = b'Example binary data'

values_list = get_values(user_input, lang_answer, image)

# Execute the insert query
result = conn.execute(query, values_list)

# Close the connection
conn.close()
