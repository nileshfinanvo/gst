import random
import requests
from bs4 import BeautifulSoup
import time
# import pprint
import read_write_database as db

def insert_data(data):
    cursor = db.connect()
    cur = cursor.cursor()
    # data = tuple(*data)
    for i in data:
        insert_query = ''' insert ignore into
        gst_basic (name,gstid,state,source)
        values (%s,%s,%s,'octacloud')
        ON DUPLICATE KEY UPDATE name = '{0}',
        gstid= '{1}',state= '{2}' '''.format(*tuple(data[i].values()))
        try:
            cur.execute(insert_query,tuple(data[i].values()))
            cursor.commit()
            print("data insert success")
        except Exception as e:
            print("data insert unsuccess")
            print(e)

def cloud_octa(name):
    cursor = db.connect()
    cur = cursor.cursor()
    Counter = 0
    f_data = {}
    for i in range(1,11):
        if Counter <= i and i != 1:
            break
        print('page==',i)
        url = f"https://cloud.octagst.com/gstin?q={name}&adv=False&p={i}"
        print(url)

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)

        soup = BeautifulSoup(response.text, 'lxml')
        noda  = soup.find('p',{'class':'lead'})
        if 'Your search did not match any company' in noda.text:
            print(noda.txt)
            return
        if i == 1 :
            Counter = int(soup.find('p',{'class':'lead mb-4'}).text.split('Showing page 1 of ')[1].split('.')[0])

        namelist = [i.text.strip()
                    for i in soup.findAll('h4', attrs={'class': "mb-0"})]
        detailsList = [i.text.strip()
                    for i in soup.findAll('p', attrs={'class': "mb-4"})][1:]
        data = {}
        for i in range(len(namelist)):
            rand = random.randrange(10, 20, 1)
            detail = detailsList[i].strip().split('\n')[0]
            detaillis = detail.split('—')
            # print(f'{rand}{i}')
            data[f'{rand}{i}'] = {
                'name': cur._connection.converter.escape(namelist[i].strip()),
                'gst' : detaillis[1].strip(),
                'state': detaillis[0].strip()
            }

        insert_data(data)
        # print(pprint.pprint(data))
        f_data.update(data)
        time.sleep(2)
    # print(pprint.pprint(f_data))
    return f_data
        # time.sleep(20)
    
