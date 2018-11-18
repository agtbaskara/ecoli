import sqlite3
import datetime
import time
import os
from threading import Thread
from sqlite3 import Error

import cherrypy
import os
 
def create_connection(db_file):
    """
    Create a database connection to the SQLite database file
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_database(conn):
    """
    Initialize database (Create Table)
    """
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
    """
    Login function, will return True if login success
    """
    cur = conn.cursor()
    data = (username,)
    cur.execute("SELECT username FROM user WHERE username= ?", data)
    if not cur.fetchone():
        print("Login Error: Username Not Exist")
        return False
    else:
        data = (username,)
        cur.execute("SELECT password FROM user WHERE username= ?", data)
        if password == str(cur.fetchone()[0]):
            print("Welcome", username)
            return True
        else:
            print("Login Error: Password Wrong")
            return False

def register_user(conn, username, password, nik):
    """
    Register user function, will return True if register success
    """
    cur = conn.cursor()
    data = (username,)
    cur.execute("SELECT username FROM user WHERE username= ?", data)
    if cur.fetchone():
        print("Register Error: Username Exist")
        return False
    else:
        data = (username,password, nik)
        conn.execute("INSERT INTO user (username, password, nik) VALUES (?,?,?)", data)
        conn.commit()
        data = (username,)
        cur.execute("SELECT username FROM user WHERE username= ?", data)
        print(cur.fetchone()[0])
        return True

def register_plug(conn, plug_id, lokasi, kapasitas):
    """
    Register plug function, will return True if register success
    """
    cur = conn.cursor()
    data = (plug_id,)
    cur.execute("SELECT plug_id FROM plug WHERE plug_id= ?", data)
    if cur.fetchone():
        print("Register Error: Plug Already Exist")
        return False
    else:
        data = (plug_id,lokasi,kapasitas)
        conn.execute("INSERT INTO plug (plug_id, lokasi, kapasitas) VALUES (?,?,?)", data)
        conn.commit()
        data = (plug_id,)
        cur.execute("SELECT plug_id FROM plug WHERE plug_id= ?", data)
        print(cur.fetchone()[0])
        return True

def isi_saldo(conn, username, saldo):
    """
    Isi saldo function, will return True if isi saldo success
    """
    data = (saldo, username)
    conn.execute("UPDATE user SET saldo = saldo + ? WHERE username = ?", data)
    conn.commit()
    return True

def get_saldo(conn, username):
    """
    Return saldo value of given username
    """
    cur = conn.cursor()
    data = (username,)
    cur.execute("SELECT saldo FROM user WHERE username = ?", data)
    return (cur.fetchone()[0])

def sewa_plug(conn, username, plug_id, durasi):
    """
    Add transaction data for plug renting
    """
    data = (datetime.datetime.now(),username, plug_id, durasi)
    conn.execute("INSERT INTO transaksi (timestamp, username, plug_id, durasi)\
                 VALUES (?,?,?,?)", data)
    conn.commit()
    return True

def check_plug(conn, plug_id):
    """
    Check the plug condition status in the database, return "ON" or "OFF"
    """
    cur = conn.cursor()
    data = (plug_id,)
    cur.execute("SELECT status_plug FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
    if not cur.fetchone():
        #print("Check Error: Transaction Not Exist")
        return("OFF")
    else:
        data = (plug_id,)
        cur.execute("SELECT timestamp, durasi FROM transaksi WHERE plug_id= ? ORDER BY trans_id DESC", data)
        fetchdata=cur.fetchone()
        timestamp = datetime.datetime.strptime((fetchdata[0]),"%Y-%m-%d %H:%M:%S.%f")
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

def plug_checker(plugid):
    """
    Function to check plug status every 1 second
    """
    database = "example.db"
    conn = create_connection(database)
    while check_plug(conn, plugid) == "ON":
        time.sleep(1)
    print("Plug", plugid, "is OFF")
    conn.close()

class server(object):
    @cherrypy.expose
    def index(self):
        return "eColi Prototype Server"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getstatus(self, plugid):

        database = "example.db"
        conn = create_connection(database)

        data = {
            "plugid" : plugid,
            "plugstatus" : check_plug(conn, plugid)
        }

        conn.close()

        return data
config = {'/':
{
    'tools.staticdir.on': True,
    'tools.staticdir.dir': os.path.abspath(".")}
}
cherrypy.tree.mount(server(), '/', config=config)
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.engine.start()

# PROGRAM START FROM HERE
database = "example.db"
conn = create_connection(database)
initialize_database(conn)

while True:
    os.system('clear')
    print("eColi CLI Prototype")
    print("1. Login")
    print("2. Register")
    print("3. Quit")
    pilihan = input("Pilih : ")
    if pilihan == "1":
        while True:
            os.system('clear')
            print("Login")
            username = input("Username : ")
            password = input("Password : ")
            success = login(conn, username, password)
            if success:
                while True:
                    os.system('clear')
                    print("eColi CLI Prototype")
                    print("Halo", username, "Saldo anda:", get_saldo(conn, username))
                    print("1. Sewa Plug")
                    print("2. Register Plug")
                    print("3. Isi Saldo")
                    print("4. Quit")
                    pilihan = input("Pilih : ")
                    if pilihan == "1":
                        while True:
                            print("Sewa Plug")
                            plugid = input("Plug ID : ")
                            durasi = input("Durasi (Menit) : ")
                            biayasewa = int(durasi)*250
                            print("Biaya Sewa:", biayasewa)
                            isi_saldo(conn, username, (-1*biayasewa))
                            input("Lanjut")
                            success = sewa_plug(conn, username, plugid, int(durasi))
                            if success:
                                #Thread(target = plug_checker, args = (plugid)).start()
                                break
                    if pilihan == "2":
                        while True:
                            print("Register Plug")
                            plugid = input("Plug ID : ")
                            lokasi = input("Lokasi : ")
                            kapasitas = input("Kapasitas (Kwh) : ")
                            success = register_plug(conn, plugid, lokasi, kapasitas)
                            if success:
                                break
                    if pilihan == "3":
                        while True:
                            print("Isi Saldo")
                            saldo = input("Saldo : ")
                            success = isi_saldo(conn, username, saldo)
                            if success:
                                break
                    if pilihan == "4":
                        quit()
                    else:
                        print("Error")
    elif pilihan == "2":
        while True:
            print("Register")
            username = input("Username : ")
            password = input("Password : ")
            nik = input("NIK : ")
            success = register_user(conn, username, password, nik)
            if success:
                break
    elif pilihan == "3":
        conn.close()
        quit()
    else:
        print("Error")

'''
register_user(conn, "admin", "admin", 123456)
register_plug(conn, 1, "UGM-1", 1000)
register_plug(conn, 2, "UGM-2", 1000)

username=login(conn, "Anjing", "pass")
print("Login", username)
isi_saldo(conn, username, 1000)

sewa_plug(conn,username,69,1)
print(check_plug(conn, 69))
while check_plug(conn, 69) == "ON":
    time.sleep(1)
print(check_plug(conn, 69))
'''
