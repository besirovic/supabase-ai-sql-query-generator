import streamlit as st

from components import query_form, connection_form, schema_explorer
from services import Supabase, LLM

def main():
    # Initialise Supabase service
    supabase = Supabase()

    # Check if Supabase session has been stored in state
    # If not, set default value
    if 'session_established' not in st.session_state:
        st.session_state['session_established'] = False

    # Display green "CONNECTED" badge if session is established
    if st.session_state['session_established']:
        st.badge('CONNECTED', color="green")

    # Display app heading
    st.write('# Supabase AI Query Generator')
    st.write('> Explore Supabase database by using natural language')

    # Check if session is not established and display a connection form
    if not st.session_state['session_established']:
        # Display a connection form
        submitted, connection_url, openai_api_key = connection_form()

        # Store OpenAI API key in state
        st.session_state['openai_api_key'] = openai_api_key

        # If a connection form is submitted, display loader while fetching Supabase database schema
        if submitted:
            with st.spinner('Connecting...'):
                try:
                    # Establish the database connection
                    supabase.connect(connection_url)

                    # Fetch database schema
                    supabase.fetch_schema()

                    # Update session established state
                    st.session_state['session_established'] = True
                except Exception as e:
                    print("Error:", e)
                    # Display a message in case of error
                    st.error('Could not connect to Supabase')

                if st.session_state['session_established']:
                    # If the session is established, rerun Streamlit to update the UI
                    st.rerun()

    else:
        # Check if a query submitted state has been stored in state
        # If not, initialize an empty value
        if 'query_submitted' not in st.session_state:
            st.session_state['query_submitted'] = False

        # Check if generate SQL query has been stored in state
        # If not, initialize an empty value
        if 'sql' not in st.session_state:
            st.session_state['sql'] = None

        # Initialize LLM service
        llm = LLM(st.session_state['openai_api_key'])

        # Split generation form and schema explorer in tabs
        generator_tab, explorer_tab = st.tabs(["Schema Generator", "Schema Explorer"])

        # Get database schema as plain text
        schema_text = supabase.get_schema_as_text()

        # Get database schema in JSON format
        schema_json = supabase.get_schema_as_json()

        # Display query form tab
        with generator_tab:
            # If SQL code is not already generated, display a query form
            if not st.session_state['query_submitted']:
                # Get query form values
                submitted, query, model = query_form()

                # Check if a query is provided and form submitted
                if submitted and query:
                    # Display spinner while generating SQL code
                    with st.spinner('Generating your query...'):
                        try:
                            # Generate SQL code
                            sql = llm.generate_sql(model=model, query=query, database_schema=schema_text)

                            # Store generated SQL code in state
                            st.session_state['sql'] = sql
                            st.session_state['query_submitted'] = True

                            # Rerun Streamlit to update UI
                            st.rerun()
                        except Exception as e:
                            print("Error:", e)
                            # Display an error in case SQL code generation fails
                            st.error('Could not generate SQL')
            # If SQL code is generated, display the code
            else:
                st.write("### Here is your SQL query")
                st.warning("For your own safety, make sure to validate SQL code before executing it")
                st.code(st.session_state.sql, language="sql")

                # Go over button to reset the form
                go_over = st.button('Go over')
                if go_over:
                    st.session_state['query_submitted'] = False
                    st.session_state['sql'] = None
                    st.rerun()

        # Schema explorer tab
        with explorer_tab:
            schema_explorer(schema_text, schema_json)

    st.info("Check out source code on https://github.com/besirovic/supabase-ai-sql-query-generator")

if __name__ == "__main__":
    main()