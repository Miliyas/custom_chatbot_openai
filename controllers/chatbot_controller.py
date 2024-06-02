import hashlib
from datetime import datetime
import streamlit as st
from models.chatbot_model import initialize_models, get_answer
from utils.file_utils import save_uploaded_files, get_uploaded_files
from config import TMP_DIRECTORY, UPLOAD_NEW, ALREADY_UPLOADED

def start_chatbot():
    if "last_db_updated" not in st.session_state:
        st.session_state.last_db_updated = ''

    db, chain = initialize_models(st.session_state.last_db_updated)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_answer(prompt, db, chain)
            answer = full_response['answer']
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

def handle_file_upload():
    uploaded_files = st.sidebar.file_uploader("Choose a txt file", accept_multiple_files=True)

    if uploaded_files and len(uploaded_files):
        save_uploaded_files(uploaded_files, TMP_DIRECTORY)
        last_db_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.session_state.last_db_updated = hashlib.md5(','.join(get_uploaded_files(TMP_DIRECTORY)).encode()).hexdigest()

def display_uploaded_files():
    curr_dir = get_uploaded_files(TMP_DIRECTORY)
    st.sidebar.write("Current Knowledge Base")
    if curr_dir:
        st.sidebar.write(curr_dir)
    else:
        st.sidebar.write('**No KB Uploaded**')

    return curr_dir
