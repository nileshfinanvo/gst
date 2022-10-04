import mysql.connector
import json
import time
import os
import requests
import auth_create as aucreate
from multiprocessing.pool import ThreadPool

def check_authtoken():
    try:
        f = open('auth.txt', 'r')
        
    except Exception as e : 
        a = aucreate.create_token()
        print(e)
    return

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

def send_table_value(data1_par, gstin_par):
    mydb = init_database()
    ls = ['fy', 'taxp', 'mof', 'dof', 'rtntype', 'arn', 'status', 'gstin']

    mycursor = mydb.cursor()
    sql = """ INSERT IGNORE INTO gstin_filing_detail (fy, taxp, mof, dof, rtntype, arn, status, gstin) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)   """
    val = (str(data1_par[ls[0]]), str(data1_par[ls[1]]), str(data1_par[ls[2]]), str(data1_par[ls[3]]),
           str(data1_par[ls[3]]), str(data1_par[ls[4]]), str(data1_par[ls[5]]), gstin_par)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Table value inserted")
    mydb.close()



def update_database(id, val, col_name):
    mydb = init_database()

    mycursor = mydb.cursor()
    sql = f"""UPDATE gst_basic SET {col_name} = {val} WHERE gst_basic.id = {id} """
    # print(sql)
    mycursor.execute(sql)

    mydb.commit()
    print("Table Updated")
    mydb.close()




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
      'Cookie': f'AuthToken={at_par};TS01272ae7=01ab915e2c430e1e5871ad8ded5e12c54a9c2fae47edf5d3807bccd485ae8d3c38377f0a298931020fecb55b438cc6a03dc02d1ea90ef7b05381222dca9889218391c69177'
    }

    response = requests.request(request_type, url, headers=headers, data=payload)
    # print('respo',response.text)
    return response.text


def read(num):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"SELECT id,gstid FROM gst_basic WHERE gst_basic.gst_fd = '0' order by rand() LIMIT {num}" 
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records

def gst_fd(d_l):
    id,gstin_par = d_l[0],d_l[1]
    # print(gstin_par)
    while True:
        try:
            f = open('auth.txt', 'r')
            at_val = f.readline()
            f.close()
            filling_stat_info = get_data(at_val,'https://publicservices.gst.gov.in/publicservices/auth/api/search/taxpayerReturnDetails',gstin_par)

            filling_stat_dic = json.loads(filling_stat_info)
            # print(filling_stat_dic)
            break

        except:
            try:
                print('File removed')
                #os.remove('auth.txt')
                # time.sleep(10)
                #aucreate.create_authtoken()
            except:
                pass
            

    try:
        filling_stat_dict = json.loads(filling_stat_info)
        keys_ls = list(filling_stat_dict.keys())
        for x in range(len(filling_stat_dict) - 1):
            dic_ls = filling_stat_dict[keys_ls[x]][0]

        for val in dic_ls:
            send_table_value(val, gstin_par)
        # return filling_stat_dict
        update_database(id, '1', 'gst_fd')

    except:
        update_database(id, '100', 'gst_fd')


def main_func():
    try:
               
        limit_count = 15

        count = 1000

        for index in range(0,count,1):
            rows =  read(limit_count)
            print(rows)
            if rows:
               
                try:
                    pool = ThreadPool(limit_count)
                    pool.map(gst_fd, rows) # Will split the load between the threads nicely
                    pool.close()

                except Exception as e:
                    print(str(e))
                
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        try:
            
            main_func()
        except:
            pass

# calling_func('19AAFCP6696M2ZF')
