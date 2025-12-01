import streamlit as st

def query_form() -> tuple[bool, str, str]:
    """
    Shows the form for providing natural language queries that are used to
    prompt LLM together with database schema to get executable SQL queries.

    Returns:
        tuple[bool, str, str]
        A tuple where:
        - The first value is boolean indicating if the form is submitted
        - The second value is a user typed query
        - The third value is an OpenAI model
    """
    models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo' , 'gpt-4.1', 'gpt-4.1-mini', 'gpt-4.1-nano', 'gpt-4o', 'gpt-4-mini', 'gpt-5', 'gpt-5-codex', 'gpt-5-mini', 'gpt-5-nano', 'gpt-5-pro', 'gpt-5.1', 'gpt-5.1-mini', 'gpt-5.1-codex']

    with st.form(key="query_form"):
        model = st.selectbox(label="Select model", options=models)

        query: str | None = st.text_area("Enter your query in natural language")

        container = st.container(horizontal=True, horizontal_alignment="distribute")

        submitted = container.form_submit_button("Generate SQL query")

    return submitted, query, model
