import streamlit as st
from router import r1
from faq import ingest_faq_data, faq_chain, faqs_path
from sql import sql_chain

ingest_faq_data(faqs_path)

def ask(query):
    route = r1(query).name

    if route == 'faq':
        return faq_chain(query)
    
    elif route == 'sql':
        return sql_chain(query)
    
    else:
        return f"Route {route} is not applied yet"

st.title("E Commerce Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Write your query")

if query:
    with st.chat_message('user'):
        st.markdown(query)

    st.session_state.messages.append({
        'role': 'user',
        'content': query,
    })

    response = ask(query)

    with st.chat_message('assistant'):
        st.markdown(response)

    st.session_state.messages.append({
        'role': 'assistant',
        'content': response
    })
