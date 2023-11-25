import mysql.connector
from dotenv import load_dotenv
import os

def connect_to_mysql():

    load_dotenv()
    db_user = os.getenv("USERNAME")
    db_pass = os.getenv("PASSWORD")
    
    conn = mysql.connector.connect(user=db_user, passwd=db_pass,db="rpr")
    return conn