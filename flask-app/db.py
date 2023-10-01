# db.py

import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="flask_data"
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
