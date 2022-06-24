#!/usr/bin/env python3
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


connection = sqlite3.connect('ATM.db')
cursor = connection.cursor()


cursor.execute("CREATE TABLE accounts(account_id integer, account_balance real, account_pin integer, account_name text, account_type text, account_number text)")


accounts = [
    (1,5669.0,1234,"John Doe","savings","4439920001"),
    (2,73000000.0,1234,"Elon Musk","current", "4439920002"),
    (3,8930203.0,1234,"Mark Zuckerberg","current","4439920003"),
    (4,63829.0,1234,"Sam Khan","savings","4439920004"),
    (5,1099.0,1234,"Sahd Guru","savings","4439920005"),
    (6,1782139238.0,1234,"Damilola Aderibigbe","current","4439920006")
]

cursor.executemany("INSERT INTO accounts VALUES (?,?,?,?,?,?)", accounts)
cursor.execute("SELECT * FROM accounts")
print(cursor.fetchall())
for row in cursor.execute("SELECT * FROM accounts"):
    print(row)

connection.commit()
connection.close()

connection = create_engine('sqlite:///ATM.db').connect()
df = pd.read_sql_table('accounts', connection, coerce_float=True)
print(df)