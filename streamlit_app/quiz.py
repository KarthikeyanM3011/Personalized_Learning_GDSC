import streamlit as st
import requests

def show_quiz():
    """Quiz Generation interface."""
    st.title("Generate a Quiz")
    
    topic = st.text_input("Enter a topic for the quiz:")
    uploaded_file = st.file_uploader("Or upload a file", type=['pdf', 'pptx', 'docx'])

    if st.button("Generate Quiz"):
        if topic or uploaded_file:
            data = {}
            if topic:
                data["topic"] = topic
            if uploaded_file:
                data["file"] = uploaded_file.getvalue()  # Assuming you handle the file appropriately
            
            response = requests.post("http://localhost:5000/generate_quiz", json=data)
            if response.status_code == 200:
                st.success("Quiz generated successfully!")
                quiz_data = response.json()
                st.write(quiz_data)
                # Store quiz details in the database
            else:
                st.error("Failed to generate quiz.")
        else:
            st.warning("Please provide a topic or upload a file.")
