import mysql.connector
import auth_create as aucreate
import json
import os
import requests
from multiprocessing.pool import ThreadPool
import time
def init_database():
    mydb = mysql.connector.connect(
        host="161.97.177.80",
        user="bipin_gstin",
        password="Gstin@123",
        database="gstin_bipin"
    )

    return mydb

def update_database(id, val, col_name):
    mydb = init_database()

    mycursor = mydb.cursor()
    sql = f"""UPDATE gst_basic SET {col_name} = {val} WHERE gst_basic.id = {id} """
    # print(sql)
    try:
        mycursor.execute(sql)

        mydb.commit()
        print(f" {val} Table Updated")
    except:
        print('table update unsuccess')
    mydb.close()


def send_buisness_val(data1_par, gstin_par):
    mydb = init_database()
    ls = ['adr', 'em', 'mb', 'addr', 'lastUpdatedDate', 'ntr', 'gstin']

    mycursor = mydb.cursor()
    sql = """ INSERT IGNORE INTO gst_business_detail ( adr, em, mb, addr, lastUpdatedDate,
                ntr, gstin) VALUES (%s,%s,%s,%s,%s,%s,%s)  """
    val = (str(data1_par[ls[0]]), str(data1_par[ls[1]]), str(data1_par[ls[2]]), str(data1_par[ls[3]]),
           str(data1_par[ls[4]]), str(data1_par[ls[5]]), gstin_par)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Business Table inserted")
    mydb.close()


def get_data(at_par, url,gstin):
    payload = "{\"gstin\":\"%s\"}" % gstin
    # print(payload)
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Cookie': f'AuthToken={at_par}; '#'TS01272ae7=01ab915e2c77f62dbb3f68d44e9ad40659860803d8916574d23721206ac931caeeaa49a3a17b6b011cd8aff86974570520383f5a21'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print('respo',response.text)
    return response.text



def read(num):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"SELECT id,gstid FROM gst_basic WHERE gst_basic.gst_bd = '0'  order by rand() LIMIT {num}" 
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records



def gst_bd(d_l):
    id,gstin_par = d_l[0],d_l[1]
    while True:
        try:
            try:
                f = open('auth.txt', 'r')
                at_val = f.readline()
                f.close()
            except:
                # print('excepts')
                # aucreate.create_token()
                continue

            buisness_info = get_data(at_val,"https://publicservices.gst.gov.in/publicservices/auth/api/search/tp/busplaces",gstin_par)
            # buis_dict = json.loads(buisness_info)
            if len(buisness_info) > 0:
                # print("aaa",buisness_info)
                try:
                    buis_dict = json.loads(buisness_info)
                except Exception as e:
                    print(e)
                    f = open("Error.txt", 'a')
                    f.write(buisness_info+"\n")
                    f.close()
                    update_database(id, '100', 'gst_bd')
                    return 
                break
            else:
                try:
                    print('File removed')
                    #os.remove('auth.txt')
                    time.sleep(10)
                except:
                    pass

        except Exception as e:
            print(e)
            try:
                print('File removed')
                # os.remove('auth.txt')
            except:
                pass
                # aucreate.create_token()

    try:
        buisness_info = buisness_info.replace('"NA"J', "J")
        buis_dict = json.loads(buisness_info.replace('"NA"J', "J"))
        keys_ls = list(buis_dict.keys())
        try:
            prad = buis_dict['pradr']
        except:
            print('blank  data...')
            update_database(id, '2', 'gst_bd')
            return
        for x in range(len(buis_dict) - 1):
            # print("x",x)
            if len(buis_dict[keys_ls[x]]) == 0:
                break
            try:
                send_buisness_val(buis_dict[keys_ls[x]], gstin_par)
            except:
                dic = buis_dict[keys_ls[x]][0]
                send_buisness_val(dic, gstin_par)
            update_database(id, '1', 'gst_bd')
    except:
        update_database(id, '100', 'gst_bd')

# gst_bd(('1','03AARFS1372G1Z6'))    
def main_func():
    try:
               
        limit_count = 20
        count = 100

        for index in range(0,count,1):
            rows =  read(limit_count)
            print(rows)
            if rows:

                try:
                    pool = ThreadPool(limit_count)
                    pool.map(gst_bd, rows) # Will split the load between the threads nicely
                    pool.close()
                except Exception as e:
                    print(str(e))
                
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        
        main_func()
        
