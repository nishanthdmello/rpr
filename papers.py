import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *
import base64

st.set_page_config(layout="wide")

conn=connect_to_mysql()
sql = conn.cursor()

if "p_id" not in st.session_state:
    st.session_state.p_id=None
if "a_id" not in st.session_state:
    st.session_state.a_id=None    

def p_click(p_id,):
    if st.session_state.p_id:
        st.session_state.p_id=None
    else:
        st.session_state.p_id = p_id
def all_click():
    st.session_state.a_id=None    
def a_click(a_id,):
    st.session_state.a_id=a_id   
    
    

# ===========================================================================================================

x, w, y = st.columns([2,0.2,2])
x.title("List of Papers")
y.title("List of Authors")
x1, x2 = x.columns(2)
y1, y2 = y.columns(2)

if not st.session_state.a_id:
    query=f"select distinct paper from written;"
    sql.execute(query)
    data=sql.fetchall()
else:
    query=f"select distinct paper from written where author='{st.session_state.a_id}';"
    sql.execute(query)
    data=sql.fetchall()
    
for i, option in enumerate(data):
    if i % 2 == 0:
        x1.button(option[0], on_click=p_click, args=(option[0],),use_container_width=True)
    else:
        x2.button(option[0], on_click=p_click, args=(option[0],),use_container_width=True)

query=f"select username from user;"
sql.execute(query)
data=sql.fetchall()

y1.button("All Papers", on_click=all_click,use_container_width=True)
for i, option in enumerate(data):
    if i % 2 == 0:
        y2.button(option[0], on_click=a_click, args=(option[0],),use_container_width=True)
    else:
        y1.button(option[0], on_click=a_click, args=(option[0],),use_container_width=True)
        
if st.session_state.p_id:
    pdf_file_path = f"pdfs/{st.session_state.p_id}"
    with open(pdf_file_path, "rb") as f:
        pdf_file = f.read()
    b64 = base64.b64encode(pdf_file).decode()
    pdf_display = f'<embed src="data:application/pdf;base64,{b64}" width="930" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

    

