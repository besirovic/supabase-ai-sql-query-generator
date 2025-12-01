import streamlit as st

def connection_form() -> tuple[bool, str, str]:
    """
    Shows the form for providing a Supabase connection link

    Returns:
        tuple[bool, str, str]:
            A tuple where:
            - The first value is boolean indicating if the form is submitted
            - The second value is a Supabase connection link
            - The third value is an OpenAI API key
    """
    with st.form(key="connection_form"):
        connection_url = st.text_input(label="Enter your Supabase connection link to start")
        openai_api_key = st.text_input(label="Enter your OpenAI API key")
        submitted = st.form_submit_button("Connect to Supabase")

    return submitted, connection_url, openai_api_key