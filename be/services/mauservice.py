import pandas as pd
import mysql.connector
from mysql.connector import Error
from flask import jsonify
from db import create_db_connection, close_db_connection
import os

def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(str(e))
        return None
    
def getMaus():
    
    conn = create_db_connection()
    if conn:
        cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT mau.id, mau.title, mau.noiDung, mau.theLoai, mau.ngayTaoMau, mau.ngaySuaMau,
                mau.nhan_id, label.name
            FROM mau
            LEFT JOIN label ON mau.nhan_id = label.id
        ''')
        result = cursor.fetchall()
        mau_list = [
            {
                'id': row[0],
                'title': row[1],
                'noiDung': row[2],
                'theLoai': row[3],
                'ngayTaoMau': row[4],
                'ngaySuaMau': row[5],
                'idNhan': row[6],
                'nhan_name': row[7]
            }
            for row in result
        ]
        return mau_list
    except Exception as e:
        print(str(e))
        return []
    

def getMau(mau_id):
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT mau.id, mau.title, mau.noiDung, mau.theLoai, mau.ngayTaoMau, mau.ngaySuaMau,
                    mau.nhan_id, label.name
                FROM mau
                LEFT JOIN label ON mau.nhan_id = label.id
                WHERE mau.id = %s
            ''', (mau_id,))
            result = cursor.fetchone()
            if result:
                mau_info = {
                    'id': result[0],
                    'title': result[1],
                    'noiDung': result[2],
                    'theLoai': result[3],
                    'ngayTaoMau': result[4],
                    'ngaySuaMau': result[5],
                    'idNhan': result[6],
                    'nhan_name': result[7]
                }
                return mau_info
        return None
    except Exception as e:
        print(str(e))
        return None
    finally:
        close_db_connection(connection)


import csv

def saveMau(title, noiDung, theLoai, nhan_id, ngayTaoMau, ngaySuaMau):
    connection = create_db_connection()
    if connection:
        cursor = execute_query(
            connection,
            '''INSERT INTO mau (title, noiDung, theLoai, nhan_id, ngayTaoMau, ngaySuaMau, isnew) VALUES (%s, %s, %s, %s, %s, %s, 1)''',
            (title, noiDung, theLoai, nhan_id, ngayTaoMau, ngaySuaMau)
        )
        close_db_connection(connection)
        
        # # Lưu dữ liệu vào tệp CSV
        # with open('train.csv', 'a', newline='') as csvfile:
        #     csv_writer = csv.writer(csvfile)
        #     csv_writer.writerow([title, noiDung, theLoai, ngayTaoMau, nhan_id])

def updateMau(mau_id, title, noiDung, theLoai, nhan_id, ngaySuaMau):
    try:
        connection = create_db_connection()
        if connection:
            cursor = execute_query(
                connection,
                '''UPDATE mau
                   SET title = %s, noiDung = %s, theLoai = %s, nhan_id = %s, ngaySuaMau = %s
                   WHERE id = %s''',
                (title, noiDung, theLoai, nhan_id, ngaySuaMau, mau_id)
            )
            close_db_connection(connection)
        else:
            print("Không thể kết nối đến cơ sở dữ liệu.")
    except Exception as e:
        print(str(e))


def deleteMau(mau_id):
    try:
        connection = create_db_connection()
        if connection:
            cursor = execute_query(
                connection,
                '''DELETE FROM mau WHERE id = %s''',
                (mau_id,)
            )
            close_db_connection(connection)
    except Exception as e:
        print(str(e))

