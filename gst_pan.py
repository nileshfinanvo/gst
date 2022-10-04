import mysql.connector
import json,os
import time
import requests
# import auth_create as aucreate
from multiprocessing.pool import ThreadPool
import time

def get_data(at_par, url, pan):
    payload = "{\"panNO\":\""+str(pan)+"\"}"
    headers = {
      'Host': 'publicservices.gst.gov.in',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
      'Accept': 'application/json, text/plain',
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept-Encoding': 'gzip, deflate, br',
      'Content-Type': 'application/json;charset=UTF-8',
      'at': f'{at_par}',
      'Content-Length': '27',
      'Origin': 'https://services.gst.gov.in',
      'Connection': 'keep-alive',
      'Referer': 'https://services.gst.gov.in',
      'Cookie': f'AuthToken={at_par};TS01272ae7=019116acc025b06305a5a95d3163fca9d54ffc1ff28695d11f8caadfd0bb34bbf489ea41cee6ed845e4e0028b1260b3015442eb4236dcf2309b877b94845280e01309aea97'
    }

    response = requests.request('POST', url, headers=headers, data=payload)
    #print('rrrrr',response.text)
    return response.text

def init_database():
    while True:
        try:
            mydb = mysql.connector.connect(host="161.97.177.80",user="bipin_gstin",password="Gstin@123",database="gstin_bipin")
            break
        except:
            continue

    return mydb

state_code = {"35":"Andaman and Nicobar Islands" ,"37":"Andhra Pradesh", "12":"Arunachal Pradesh","18":"Assam","10":"Bihar",
              "04":"Chandigarh","22":"Chhattisgarh","26":"Dadra and Nagar Haveli and Daman and Diu","25":"Daman and Diu","07":"Delhi",
              "30":"Goa", "24":"Gujarat","06":"Haryana","02":"Himachal Pradesh" ,"01":"Jammu and Kashmir",
            "20":"Jharkhand","29":"Karnataka","32":"Kerala","38":"Ladakh","31":"Lakshadweep","23":"Madhya Pradesh", "27":"Maharashtra",
            "14":"Manipur", "17":"Meghalaya","15":"Mizoram","13":"Nagaland","21":"Odisha","97":"Other Territory","34":"Puducherry",
              "03":"Punjab","08":"Rajasthan","11":"Sikkim","33":"Tamil Nadu","36":"Telangana","16":"Tripura","09":"Uttar Pradesh",
              "05":"Uttarakhand" ,"19":"West Bengal"}

def read(num):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f"SELECT id,gstid,priority FROM gst_basic WHERE gst_basic.gst_pan = '0' order by rand() LIMIT {num}" 
    mycursor.execute(sql)
    records = mycursor.fetchall()
    return records


def send_val (gstin_par, status_par, state_par,priority):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql = f""" INSERT IGNORE INTO gst_basic ( gstid, state, status,priority,gst_pan) VALUE (%s, %s, %s,%s,'1') 
            ON DUPLICATE KEY UPDATE gstid = '{gstin_par}', state = '{state_par}', status = '{status_par}',priority = '{priority}',gst_pan = '1' """
    val = (str(gstin_par), str(state_par), str(status_par),str(priority))

    mycursor.execute(sql, val)
    mydb.commit()
    print("Value Inserted")
    mydb.close()


def update_database(id, val):
    mydb = init_database()
    mycursor = mydb.cursor()
    sql2 = f"""UPDATE gst_basic SET gst_pan = {val} where id  = {id} """

    mycursor.execute(sql2)
    mydb.commit()
    print("Table Updated")
    mydb.close()


def gst_pan(d_l):
    id,gstin,priority = d_l[0],d_l[1],d_l[2]
    pan = gstin[2:-3]
    f = open('auth.txt', 'r')
    at_val = f.readline()
    f.close()
    while True:
        try:
            f = open('auth.txt', 'r')
            at_val = f.readline()
            f.close()
            time.sleep(3)
            res = get_data(at_val, 'https://services.gst.gov.in/services/auth/api/get/gstndtls',
                                   pan)
            res_dict = json.loads(res)
            # print(res_dict)
            break
        except:
            try:
                print('File removed')
                os.remove('auth.txt')
                time.sleep(10)
            except:
                pass
            

    try:
        for x in res_dict['gstinResList']:
            code = x['stateCd']
            send_val(x['gstin'], x['authStatus'], state_code[code],priority)
        update_database(id,'1')    
    except:
        update_database(id,'100')    
        pass
# calling_func('19AAFCP6696M2ZF')



def main_func():
    try:
               
        limit_count = 15

        count = 1000

        for index in range(0,count,1):
            rows =  read(limit_count)
            thd = len(rows)
            print(rows)
            if rows:
               
                try:
                    pool = ThreadPool(thd)
                    pool.map(gst_pan, rows) # Will split the load between the threads nicely
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
