import streamlit as st

from components import query_form, connection_form, schema_explorer
from services import Supabase, LLM

def main():
    supabase = Supabase()

    if 'session_established' not in st.session_state:
        st.session_state['session_established'] = False

    if st.session_state['session_established']:
        st.badge('CONNECTED', color="green")
    st.write('# Supabase AI Query Generator')
    st.write('> Explore Supabase database by using natural language')

    if not st.session_state['session_established']:
        submitted, connection_url, openai_api_key = connection_form()

        st.session_state['openai_api_key'] = openai_api_key

        if submitted:
            with st.spinner('Connecting...'):
                try:
                    supabase.connect(connection_url)
                    supabase.fetch_schema()
                    st.session_state['session_established'] = True
                except Exception as e:
                    st.error('Could not connect to Supabase')

                if st.session_state['session_established']:
                    st.rerun()

    else:
        if 'query_submitted' not in st.session_state:
            st.session_state['query_submitted'] = False

        if 'sql' not in st.session_state:
            st.session_state['sql'] = None

        llm = LLM(st.session_state['openai_api_key'])

        generator_tab, explorer_tab = st.tabs(["Schema Generator", "Schema Explorer"])
        schema_text = supabase.get_schema_as_text()
        schema_json = supabase.get_schema_as_json()

        with generator_tab:
            if not st.session_state['query_submitted']:
                submitted, query, model = query_form()

                if submitted and query:
                    with st.spinner('Generating your query...'):
                        try:
                            sql = llm.generate_sql(model=model, query=query, database_schema=schema_text)
                            st.session_state['sql'] = sql
                            st.session_state['query_submitted'] = True
                            st.rerun()
                        except Exception as e:
                            st.error('Could not generate SQL')
            else:
                st.write("### Here is your SQL query")
                st.code(st.session_state.sql, language="sql")
                go_over = st.button('Go over')
                if go_over:
                    st.session_state['query_submitted'] = False
                    st.session_state['sql'] = None
                    st.rerun()

        with explorer_tab:
            schema_explorer(schema_text, schema_json)

if __name__ == "__main__":
    main()