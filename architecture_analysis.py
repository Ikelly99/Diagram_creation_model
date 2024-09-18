import streamlit as st

st.title("Architecture analysis")

st.set_page_config(
    page_title="Codd",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed")

col1, col2 = st.columns([1,1])


with col1:
    uploaded_files = st.file_uploader(
        "Choose a CSV file", accept_multiple_files=True)
    txt_input = st.text_area("Enter a short description of the diagram")


with col2:
    st.write(f"You wrote {len(txt)} characters.")