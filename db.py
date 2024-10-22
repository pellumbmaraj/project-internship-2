import sqlite3

from sqlalchemy import DATE, sql

conn = sqlite3.connect("data.db")

cursor = conn.cursor()

import pandas as pd
from datetime import datetime
import random
import string

def generate_random_string(length):
    # Define the characters you want to use (letters and digits in this case)
    characters = string.ascii_letters + string.digits  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    # Use random.choices to generate a list of random characters and join them into a string
    random_string = ''.join(random.choices(characters, k=length))
    
    return random_string

# df = pd.read_excel("regression.xlsx")

# for index, row in df.iterrows():
#     sql = """INSERT INTO Regression (name, dependant, wives, projects) VALUES (?, ?, ?, ?);"""

#     # if isinstance(row[1], pd.Timestamp):
#     #     datetime_obj = row[1].to_pydatetime()
#     # datetime = row['Date'].strftime('%m-%d-%Y %H:%M:%S')

#     # print(row)

#     cursor.execute(sql, (row['Name'], row['Dependant'], row['Wives'], row['Projects']))



import csv

with open("sales.csv", mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)

    for row in csv_reader:
        sql = '''INSERT INTO Sales VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        

        cursor.execute(sql, (generate_random_string(30), datetime.strptime(row[0], '%Y-%m-%d').date(), row[1], row[2], 
                             row[3], row[4], int(float(row[5])), float(row[6]), float(row[7])))


conn.commit()
conn.close()


