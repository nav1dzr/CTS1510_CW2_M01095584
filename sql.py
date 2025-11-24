
import sqlite3
import pandas as pd
conn = sqlite3.connect('DATA/telligence_platform.db')


def add_user(conn,name,hash):
    curr = conn.cursor()
    sql = ("""INSERT INTO users (username, password_hash) VALUES (?, ?) """)
    param = (name,hash) 
    curr.execute(sql,param)
    conn.commit()


def get_user():
    curr = conn.cursor()
    sql = ("""SELECT * FROM users""")
    curr.execute(sql)
    users = curr.fetchall()
    return users

def migrate_user_data(conn):
    with open("DATA/users.txt", "r") as f:
        users = f.readlines()
    for user in users:
       name, hash = user.strip().split(",")
       add_user(conn,name,hash)
    conn.close()

def migrate_cyber_data(conn):
    cyber_data = pd .read_csv(r'C:\Users\navid\CTS1510_M01095584_CW2\DATA\cyber_incidents.csv')
    cyber_data.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    conn.close()


def get_cyber_data(conn):
    sql = ("select * from cyber_incidents")
    cyber_df = pd.read_sql_query(sql, conn)
    return cyber_df


def get_user_by_name(conn, name):
    curr = conn.cursor()
    sql =  "SELECT * FROM users WHERE username = ? "
    param = (name,)
    curr.execute(sql,param)
    user = curr.fetchone()
    return user

migrate_user_data(conn)
conn.close()