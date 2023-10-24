from flask import jsonify
from db import create_db_connection, close_db_connection

def getLabels():
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM label")
            labels = cursor.fetchall()
            labels_list = [{"id": row[0], "name": row[1]} for row in labels]
            close_db_connection(conn)
            return labels_list
        except Exception as e:
            print(str(e))
            close_db_connection(conn)
            return []
    return []
