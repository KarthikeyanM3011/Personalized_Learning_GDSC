import streamlit as st

def show_home():
    """Display the home page with feature cards."""
    st.title("Available Features")
    
    st.write("Select a feature to get started:")

    features = {
        "Chatbot": "Interact with our intelligent chatbot.",
        "RAG Chat": "Upload documents and chat with them.",
        "Quiz Generation": "Generate quizzes based on topics or documents.",
        "Assignment Generation": "Create assignments from your input."
    }

    for feature in features.keys():
        if st.button(feature):
            if feature == "Chatbot":
                st.session_state.page = "Chat"
                show_chat()
            elif feature == "RAG Chat":
                st.session_state.page = "RAG Chat"
                show_rag_chat()
            elif feature == "Quiz Generation":
                st.session_state.page = "Quiz Generation"
                show_quiz()
            elif feature == "Assignment Generation":
                st.session_state.page = "Assignment Generation"
                show_assignment()

def show_chat():
    """Redirect to Chat page."""
    import chat
    chat.show_chat()

def show_rag_chat():
    """Redirect to RAG Chat page."""
    import rag_chat
    rag_chat.show_rag_chat()

def show_quiz():
    """Redirect to Quiz Generation page."""
    import quiz
    quiz.show_quiz()

def show_assignment():
    """Redirect to Assignment Generation page."""
    import assignment
    assignment.show_assignment()