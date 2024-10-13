import streamlit as st
from auth import show_login_signup
from home import show_home

def main():
    st.set_page_config(page_title="Learning Path API", layout="wide")

    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        show_login_signup()
    else:
        show_home()

if __name__ == "__main__":
    main()