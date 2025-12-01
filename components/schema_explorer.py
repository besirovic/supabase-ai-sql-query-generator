import streamlit as st

def schema_explorer(schema_text: str, schema_json: list) -> None:
    """
    Display the schema explorer component with an option to explore schema as text or JSON

    Receives:
    - schema_text: str - Database schema as plain text
    - schema_json: list - Database schema as JSON

    Returns: None
    """

    # Display a schema explore tabs
    text_tab, json_tab = st.tabs(["Text", "JSON"])

    # Display tab for schema text
    with text_tab:
        container = text_tab.container(height=650)
        container.write(schema_text)

    # Display tab for JSON schema
    with json_tab:
        container = json_tab.container(height=650)
        container.write(schema_json)
