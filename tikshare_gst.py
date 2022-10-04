from time import sleep
import requests
from bs4 import BeautifulSoup
# import re
import read_write_database as db
import configparser

config = configparser.ConfigParser()

def insert_gst_basic(data):
    cursor = db.connect()
    cur = cursor.cursor()
    
    insert_query = ''' insert ignore into
    gst_basic (gstid,source) values ('{0}','tikshare') '''.format(data)
    try:
        cur.execute(insert_query)
        cursor.commit()
        print("gst_basic insert success")
    except Exception as e:
        print("gst_basic insert unsuccess",insert_query)
        print(e)
    cursor.close()

# def gst_valid(str):

#     regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{2}"
     
#     p = re.compile(regex)
 
#     if (str == None):
#         return False
 
#     if(re.search(p, str)):
#         return True
#     else:
#         return False

def update_name(name_old):
    if len(name_old) == 2:
        ord_o = ord(name_old[1])
        if ord_o < 122:
            n_ord = ord_o+1
            name = name_old[0]+chr(n_ord)
        else:
            ord_o = ord(name_old[0])
            if ord_o < 122 :
                name=chr(ord_o+1)+'a'
    elif len(name_old) == 3:
        ord_o = ord(name_old[2])
        if ord_o < 122:
            n_ord = ord_o+1
            name = name_old[:2]+chr(n_ord)
        else:
            ord_o = ord(name_old[1])
            if ord_o < 122 :
                name = name_old[0] + chr(ord_o+1)+'a'
            else:
                f_ord = ord(name_old[0])
                name = chr(f_ord+1) + 'aa'
    elif len(name_old) == 4:
        ord_o = ord(name_old[3])
        if ord_o < 122:
            n_ord = ord_o+1
            name = name_old[:3]+chr(n_ord)
        else:
            ord_o = ord(name_old[2])
            if ord_o < 122 :
                name = name_old[:2] + chr(ord_o+1)+'a'
            else:
                f_ord = ord(name_old[1])
                if f_ord < 122 :
                    name = name_old[0]+chr(f_ord+1) + 'aa'
                else:
                    name = chr(ord(name_old[0])+1)+ 'aaa'
        return name
    return name

def get_gst(name):
    print(name)

    url = "https://tikshare.com/?gstsearch="+name

    payload={}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'Host': 'tikshare.com'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response)
    if response.status_code ==200:
        soup2 = BeautifulSoup(response.content, 'lxml')
        result = soup2.find('div', attrs={'class': "col-12 resultdiv"})

        gst_list = [i.text.strip() for i in result.findAll('strong')]
        for gst in gst_list:
            insert_gst_basic(gst)
    if response.status_code == 50:
        return 0

get_gst('aa')
if __name__ =="__main__":
    config.read('tikshare.conf')
    wdcounter = config['word']['word'] if config['word']['word'] else 'aa'
    while True:
        config['word']['word'] = wdcounter
        with open('tikshare.conf','w') as fil:
            config.write(fil)
        if get_gst(wdcounter) == 0:
            sleep(200)
            continue

        # print(wdcounter)
        # sleep(1)
        if wdcounter == 'zz':
            wdcounter = 'aaa'
        if wdcounter =="zzzz":
            wdcounter = 'aaaa'
        else:
            wdcounter = update_name(wdcounter)