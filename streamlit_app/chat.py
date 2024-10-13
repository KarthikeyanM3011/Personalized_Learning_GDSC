import streamlit as st
import requests

def show_chat():
    """Chatbot interface to interact with the chatbot."""
    st.title("Chatbot Interface")
    st.write("Ask your questions and get responses from the chatbot.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "chat_user_input" not in st.session_state:
        st.session_state.chat_user_input = ""  # Initialize if not already present

    if st.session_state.chat_history:
        for entry in st.session_state.chat_history:
            if entry["role"] == "user":
                st.markdown(f"**User:** {entry['message']}")
            elif entry["role"] == "bot":
                st.markdown(f"**Chatbot:** {entry['message']}")

    user_input = st.text_input("Your question:")
    st.session_state.chat_user_input = user_input
    def send_message_to_api(question, history):
        try:
            api_url = "http://localhost:5000/chatbot/ask"
            response = requests.post(api_url, json={"current_question": question, "history": history})
            
            if response.status_code == 200:
                st.session_state.chat_user_input = ""
                return response.json().get("response", "I couldn't process that. Please try again.")
            else:
                return "Error: Unable to get a response from the chatbot."
        except Exception as e:
            return f"Error: {e}"
        
    def format_chat_history(history):
        """Convert chat history into a list of questions and responses."""
        formatted = []
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                user_message = history[i]['message']
                bot_message = history[i + 1]['message']
                formatted.append(f'''"Question": {user_message}''')
                formatted.append(f'''"Bot Response": {bot_message}''')
        return formatted

    if st.button("Send"):
        if user_input.strip() != "":
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            history = format_chat_history(st.session_state.chat_history)
            bot_response = send_message_to_api(user_input, history)

            st.session_state.chat_history.append({"role": "bot", "message": bot_response})

            st.session_state.chat_user_input = ""
            st.rerun()
