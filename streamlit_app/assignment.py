import streamlit as st
import requests

def show_assignment():
    st.title("Generate an Assignment")
    
    topic = st.text_input("Enter a topic for the assignment:")
    uploaded_files = st.file_uploader("Or upload a file", type=['pdf', 'pptx', 'docx'], accept_multiple_files=True)
    
    level = st.selectbox("Select the assignment level:", options=["easy", "medium", "hard"])

    if st.button("Generate Assignment"):
        if topic or uploaded_files:
            data = {}
            if topic:
                data["topic"] = topic
                data["level"] = level
                response = requests.post("http://localhost:5000/assignment/generate/topic", json=data)
            
            elif uploaded_files:
                files = []
                for file in uploaded_files:
                    files.append(("files", (file.name, file, file.type)))
                upload_response = requests.post("http://localhost:5000/upload_files", files=files)
                
                if upload_response.status_code == 200:
                    uploaded_content = upload_response.json()
                    processed_files = uploaded_content.get("files")
                    combined_content = "\n".join([file["content"] for file in processed_files])
                    data["text_content"] = combined_content
                    data["level"] = level
                response = requests.post("http://localhost:5000/assignment/generate/content", json=data)
           

            if response.status_code == 200:
                st.success("Assignment generated successfully!")
                assignment_data = response.json()
                st.write(assignment_data)
            else:
                print(response.json())
                st.error("Failed to generate assignment.")
                st.write(response.json().get("error", "Unknown error occurred."))
        else:
            st.warning("Please provide a topic or upload a file to generate an assignment.")
