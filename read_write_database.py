from time import sleep
import mysql.connector

def connect():

    host = "161.97.177.80"
    port = 3306
    username = "bipin_gstin"
    password = "Gstin@123"
    database = "gstin_bipin"
    while True:
        try:
            db = mysql.connector.connect(host=host, port=port, user=username, passwd=password, db=database)
            break
        except:
            sleep(5)
            pass
    return db

