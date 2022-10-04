import time
import os
import mysql.connector
from datetime import datetime
from pytz import timezone
import requests
from azcaptchaapi import AZCaptchaApi
import read_write_database as db
s = requests.session()

def updatestattus(status,username):
    cursor = mysql.connector.connect(
        # host="185.214.126.3",
        # user="u653283300_gst",
        # password="Gst@1234",
        # database="u653283300_gst"
        host="161.97.177.80",
        user="bipin_gstin",
        password="Gstin@123",
        database="gstin_bipin_cred"
    )
   
    #cursor = db.connect()
    cur = cursor.cursor()

    update_qu = f"update acli set `status` ='{status}'  where `User_Name` = '{username}'"
    try:
        cur.execute(update_qu)
        cursor.commit()
        print(f"update {status} success")
    except Exception as e:
        print(e)
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
        'Cookie': f'AuthToken={at_par}; TS01272ae7=01ab915e2c77f62dbb3f68d44e9ad40659860803d8916574d23721206ac931caeeaa49a3a17b6b011cd8aff86974570520383f5a21'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print('respo',response.text)
    return response.text

def check_login(gstin_par):
    try:
        f = open('auth.txt', 'r')
        at_val = f.readline()
        f.close()
    except:
        # print('excepts')
        # aucreate.create_token()
        pass
    buisness_info = get_data(at_val,"https://publicservices.gst.gov.in/publicservices/auth/api/search/tp/busplaces",gstin_par)
    # buis_dict = json.loads(buisness_info)
    if len(buisness_info) > 0:
        print('logedin')
        # time.sleep(120)        
    else:
        try:
            print('File removed')
            os.remove('auth.txt')
        except:
            pass

def create_authtoken(username,password):
    for n in range(1,3,1):
        url = "https://services.gst.gov.in/services/captcha?rnd=0.14743381001825684"

        payload={}
        headers = {
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'TS01b8883c=01ab915e2cfb5747215d12773b23488248d7f324f031182e825574ba8bdda693c18daf648b03350b726caa8dc4d8901272a4508f8b; ak_bmsc=C805E422BAC88ECA00C6C6372CD4A85A~000000000000000000000000000000~YAAQBcAsMb7Fw+eAAQAAYZGbAA8/MSkl1a/4yTZk10qFBmEnLVLMmrv6X0XXqGzo9JfIp+2QtIezSk8wKVFYEPQPkCGRVUFRyE7qQqhwCTPT36Dz+v8hqz90u31dFCD+8Q9mCFLaow5i7Xg9gJKfyQpwKp8Yvp5TQJ/oQC6HXKk6Pe2iMYhX8jFJaOyFgupgWEZWNZQpcYg+AgmKiz+sDlGHw2X1RIYACb8z1u3SJUpaEy/kY92lo2sH+qq6NzbshRPrnUdqb/URcPeVMPCbdRn86fd5Gm/Xn0BdSwceVc6Zm9bfg4Oo/UeHoj5tq8SerSJFI8AY/klFvdxpS8VyHwRalreXXYLBIHfdCyJcxskpTNK5pWCNpBXsYH8lbuyd; bm_sv=01478F59B48EA5443DDD8EA2D24C4103~YAAQBcAsMcrFw+eAAQAA8ZObAA+m7MGoE1LB5AfZ1GjUfMl6T0dpaYlxx1lZj1RTha6PIf9Q2cP0l1CH5Yo8KTFrZsyrnSpnbOQTbELOo/TlKpH8IoAk5oSNDJ9VbN70iEDA5yuDUPoVcP5VgK7tZO5/ISrzg8ulwx6QPaSj+192kVcKwH2yZFkmMNWwTWGftLEgrA4/W87+Chjm4oVEEGXlPvcGWcHylAdzaL8vD5K3kRzHw9SLI6O4QKWZP8Y4~1',
            'Host': 'services.gst.gov.in',
            'Referer': 'https://services.gst.gov.in/services/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }

        response = s.get(url,headers=headers)
        # print(response)
        coockiee = response.cookies.get_dict()
        capcoo = coockiee['CaptchaCookie']
        ts = coockiee['TS01b8883c']

        with open('captcha.png','wb')as f:
            f.write(response.content)
        try:
            api = AZCaptchaApi('mmvf0ec5cb6hzjwlsjqovryit1zkxpdr')
            captcha = api.solve('captcha.png')
            result = captcha.await_result()
            print("The captcha is : ", result)
        except Exception as e:
            print(e)

        url = "https://services.gst.gov.in/services/authenticate"
        payload = "{\"username\":\"%s\",\"password\":\"%s\",\"captcha\":\"%s\",\"mFP\":\"{\\\"VERSION\\\":\\\"2.1\\\",\\\"MFP\\\":{\\\"Browser\\\":{\\\"UserAgent\\\":\\\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36\\\",\\\"Vendor\\\":\\\"Google Inc.\\\",\\\"VendorSubID\\\":\\\"\\\",\\\"BuildID\\\":\\\"20030107\\\",\\\"CookieEnabled\\\":true},\\\"IEPlugins\\\":{},\\\"NetscapePlugins\\\":{\\\"PDF Viewer\\\":\\\"\\\",\\\"Chrome PDF Viewer\\\":\\\"\\\",\\\"Chromium PDF Viewer\\\":\\\"\\\",\\\"Microsoft Edge PDF Viewer\\\":\\\"\\\",\\\"WebKit built-in PDF\\\":\\\"\\\"},\\\"Screen\\\":{\\\"FullHeight\\\":864,\\\"AvlHeight\\\":816,\\\"FullWidth\\\":1536,\\\"AvlWidth\\\":1536,\\\"ColorDepth\\\":24,\\\"PixelDepth\\\":24},\\\"System\\\":{\\\"Platform\\\":\\\"Win32\\\",\\\"systemLanguage\\\":\\\"en-GB\\\",\\\"Timezone\\\":-330}},\\\"ExternalIP\\\":\\\"\\\",\\\"MESC\\\":{\\\"mesc\\\":\\\"mi=2;cd=150;id=30;mesc=791572;mesc=927285\\\"}}\",\"deviceID\":null,\"type\":\"username\"}" % (username,password,result)

        # payload = "{\"username\":\"%s\",\"password\":\"%s\",\"captcha\":\"%s\",\"mFP\":\"{\\\"VERSION\\\":\\\"2.1\\\",\\\"MFP\\\":{\\\"Browser\\\":{\\\"UserAgent\\\":\\\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36\\\",\\\"Vendor\\\":\\\"Google Inc.\\\",\\\"VendorSubID\\\":\\\"\\\",\\\"BuildID\\\":\\\"20030107\\\",\\\"CookieEnabled\\\":true},\\\"IEPlugins\\\":{},\\\"NetscapePlugins\\\":{\\\"PDF Viewer\\\":\\\"\\\",\\\"Chrome PDF Viewer\\\":\\\"\\\",\\\"Chromium PDF Viewer\\\":\\\"\\\",\\\"Microsoft Edge PDF Viewer\\\":\\\"\\\",\\\"WebKit built-in PDF\\\":\\\"\\\"},\\\"Screen\\\":{\\\"FullHeight\\\":864,\\\"AvlHeight\\\":816,\\\"FullWidth\\\":1536,\\\"AvlWidth\\\":1536,\\\"ColorDepth\\\":24,\\\"PixelDepth\\\":24},\\\"System\\\":{\\\"Platform\\\":\\\"Win32\\\",\\\"systemLanguage\\\":\\\"en-GB\\\",\\\"Timezone\\\":-330}},\\\"ExternalIP\\\":\\\"\\\",\\\"MESC\\\":{\\\"mesc\\\":\\\"mi=2;cd=150;id=30;mesc=791572;mesc=927285\\\"}}\",\"deviceID\":null,\"type\":\"username\"}" % username,password,result
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '859',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': f'Lang=en; ak_bmsc=C805E422BAC88ECA00C6C6372CD4A85A~000000000000000000000000000000~YAAQBcAsMb7Fw+eAAQAAYZGbAA8/MSkl1a/4yTZk10qFBmEnLVLMmrv6X0XXqGzo9JfIp+2QtIezSk8wKVFYEPQPkCGRVUFRyE7qQqhwCTPT36Dz+v8hqz90u31dFCD+8Q9mCFLaow5i7Xg9gJKfyQpwKp8Yvp5TQJ/oQC6HXKk6Pe2iMYhX8jFJaOyFgupgWEZWNZQpcYg+AgmKiz+sDlGHw2X1RIYACb8z1u3SJUpaEy/kY92lo2sH+qq6NzbshRPrnUdqb/URcPeVMPCbdRn86fd5Gm/Xn0BdSwceVc6Zm9bfg4Oo/UeHoj5tq8SerSJFI8AY/klFvdxpS8VyHwRalreXXYLBIHfdCyJcxskpTNK5pWCNpBXsYH8lbuyd; bm_sv=01478F59B48EA5443DDD8EA2D24C4103~YAAQBcAsMcrFw+eAAQAA8ZObAA+m7MGoE1LB5AfZ1GjUfMl6T0dpaYlxx1lZj1RTha6PIf9Q2cP0l1CH5Yo8KTFrZsyrnSpnbOQTbELOo/TlKpH8IoAk5oSNDJ9VbN70iEDA5yuDUPoVcP5VgK7tZO5/ISrzg8ulwx6QPaSj+192kVcKwH2yZFkmMNWwTWGftLEgrA4/W87+Chjm4oVEEGXlPvcGWcHylAdzaL8vD5K3kRzHw9SLI6O4QKWZP8Y4~1; CaptchaCookie ={capcoo}; TS01b8883c={ts};',
            'Host': 'services.gst.gov.in',
            'Origin': 'https://services.gst.gov.in',
            'Referer': 'https://services.gst.gov.in/services/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }


        response = s.post(url,headers=headers,data=payload)
        coockiee = response.cookies.get_dict()
        # print(response.text)
        # print(coockiee)
        try:
            error_c = response.text.split('"errorCode":"')[1].split('","') 
            print(error_c)
            if  "SWEB_9014" in error_c[0]:
                print('username block')
                return 0
                # break
            elif "AUTH_9033" in error_c[0]:
                print('password expired')
                updatestattus('3',username)
                return 0
            elif "AUTH_9002" in error_c[0]:
                print('wrong password')
                updatestattus('2',username)
                return 0
            elif "SWEB_9000" in error_c[0]:
                print('wrong captcha')
                # return 0
 
        except:
            pass
        try:
            a = 0
            res = response.text.split('"message":"')[1].split('","')[0]
            if res == "auth":
                with  open('auth.txt', 'w') as f:
                    f.write(coockiee['AuthToken'])
                a = 1
                return 1
            else:
                pass #create_authtoken(username,password)
            if a == 1:
                break
        except Exception as e:
            print(e)
            pass #create_authtoken(username,password)
    
def login_info():
    mydb = mysql.connector.connect(
        # host="185.214.126.3",
        # user="u653283300_gst",
        # password="Gst@1234",
        # database="u653283300_gst"
        host="161.97.177.80",
        user="bipin_gstin",
        password="Gstin@123",
        database="gstin_bipin_cred"
    )
    # 'u653283300_gst','Gst@1234','u653283300_gst'
    # id = random.randint(1,10)
    mycursor = mydb.cursor()
    try:
        sql = f"""SELECT * FROM `acli` WHERE status='1' ORDER BY rand() LIMIT 1 """
        mycursor.execute(sql)
        records = mycursor.fetchall()
        # print(records)
    except Exception as e:
        print(e)

    return records



def create_token():
    while True:
        try:
            while True:
                try:
                    print("Getting data from database")
                    info = login_info()
                    print(info)
                    usser_name = info[0][6]
                    password = info[0][7]
                    break
                except:
                    print("data not found")
                    time.sleep(2)
            
            # print(f"The username is {usser_name} and password is {password}")
            flag = create_authtoken(usser_name, password)
            if flag != 1:
                create_authtoken(usser_name, password)
            else:
                break
        except:
            pass
    return 0

if __name__ =='__main__':
    while True:
        try:
            now = datetime.now(timezone("Asia/Kolkata"))
            current_time = now.strftime("%H:%M")
            if not "00:30" < current_time < "06:30":
                try:
                    f = open('auth.txt', 'r')
                    f.close()
                    print("File Exist")
                    time.sleep(10)
                except:
                    print("File Does not exist")
                    create_token()
                check_login('03AARFS1372G1Z6')
            else:
                print("Program is Sleeping")
                time.sleep(300)
        except:
            pass
