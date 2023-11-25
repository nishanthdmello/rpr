import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *

conn=connect_to_mysql()
sql = conn.cursor()

st.title("SignUp Page")

if "uname" not in st.session_state:
    st.session_state.uname=None
    

def signup(username, password):
    if not username or not password:
        return 
    sql.execute(f"select password from user where username='{username}'")
    data=sql.fetchall()
    if not data:
        sql.execute(f"insert into user (username, password) values ('{username}','{password}');")
        conn.commit()
        add_vertical_space(2)
        st.success("SignUp Successfull!")


# ===========================================================================================================

if not st.session_state.uname:
    username = st.text_input("",placeholder="Username")
    password = st.text_input("",placeholder="Password", type="password")
    add_vertical_space(2)
    st.button("Done", on_click=signup, args=(username, password,))
    # if signup(username, password):
    #     st.success("SignUp Successfull!")
        
else:
    st.warning("Already logged in !")