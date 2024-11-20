import streamlit as st
import os
import logging  # Import logging module
from dotenv import load_dotenv  # Import dotenv to load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()
logger.info("Environment variables loaded from .env file")

# Set the OpenAI API key as an environment variable from the loaded .env file
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    logger.info("OpenAI API key set successfully")
else:
    logger.error("OpenAI API key not found in environment variables")

# Define pages for the application with titles and corresponding Python script files
# These pages will be used to navigate between different functionalities (e.g., generating and analyzing architecture)
pages = {
    "Architecture": [
        # First page for architecture generation
        st.Page("architecture_generation.py", title="Generate architecture"),
        logger.info("Page 'Generate architecture' added"),

        # Second page for architecture analysis
        st.Page("architecture_analysis.py", title="Analyze architecture"),
        logger.info("Page 'Analyze architecture' added"),
    ]
}

# Create a navigation object that allows switching between the defined pages
pg = st.navigation(pages)
logger.info("Navigation object created")

# Run the selected page (either "Generate architecture" or "Analyze architecture")
pg.run()
logger.info("Application started")
