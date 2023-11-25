import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *

conn=connect_to_mysql()
sql = conn.cursor()

st.title("LogIn Page")

if "uname" not in st.session_state:
    st.session_state.uname=None


def login(username,password,):
    if not username or not password:
        return False
    sql.execute(f"select password from user where username='{username}';")
    data=sql.fetchone()
    if data and data[0]==password:
        st.session_state.uname=username
        return True
    return False


def logout():
    st.session_state.uname=None


# ===========================================================================================================

if not st.session_state.uname:
    sql.execute("select username from user;")
    data=sql.fetchall()
    users = [i[0] for i in data]
    username = st.selectbox("",users,index=None,placeholder="Username",)
    password = st.text_input("",placeholder="Password", type="password")
    add_vertical_space(2)
    if login(username,password):
        switch_page("main")

else:
    st.button("Log Out",on_click=(logout))