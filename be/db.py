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
            cursor = connection.cursor()
            try:
                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS model(
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        date TEXT NOT NULL,
                        acc DOUBLE NOT NULL,
                        pre DOUBLE NOT NULL,
                        re DOUBLE NOT NULL,
                        f1 DOUBLE NOT NULL
                    );''')
                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS label(
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        description TEXT
                    );''')
                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS sample(
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        text VARCHAR(255) NOT NULL,
                        label_id INTEGER,
                        FOREIGN KEY (label_id) REFERENCES label(id) ON DELETE SET NULL
                    );''')
                cursor.execute(    
                    '''CREATE TABLE IF NOT EXISTS mau (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        itle LONGTEXT,
                        noiDung LONGTEXT,
                        theLoai LONGTEXT,
                        ngayTaoMau DATE,
                        ngaySuaMau DATE,
                        nhan_id INT,
                        isnew TINYINT(1)
                        FOREIGN KEY (nhan_id) REFERENCES label(id) ON DELETE SET NULL
                            );''')
                cursor.close()
            except Exception as e:
                print('Create error')
            finally:
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