import streamlit as st
import requests

def show_quiz():
    """Quiz Generation interface."""
    st.title("Generate a Quiz")
    
    topic = st.text_input("Enter a topic for the quiz:")
    uploaded_files = st.file_uploader("Or upload a file", type=['pdf', 'pptx', 'docx'], accept_multiple_files=True)

    if st.button("Generate Quiz"):
        if topic or uploaded_files:
            data = {}

            if topic:
                data["topic"] = topic
                response = requests.post("http://localhost:5000/quiz/generate/topic", json=data)
                if response.status_code == 200:
                    st.success("Quiz generated successfully from topic!")
                    quiz_data = response.json()
                    st.write(quiz_data)
                else:
                    st.error("Failed to generate quiz from topic.")

            if uploaded_files:
                files = []
                for file in uploaded_files:
                    files.append(("files", (file.name, file, file.type)))

                upload_response = requests.post("http://localhost:5000/upload_files", files=files)
                if upload_response.status_code == 200:
                    uploaded_content = upload_response.json()
                    processed_files = uploaded_content.get("files")

                    combined_content = "\n".join([file["content"] for file in processed_files])

                    quiz_data = {
                        "text_content": combined_content,
                        "level": "medium" 
                    }

                    quiz_response = requests.post("http://localhost:5000/quiz/generate/content", json=quiz_data)
                    if quiz_response.status_code == 200:
                        st.success("Quiz generated successfully from uploaded files!")
                        st.write(quiz_response.json()) 
                    else:
                        st.error("Failed to generate quiz from uploaded files.")
                        st.write(quiz_response.json().get("error", "Unknown error occurred."))
                else:
                    st.error("Failed to upload files.")
                    st.write(upload_response.json().get("message", "Unknown error occurred during file upload."))
        else:
            st.error("Please provide a topic or upload a file to generate a quiz.")
