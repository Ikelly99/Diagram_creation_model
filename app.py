import streamlit as st
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables from .env file

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key as an environment variable from the loaded .env file
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# Define pages for the application with titles and corresponding Python script files
# These pages will be used to navigate between different functionalities (e.g., generating and analyzing architecture)
pages = {
    "Architecture": [
        # First page for architecture generation
        st.Page("architecture_generation.py", title="Generate architecture"),

        # Second page for architecture analysis
        st.Page("architecture_analysis.py", title="Analyze architecture"),
    ]
}

# Create a navigation object that allows switching between the defined pages
pg = st.navigation(pages)

# Run the selected page (either "Generate architecture" or "Analyze architecture")
pg.run()
