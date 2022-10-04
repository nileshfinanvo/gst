import mysql.connector

def init_database():
        
    while True:
        try:
            mydb = mysql.connector.connect(
                host="161.97.177.80",
                user="bipin_gstin",
                password="Gstin@123",
                database="gstin_bipin"
            )
            break
        except:
            pass


    return mydb


def read(num):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = num
    mycursor.execute(sql)
    records = mycursor.fetchone()

    return records

    
if __name__ =="__main__":
    # print(' aggreTurnOverFY 2020-2021 =',read("SELECT COUNT(*) FROM `gst_detail` WHERE aggreTurnOverFY = '2020-2021'")[0])
    # print(' GST Counts =',read("SELECT COUNT(*) FROM `gst_basic`")[0])
    # print(' DISTINCT pan =',read("SELECT DISTINCT(pan),COUNT(*) FROM `gst_detail` group by pan")[1])
    # print(' pan is null =',read("SELECT COUNT(*) FROM `gst_detail` WHERE pan is null OR pan = '' ")[0])

    print(' aggreTurnOverFY 2020-2021 =',read("SELECT COUNT(*) FROM `gst_detail` WHERE aggreTurnOverFY = '2020-2021'")[0])
    print(' GST Counts =',read("SELECT COUNT(*) FROM `gst_basic`")[0])
    print(' DISTINCT pan =',read("SELECT count(DISTINCT(pan)) FROM `gst_detail`"))
    print(' pan is null =',read("SELECT COUNT(*) FROM `gst_detail` WHERE pan is null OR pan = '' ")[0])