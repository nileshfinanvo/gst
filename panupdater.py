import mysql.connector

def init_database():
    while True:
        try:
            mydb = mysql.connector.connect(
                host="161.97.177.80",
                user="bipin_gstin",
                password="Gstin@123",
                database="gstin_bipin")
            break
        except:
            pass

    return mydb


def update_database():
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"""update gst_detail set pan = substring(gstin,3,10) WHERE pan ="" OR pan is null LIMIT 10000 """
    try:
        mycursor.execute(sql)
        mydb.commit()
        print("Table Updated")
    except:
        print('table update unsuccess')
    mydb.close()

if __name__ =="__main__":
    while True:
        update_database()