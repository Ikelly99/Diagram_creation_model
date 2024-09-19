import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

pages = {
    "Architecture": [
        st.Page("architecture_generation.py", title="Generate architecture"),
        st.Page("architecture_analysis.py", title="Analyze architecture"),
    ]
}

pg = st.navigation(pages)
pg.run()