import streamlit as st
import requests
from home import show_home

def show_login_signup():
    """Show Login/Signup interface."""
    st.title("Welcome to Learning Path API")
    
    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Signup":
        with st.form("signup_form"):
            st.header("Create an Account")
            user_email = st.text_input("Email", max_chars=50)
            password = st.text_input("Password", type='password', max_chars=30)
            name = st.text_input("Name", max_chars=30)
            signup_button = st.form_submit_button("Signup")

            if signup_button:
                # Implement signup API call
                response = requests.post("http://localhost:5000/user", json={"user_email": user_email, "password": password, "name": name})
                if response.status_code == 201:  # Check for successful creation
                    st.success("Signup successful! Please log in.")
                else:
                    st.error(f"Signup failed: {response.json().get('message', 'Please try again.')}")

    elif choice == "Login":
        with st.form("login_form"):
            st.header("Login to Your Account")
            user_email = st.text_input("Email", max_chars=50)
            password = st.text_input("Password", type='password', max_chars=30)
            login_button = st.form_submit_button("Login")

            if login_button:
                # Implement login API call
                response = requests.get(f"http://localhost:5000/user/{user_email}/{password}")
                if response.status_code == 200:
                    st.session_state.logged_in = True  # Set user session
                    st.session_state.user_email = user_email  # Store user email in session
                    st.success("Login successful!")
                    st.session_state.choice = "Home"
                    st.rerun()  
                else:
                    st.error("Login failed. Please check your credentials.")
