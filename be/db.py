import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
# from os.path import join, dirname

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
load_dotenv()
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASS'),
            database=os.getenv('DBNAME')
        )
        if connection.is_connected():
            print('Kết nối thành công')
            return connection
        else:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return None
    except Error as e:
        print(str(e))
        return None

def close_db_connection(connection):
    if connection:
        connection.close()
