import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *
import streamlit as st
import os
import base64

conn=connect_to_mysql()
sql = conn.cursor()

st.title("Main Page")

if "uname" not in st.session_state:
    st.session_state.uname=None
if "id" not in st.session_state:
    st.session_state.id=None
if "add" not in st.session_state:
    st.session_state.add = False


def butn_click(id,):
    st.session_state.add = False
    if st.session_state.id:
        st.session_state.id=None
    else:
        st.session_state.id = id
def add_click():
    st.session_state.id = None
    st.session_state.add = not st.session_state.add
    
    
# ===========================================================================================================

if st.session_state.uname:
    
    st.button("Add Papers", on_click=(add_click))
    col1, col2 = st.columns(2)

    query=f"select distinct paper from written where author = '{st.session_state.uname}';"
    sql.execute(query)
    data=sql.fetchall()

    for i, option in enumerate(data):
        if i % 2 == 0:
            col1.button(option[0], on_click=butn_click, args=(option[0],),use_container_width=True)
        else:
            col2.button(option[0], on_click=butn_click, args=(option[0],),use_container_width=True)
            
    if st.session_state.id and not st.session_state.add:
        
        pdf_file_path = f"pdfs/{st.session_state.id}"
        with open(pdf_file_path, "rb") as f:
            pdf_file = f.read()
        b64 = base64.b64encode(pdf_file).decode()
        pdf_display = f'<embed src="data:application/pdf;base64,{b64}" width="930" height="1000" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)
    
    if st.session_state.add and not st.session_state.id:
        
        uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
        sql.execute(f"select username from user where username <> '{st.session_state.uname}';")
        data = sql.fetchall()
        authors = []
        for i in data:
            authors.append(i[0])
        authors = st.multiselect("",authors, placeholder="Collaborators",)
            
        if st.button('Save PDF'):
            if uploaded_file is not None:
                directory = "pdfs"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_path = os.path.join(directory, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success('File saved.')
                query=f"insert into written (paper, author) values ('{uploaded_file.name}', '{st.session_state.uname}');"
                sql.execute(query)
                conn.commit()
                for author in authors:
                    query = f"insert into written (paper, author) values ('{uploaded_file.name}', '{author}');"
                    sql.execute(query)
                    conn.commit()
            else:
                st.error('No file uploaded.')

    
else:
    st.warning("Login First!")