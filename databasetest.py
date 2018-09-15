import sqlite3
import datetime
import time
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_database(conn):
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        username text PRIMARY KEY,
                                        password text NOT NULL,
                                        nik integer NOT NULL,
                                        saldo integer NOT NULL DEFAULT 0
                                    ); """

    sql_create_plug_table = """ CREATE TABLE IF NOT EXISTS plug (
                                        plug_id integer PRIMARY KEY,
                                        lokasi text NOT NULL,
                                        kapasitas integer NOT NULL
                                    ); """

    sql_create_transaksi_table = """CREATE TABLE IF NOT EXISTS transaksi (
                                    trans_id integer PRIMARY KEY AUTOINCREMENT,
                                    status_plug text NOT NULL DEFAULT 'ON',
                                    timestamp text NOT NULL,
                                    durasi text NOT NULL,
                                    username integer NOT NULL,
                                    plug_id integer NOT NULL,
                                    FOREIGN KEY (username) REFERENCES user (username),
                                    FOREIGN KEY (plug_id) REFERENCES plug (plug_id)
                                );"""

    create_table(conn, sql_create_user_table)
    create_table(conn, sql_create_transaksi_table)
    create_table(conn, sql_create_plug_table)

def login(conn, username, password):
    cur = conn.cursor()
    data = (username,)
    cur.execute("SELECT username FROM user WHERE username= ?", data)
    if not cur.fetchone():
        print("Login Error: Username Not Exist")
    else:
        data = (username,)
        cur.execute("SELECT password FROM user WHERE username= ?", data)
        if password == str(cur.fetchone()[0]):
            print("Welcome", username)
            return(username)
        else:
            print("Login Error: Password Wrong")

def register_user(conn, username, password, nik):
    cur = conn.cursor()
    data = (username,)
    cur.execute("SELECT username FROM user WHERE username= ?", data)
    if cur.fetchone():
        print("Register Error: Username Exist")
    else:
        data = (username,password, nik)
        conn.execute("INSERT INTO user (username, password, nik) VALUES (?,?,?)", data)
        conn.commit()
        data = (username,)
        cur.execute("SELECT username FROM user WHERE username= ?", data)
        print(cur.fetchone()[0])

def register_plug(conn, plug_id, lokasi, kapasitas):
    cur = conn.cursor()
    data = (plug_id,)
    cur.execute("SELECT plug_id FROM plug WHERE plug_id= ?", data)
    if cur.fetchone():
        print("Register Error: Plug Already Exist")
    else:
        data = (plug_id,lokasi,kapasitas)
        conn.execute("INSERT INTO plug (plug_id, lokasi, kapasitas) VALUES (?,?,?)", data)
        conn.commit()
        data = (plug_id,)
        cur.execute("SELECT plug_id FROM plug WHERE plug_id= ?", data)
        print(cur.fetchone()[0])

def isi_saldo(conn, username, saldo):
    data = (saldo, username)
    conn.execute("UPDATE user SET saldo = saldo + ? WHERE username = ?", data)
    conn.commit()

def sewa_plug(conn, username, plug_id, durasi):
    data = (datetime.datetime.now(),username, plug_id, durasi)
    conn.execute("INSERT INTO transaksi (timestamp, username, plug_id, durasi)\
                 VALUES (?,?,?,?)", data)
    conn.commit()

def check_plug(conn, plug_id):
    cur = conn.cursor()
    data = (plug_id,)
    cur.execute("SELECT status_plug FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
    if not cur.fetchone():
        print("Check Error: Transaction Not Exist")
        return("OFF")
    else:
        data = (plug_id,)
        cur.execute("SELECT timestamp, durasi FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
        fetchdata=cur.fetchone()
        timestamp = datetime.datetime.strptime((fetchdata[0]),'%Y-%d-%m %H:%M:%S.%f')
        timeon = timestamp+datetime.timedelta(minutes=int(fetchdata[1]))
        if(timeon>=datetime.datetime.now()):
            data = (plug_id,)
            cur.execute("SELECT status_plug FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
            return(cur.fetchone()[0])
        else:
            data = (plug_id,)
            conn.execute("UPDATE transaksi SET status_plug = 'OFF' WHERE plug_id = ?", data)
            conn.commit()
            cur.execute("SELECT status_plug FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
            return(cur.fetchone()[0])


if __name__ == '__main__':
    database = "example.db"
    conn = create_connection(database)

    initialize_database(conn)
    register_user(conn, "Anjing", "pass", 123456)
    register_plug(conn, 69, "UGM", 100)

    username=login(conn, "Anjing", "pass")
    print("Login", username)
    isi_saldo(conn, username, 1000)

    sewa_plug(conn,username,69,1)
    print(check_plug(conn, 69))
    while check_plug(conn, 69) == "ON":
        time.sleep(1)
    print(check_plug(conn, 69))

