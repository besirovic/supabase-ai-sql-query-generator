import streamlit as st

def schema_explorer(schema_text: str, schema_json: list) -> None:
    """
    Display the schema explorer component with an option to explore schema as text or JSON

    Receives:
    - schema_text: str - Database schema as plain text
    - schema_json: list - Database schema as JSON

    Returns: None
    """

    text_tab, json_tab = st.tabs(["Text", "JSON"])

    with text_tab:
        container = text_tab.container(height=650)
        container.write(schema_text)
    with json_tab:
        container = json_tab.container(height=650)
        container.write(schema_json)
