import sqlite3
import datetime
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
                                        user_id integer PRIMARY KEY AUTOINCREMENT,
                                        nama text NOT NULL,
                                        saldo integer NOT NULL
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
                                    user_id integer NOT NULL,
                                    plug_id integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES user (user_id),
                                    FOREIGN KEY (plug_id) REFERENCES plug (plug_id)
                                );"""

    create_table(conn, sql_create_user_table)
    create_table(conn, sql_create_transaksi_table)
    create_table(conn, sql_create_plug_table)

def login(conn, nama):
    cur = conn.cursor()
    data = (nama,)
    cur.execute("SELECT nama FROM user WHERE nama= ?", data)
    if not cur.fetchone():
        print("Login Error: Username Not Exist")
    else:
        cur.execute("SELECT user_id FROM user WHERE nama= ?", data)
        print("Welcome", nama)
        return(int(cur.fetchone()[0]))

def register_user(conn, nama):
    cur = conn.cursor()
    data = (nama,)
    cur.execute("SELECT nama FROM user WHERE nama= ?", data)
    if cur.fetchone():
        print("Register Error: Username Exist")
    else:
        data = (nama,0)
        conn.execute("INSERT INTO user (nama, saldo) VALUES (?,?)", data)
        conn.commit()
        data = (nama,)
        cur.execute("SELECT user_id FROM user WHERE nama= ?", data)
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

def isi_saldo(conn, user_id, saldo):
    data = (saldo, user_id)
    conn.execute("UPDATE user SET saldo = saldo + ? WHERE user_id = ?", data)
    conn.commit()

def sewa_plug(conn, user_id, plug_id, durasi):
    data = (datetime.datetime.now(),user_id, plug_id, durasi)
    conn.execute("INSERT INTO transaksi (timestamp, user_id, plug_id, durasi)\
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
    register_user(conn, "Anjing")
    register_plug(conn, 69, "UGM", 100)

    user_id=login(conn, "Anjing")
    print("Login",user_id)
    isi_saldo(conn, user_id, 1000)

    sewa_plug(conn,user_id,69,1)
    print(check_plug(conn, 69))

