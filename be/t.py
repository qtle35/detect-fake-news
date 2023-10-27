import mysql.connector
import pandas as pd
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()
# Kết nối đến cơ sở dữ liệu MySQL
mydatabase = mysql.connector.connect(
    host=os.getenv('DBHOST'),
    user=os.getenv('DBUSER'),
    password=os.getenv('DBPASS'),
    database=os.getenv('DBNAME')
)

mycursor = mydatabase.cursor()

# Đoạn mã SQL để tạo bảng 'mau'
# create_table_sql = """
# CREATE TABLE IF NOT EXISTS mau (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title LONGTEXT,
#     noiDung LONGTEXT,
#     theLoai LONGTEXT,
#     ngayTaoMau DATE,
#     ngaySuaMau DATE,
#     nhan_id INT,
#     isnew TINYINT(1)
# )
# """

# mycursor.execute(create_table_sql)

# Định dạng cho mẫu ngày từ ngày tháng năm
date_pattern = r'(\w+) (\d{1,2}), (\d{4})'

# Đọc dữ liệu từ tệp CSV bằng pandas
df = pd.read_csv('train.csv', encoding='utf-8')
count = 0

# ...

for index, row in df.iterrows():
    title = row['title']
    noiDung = row['text']
    theLoai = row['subject']
    date_str = row['date']
    match = re.match(date_pattern, date_str)
    count += 1
    print(match)
    try:
        month = match.group(1)
        day = int(match.group(2))
        year = int(match.group(3))

        # Convert the month name to its numerical representation
        month_mapping = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month = month_mapping.get(month, 1)

        ngayTaoMau = datetime(year, month, day).strftime("%Y-%m-%d")

        nhan_id = int(row['label'])

        # Đoạn mã SQL để chèn dữ liệu vào bảng 'mau'
        insert_sql = "INSERT INTO mau (title, noiDung, theLoai, ngayTaoMau, nhan_id) VALUES (%s, %s, %s, %s, %s)"
        values = (title, noiDung, theLoai, ngayTaoMau, nhan_id)

        mycursor.execute(insert_sql, values)
        mydatabase.commit()

    except AttributeError:
        print(f"Failed to match date for row {index}: {date_str}")

# ...

mydatabase.close()

