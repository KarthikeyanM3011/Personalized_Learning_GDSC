import streamlit as st
from chat import show_chat
from quiz import show_quiz
from rag_chat import show_rag_chat
from assignment import show_assignment

def show_home():
    """Display the home page with feature cards."""
    st.title("Available Features")
    st.write("Select a feature to get started:")

    features = {
        "Chatbot": "Interact with our intelligent chatbot.",
        "RAG Chat": "Upload documents and chat with them.",
        "Quiz Generation": "Generate quizzes based on topics or documents.",
        "Assignment Generation": "Create assignments from your input.",
        "Feature 5": "Description of Feature 5"
    }

    feature_keys = list(features.keys())

    for i in range(0, len(feature_keys), 3):
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            if i + idx < len(feature_keys):
                feature = feature_keys[i + idx]
                
                with col:
                    st.markdown(
                        f"""
                        <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); text-align: center;'>
                            <h3>{feature}</h3>
                            <p>{features[feature]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(f"Go to {feature}", key=f"btn_{feature}"):
                        st.session_state.page = feature
                        st.experimental_rerun()

if "page" in st.session_state:
    if st.session_state.page == "Chatbot":
        show_chat()
    elif st.session_state.page == "RAG Chat":
        show_rag_chat()
    elif st.session_state.page == "Quiz Generation":
        show_quiz()
    elif st.session_state.page == "Assignment Generation":
        show_assignment()
    else:
        show_home()
else:
    show_home()
