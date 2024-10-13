import streamlit as st
import requests

def show_rag_chat():
    """RAG Chat interface for uploading files."""
    st.title("RAG Chat with Document Upload")
    
    uploaded_files = st.file_uploader("Upload PDF, PPT, or DOCX files", type=['pdf', 'pptx', 'docx'], accept_multiple_files=True)

    if st.button("Upload and Start Chat"):
        if uploaded_files:
            file_contents = []
            for uploaded_file in uploaded_files:
                file_contents.append({"filename": uploaded_file.name, "content": uploaded_file.getvalue().decode("utf-8")})
            
            response = requests.post("http://localhost:5000/upload_files", files={"files": uploaded_files})
            if response.status_code == 200:
                session_key = response.json().get("session_key")
                st.session_state.session_key = session_key
                st.success(f"Session created with key: {session_key}")
            else:
                st.error("Failed to upload files.")
        else:
            st.warning("Please upload at least one file to proceed.")

    user_question = st.text_input("Ask a question about the documents:")
    
    if st.button("Send"):
        if user_question and 'session_key' in st.session_state:
            response = requests.post("http://localhost:5000/chat", json={"session_key": st.session_state.session_key, "question": user_question})
            answer = response.json().get('answer', "No answer found.")
            st.success("Bot: " + answer)
