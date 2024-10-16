import streamlit as st
import requests
from uuid import uuid4

def show_rag_chat():
    """RAG Chat interface for uploading files."""
    st.title("RAG Chat with Document Upload")
    
    uploaded_files = st.file_uploader("Upload PDF, PPT, or DOCX files", type=['pdf', 'pptx', 'docx'], accept_multiple_files=True)

    if st.button("Upload and Start Chat"):
        if uploaded_files:
            # Create a list of tuples for the files to upload
            files = []
            for file in uploaded_files:
                files.append(("files", (file.name, file, file.type)))

            # Sending files for processing
            upload_response = requests.post("http://localhost:5000/upload_files", files=files)
            if upload_response.status_code == 200:
                files_content = upload_response.json().get("files", [])

                # Prepare data for the /index API
                index_data = [
                    {
                        "filename": file['filename'],
                        "content": file['content']
                    }
                    for file in files_content
                ]

                # Call the /index API to get the session key
                index_response = requests.post("http://localhost:5000/index", json=index_data)
                if index_response.status_code == 200:
                    session_key = index_response.json().get("session_key")
                    st.session_state.session_key = session_key
                    st.success(f"Session created with key: {session_key}")
                else:
                    st.error("Failed to create session.")
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
