import streamlit as st

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "viewer": {"password": "view123", "role": "Viewer"},
}

def login_form():
    st.title("Login")
    st.markdown("Please log in to access the dashboard.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.success(f"Welcome, {username}! Role: {user['role']}")
            st.rerun()
        else:
            st.error("Invalid username or password.")

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.rerun()

def require_login():
    if not st.session_state.get("logged_in"):
        login_form()
        st.stop()

def require_admin():
    require_login()
    if st.session_state.get("role") != "Admin":
        st.error("Access denied. Admin role required.")
        st.stop()

def is_admin():
    return st.session_state.get("role") == "Admin"

def show_user_info():
    if st.session_state.get("logged_in"):
        role = st.session_state.get("role", "")
        username = st.session_state.get("username", "")
        st.sidebar.markdown(f"**User:** {username}  \n**Role:** {role}")
        if st.sidebar.button("Logout"):
            logout()
