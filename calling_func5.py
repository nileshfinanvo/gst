import mysql.connector
import json
# import os
import auth_create as aucreate
import requests
from multiprocessing.pool import ThreadPool
import time

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


def update_database(id, val, col_name):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"""UPDATE gst_basic SET {col_name} = {val} WHERE gst_basic.id = '{id}' """
    # print(sql)
    try:
        mycursor.execute(sql)
        mydb.commit()
        print(val,"Table Updated")
    except:
        print('table update unsuccess')
    mydb.close()



def send_profile_detail(data_par, gstin_par):
    mydb = init_database()

    mycursor = mydb.cursor()

    ls = ['nba', 'mandatedeInvoice', 'aggreTurnOverFY', 'lgnm', 'dty', 'aggreTurnOver', 'cxdt', 'gstin', 'gtiFY',
          'cmpRt', 'rgdt', 'ctb', 'sts','tradeNam', 'isFieldVisitConducted', 'ctj', 'percentTaxInCashFY','percentTaxInCash',
          'compDetl', 'gti', 'adhrVFlag', 'ekycVFlag', 'stj', 'mbr']
    for i in ls: 
        try:
            val = data_par[i]
        except:
            data_par[i] = ''

    val1 = ( str(data_par[ls[0]]), str(data_par[ls[1]]), str(data_par[ls[2]]), str(data_par[ls[3]]), str(data_par[ls[4]]), str(data_par[ls[5]]),
           str(data_par[ls[6]]), str(data_par[ls[7]]), str(data_par[ls[8]]), str(data_par[ls[9]]), str(data_par[ls[10]]) , str(data_par[ls[11]]),
           str(data_par[ls[12]]), str(data_par[ls[13]]), str(data_par[ls[14]]), str(data_par[ls[15]]), str(data_par[ls[16]]), str(data_par[ls[17]]),
           str(data_par[ls[18]]), str(data_par[ls[19]]), str(data_par[ls[20]]), str(data_par[ls[21]]), str(data_par[ls[22]]), str(data_par[ls[23]]),str(gstin_par)[2:-3])
    val = [mycursor._connection.converter.escape(i) for i in val1]    
    sql = """INSERT IGNORE INTO gst_detail (nba, mandatedeInvoice, aggreTurnOverFY, lgnm, dty, aggreTurnOver, 
    cxdt, gstin, gtiFY, cmpRt, rgdt, ctb, sts,tradeNam, isFieldVisitConducted, ctj, percentTaxInCashFY, 
    percentTaxInCash, compDetl, gti, adhrVFlag, ekycVFlag, stj, mbr,pan) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE 
    nba='{0}',mandatedeInvoice='{1}',aggreTurnOverFY='{2}',lgnm='{3}',dty='{4}',aggreTurnOver='{5}',cxdt='{6}',gstin='{7}',gtiFY='{8}',cmpRt='{9}',rgdt='{10}',
    ctb='{11}',sts='{12}',tradeNam='{13}',isFieldVisitConducted='{14}',ctj='{15}',percentTaxInCashFY='{16}',percentTaxInCash='{17}',compDetl='{18}',gti='{19}',adhrVFlag='{20}',ekycVFlag='{21}',stj='{22}',mbr='{23}',pan='{24}' """.format(*val)
    val = ( str(data_par[ls[0]]), str(data_par[ls[1]]), str(data_par[ls[2]]), str(data_par[ls[3]]), str(data_par[ls[4]]), str(data_par[ls[5]]),
           str(data_par[ls[6]]), str(data_par[ls[7]]), str(data_par[ls[8]]), str(data_par[ls[9]]), str(data_par[ls[10]]) , str(data_par[ls[11]]),
           str(data_par[ls[12]]), str(data_par[ls[13]]), str(data_par[ls[14]]), str(data_par[ls[15]]), str(data_par[ls[16]]), str(data_par[ls[17]]),
           str(data_par[ls[18]]), str(data_par[ls[19]]), str(data_par[ls[20]]), str(data_par[ls[21]]), str(data_par[ls[22]]), str(data_par[ls[23]]),str(gstin_par)[2:-3])
    #print(val)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        # print(val)
        print("Table inserted")
        mydb.close()
    except:
        print('table unsucess',sql)


def read(num):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"SELECT id,gstid FROM gst_basic WHERE gst_basic.gst_gd = '0'  order by gstid asc LIMIT {num}" 
    # sql = f"SELECT id,gstid FROM gst_basic WHERE gst_basic.gst_gd = '0'  order by rand() LIMIT {num}"
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records


def get_data(at_par, url,gstin ,request_type = 'POST'):
    payload = "{\"gstin\":\""+str(gstin)+"\"}"
    # print(at_par,gstin)
    headers = {
      'Accept': 'application/json, text/plain',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9',
      'at': f'{at_par}',
      'Connection': 'keep-alive',
      'Content-Length': '27',
      'Content-Type': 'application/json;charset=UTF-8',
      'Host': 'publicservices.gst.gov.in',
      'Origin': 'https://services.gst.gov.in',
      'Referer': 'https://services.gst.gov.in/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
      'Cookie': f'AuthToken={at_par}; TS01b8883c=01ab915e2ca33a9749c487c5d7debe3d8832fba5ea1785ccd9635146ff4a4fafef2bd437ca1baa036ffb0e034e78d22fc4f0df8dce;'
    }

    response = requests.request(request_type, url, headers=headers, data=payload)
    # print('respo',response.text,response)
    return response.text

def check_authtoken():
    try:
        f = open('auth.txt', 'r')
        
    except Exception as e : 
        a = aucreate.create_token()
        print(e)
    return

def calling_func(d_l):
    id,gstin_par = d_l[0],d_l[1]
    # print(id,"==",gstin_par)
    print("Function Started")
    while True:
        try:
            try:
                f = open('auth.txt', 'r')
                at_val = f.readline()
                f.close()
            except:
                print('excepts')
                #aucreate.create_token()
                continue
            prof_info = get_data(at_val, 'https://publicservices.gst.gov.in/publicservices/auth/api/search/tp',gstin_par)
            
            if prof_info:
                break
            else:
                print("File remov")
                try:
                    #os.remove('auth.txt')    
                    time.sleep(10)
                except:
                    pass
                return

        except Exception as e:
            print(e)
            try:
                print('File removed')
                #os.remove('auth.txt')
                time.sleep(10)
            except:
                pass

    try:
        prof_dict = json.loads(prof_info)
        if 'errorCode' in prof_dict.keys():
            update_database(id, '100', 'gst_gd')
        else:
            send_profile_detail(prof_dict, gstin_par)
            update_database(id, '1', 'gst_gd')
    except:
        update_database(id, '100', 'gst_gd')

# calling_func((13430580,'27AMGPS9487D1ZF'))
def main_func():
    try:
               
        limit_count = 10

        count = 1000

        for index in range(0,count,1):
            rows =  read(limit_count)
            print(rows)
            if rows:
               
                try:
                    pool = ThreadPool(limit_count)
                    pool.map(calling_func, rows) # Will split the load between the threads nicely
                    pool.close()

                except Exception as e:
                    print(str(e))
                
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main_func()
