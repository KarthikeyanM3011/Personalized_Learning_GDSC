import streamlit as st
from chat import show_chat
from quiz import show_quiz
from rag_chat import show_rag_chat
from assignment import show_assignment

def show_home():
    """Display the home page with sidebar navigation."""
    features = {
        "Welcome": "Welcome to the Learning Path Application!\nGDSC by Karthikeyan M",
        "Chatbot": "Interact with our intelligent chatbot.",
        "RAG Chat": "Upload documents and chat with them.",
        "Quiz Generation": "Generate quizzes based on topics or documents.",
        "Assignment Generation": "Create assignments from your input."
    }

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to:", list(features.keys()))

    # Display selected page
    if selection == "Welcome":
        st.title("Welcome to Learning Path")
        st.write(features["Welcome"])
    elif selection == "Chatbot":
        show_chat()
    elif selection == "RAG Chat":
        show_rag_chat()
    elif selection == "Quiz Generation":
        show_quiz()
    elif selection == "Assignment Generation":
        show_assignment()