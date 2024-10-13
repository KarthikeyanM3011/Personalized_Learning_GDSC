import streamlit as st
import requests

def show_chat():
    """Chatbot interface to interact with the chatbot."""
    st.title("Chatbot Interface")
    st.write("Ask your questions and get responses from the chatbot.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.chat_history:
        for entry in st.session_state.chat_history:
            if entry["role"] == "user":
                st.markdown(f"**User:** {entry['message']}")
            elif entry["role"] == "bot":
                st.markdown(f"**Chatbot:** {entry['message']}")

    user_input = st.text_input("Your question:", key="chat_user_input")

    def send_message_to_api(question, history):
        try:
            api_url = "http://localhost:5000/chatbot/ask"
            
            response = requests.post(api_url, json={"current_question": question, "history": history})
            
            if response.status_code == 200:
                return response.json().get("response", "I couldn't process that. Please try again.")
            else:
                return "Error: Unable to get a response from the chatbot."
        except Exception as e:
            return f"Error: {e}"

    if st.button("Send") or (user_input and st.session_state.get("enter_pressed", False)):
        if user_input.strip() != "":
            st.session_state.chat_history.append({"role": "user", "message": user_input})

            bot_response = send_message_to_api(user_input, st.session_state.chat_history)

            st.session_state.chat_history.append({"role": "bot", "message": bot_response})

            st.session_state["chat_user_input"] = ""

        st.session_state.enter_pressed = False

    def on_enter_key_pressed():
        st.session_state.enter_pressed = True

    st.text_input("Press Enter to Send", key="chat_user_input_enter", on_change=on_enter_key_pressed)
