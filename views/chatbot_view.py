import streamlit as st
from config import UPLOAD_NEW, ALREADY_UPLOADED
from controllers.chatbot_controller import start_chatbot, handle_file_upload, display_uploaded_files

def main():
    st.title("Hi, I'm your Custom ChatBot!")

    content_type = st.sidebar.radio("Which Knowledge base you want to use?", [ALREADY_UPLOADED, UPLOAD_NEW])

    if content_type == UPLOAD_NEW:
        handle_file_upload()

    curr_dir = display_uploaded_files()

    if curr_dir and len(curr_dir):
        start_chatbot()
    else:
        st.header('No KB Loaded, use the left menu to start')

if __name__ == "__main__":
    main()
