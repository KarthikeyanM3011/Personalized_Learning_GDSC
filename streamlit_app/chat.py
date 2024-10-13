import streamlit as st
import requests

def show_chat():
    """Chat interface for chatbot."""
    st.title("Chat with the Bot")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("Your message:", "")
    
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append({"user": user_input})
            response = requests.post("http://localhost:5000/chatbot/ask", json={"current_question": user_input, "history": st.session_state.chat_history})
            answer = response.json().get('response', "Sorry, I couldn't process your request.")
            st.session_state.chat_history.append({"bot": answer})
            st.success("Bot: " + answer)
    
    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.markdown(f"You: {chat['user']}")
        if "bot" in chat:
            st.markdown(f"Bot: {chat['bot']}")
