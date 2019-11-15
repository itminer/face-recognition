# -*- coding: utf-8 -*-
import os
import datetime
import mysql.connector as msc
from mysql.connector import Error

db_host = "localhost"
db_user = "root"
db_passwd = "root"

db_name = "company"
tb_name = "employees"
 

def connect():
    """ Connect to MySQL database """
    conn = msc.connect(host=db_host, user=db_user, passwd=db_passwd, db = db_name)
    if(conn):
        curs = conn.cursor()
        curs.execute("SELECT VERSION()")
        version = curs.fetchone()
        print("Database Connected\nDatabase Version : %s" % version)
        conn.close()
        return True
    else:
        return False

def getinfo():
    result = []
    conn = msc.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_name)
    curs = conn.cursor()
    curs.execute("SELECT * FROM " + tb_name)
    for row in curs.fetchall():
        result.append(row)
    conn.commit()
    conn.close()
    return result

def insert(name):
    conn = msc.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_name)
    curs = conn.cursor()
    value = [(name, datetime.datetime.now())]
    try:
        curs.execute("INSERT INTO employees(name, time) Values (%s, now())", (name,))
        conn.commit()
        print("Success")
    except Error:
        conn.rollback()
        print("Failed")
    conn.close()

def getUserByName(name):
    result = []
    conn = msc.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_name)
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM "+tb_name+" WHERE name=%s", (name, ))
        for row in curs.fetchall():
            result.append(row)
        conn.commit()
        print("Success")
    except Error:
        conn.rollback()
        print("Failed")
    conn.close()
    return result

# if __name__ == "__main__":
#     getUserByName('tet')


