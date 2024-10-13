import streamlit as st
import requests

def show_assignment():
    """Assignment Generation interface."""
    st.title("Generate an Assignment")
    
    topic = st.text_input("Enter a topic for the assignment:")
    uploaded_file = st.file_uploader("Or upload a file", type=['pdf', 'pptx', 'docx'])

    if st.button("Generate Assignment"):
        if topic or uploaded_file:
            data = {}
            if topic:
                data["topic"] = topic
            if uploaded_file:
                data["file"] = uploaded_file.getvalue()  # Handle the file appropriately
            
            response = requests.post("http://localhost:5000/generate_assignment", json=data)
            if response.status_code == 200:
                st.success("Assignment generated successfully!")
                assignment_data = response.json()
                st.write(assignment_data)
                # Store assignment details in the database
            else:
                st.error("Failed to generate assignment.")
        else:
            st.warning("Please provide a topic or upload a file.")
