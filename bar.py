import streamlit as st

pages = {
    "Architecture": [
        st.Page("architecture_generation.py", title="Generate architecture"),
        st.Page("architecture_analysis.py", title="Analyze architecture"),
    ]
}

pg = st.navigation(pages)
pg.run()