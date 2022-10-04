import requests
from bs4 import BeautifulSoup
# import csv
# import pprint
import read_write_database as db
import configparser

config = configparser.ConfigParser()

def insert_data(*data):
    cursor = db.connect()
    cur = cursor.cursor()
    data = tuple([cur._connection.converter.escape(i)for i in data])
    insert_query = ''' insert ignore into
    gst_basic (gstid,name,state,source)
    values (%s,%s,%s,'knowyourgst')
    ON DUPLICATE KEY UPDATE gstid= '{0}',
    name= '{1}',state= '{2}',source='knowyourgst' '''.format(*data)

    try:
        cur.execute(insert_query,data)
        cursor.commit()
        print("knowyourgst insert success")
    except Exception as e:
        print("knowyourgst insert unsuccess")
        print(e)

def get_csrf():
    url = "https://www.knowyourgst.com/gst-number-search/by-name-pan/"
    headers = {
    'Cookie': 'csrftoken=WNkYPoK4lqrLezpsV1wr7rsE1bX8wymen8nsd0Lb9KnemHYc98Ax793JjU7hZNvG'
    }
    response = requests.request("GET", url, headers=headers)

    soup = BeautifulSoup(response.content, 'lxml')
    csrf = soup.find('input', attrs={'name': "csrfmiddlewaretoken"})['value']

    return csrf

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

# def update_name(name_old):    
#     ord_o = ord(name_old[3])
#     if ord_o < 122:
#         n_ord = ord_o+1
#         name = name_old[:3]+chr(n_ord)
#     else:
#         ord_o = ord(name_old[2])
#         if ord_o < 122 :
#             name = name_old[:2] + chr(ord_o+1)+'a'
#         else:
#             f_ord = ord(name_old[1])
#             if f_ord < 122 :
#                 name = name_old[0]+chr(f_ord+1) + 'aa'
#             else:
#                 name = chr(ord(name_old[0])+1)+ 'aaa'
#     return name

def knowyourgst(name):
    print(name)
    csrf = get_csrf()
    
    url = "https://www.knowyourgst.com/gst-number-search/by-name-pan/"
    payload={'csrfmiddlewaretoken': f'{csrf}','gstnum': f'{name}'}
    headers = {
    'cookie': f'csrftoken={csrf}; _ga=GA1.2.1039246515.1626869630; _gid=GA1.2.1398229936.1626869630; __gads=ID=0c5d3ee09335894f-22ba7d1774ca00cc:T=1626870340:RT=1626870340:S=ALNI_MYF2f0jRkIWXCprJ4FSllSItw4-Nw; _pbjs_userid_consent_data=3524755945110770; _gat=1; __viCookieActive=true;'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    soup2 = BeautifulSoup(response.content, 'lxml')
    result = soup2.find('div', attrs={'class': "col l7 s12 firstcolumn"})

    namelist = [i.text.strip() for i in result.findAll('h5')]
    detailsList = [i.text.strip() for i in result.findAll('span', attrs={'class': "black-text"})]

    # data = {}
    for i in range(len(detailsList)):
        detail = detailsList[i].split(',')

        insert_data(detail[1].strip(),namelist[i].strip(),detail[0].strip())
        # data[i]={
        #     'name' : namelist[i].strip(),
        #     'gst' : detail[1].strip(),
        #     'state' : detail[0].strip(),
        # }
    # print(data)
# knowyourgst('aa')
if __name__ =="__main__":
    config.read('knowgst.conf')
    wdcounter = config['word']['word'] if config['word']['word'] else 'aa'
    while True:
        config['word']['word'] = wdcounter
        with open('knowgst.conf','w') as fil:
            config.write(fil)
        knowyourgst(wdcounter)
        # print(wdcounter)
        if wdcounter == 'zz':
            wdcounter = 'aaa'
        if wdcounter =="zzzz":
            wdcounter = 'aaaa'
        else:
            wdcounter = update_name(wdcounter)