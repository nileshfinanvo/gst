import requests
from bs4 import BeautifulSoup
import re
import read_write_database as db
import configparser
config = configparser.ConfigParser()

def insert_gst_basic(data):
    cursor = db.connect()
    cur = cursor.cursor()
    
    insert_query = ''' insert ignore into
    gst_basic (gstid,source) values ('{0}','vpd') '''.format(data)
    try:
        cur.execute(insert_query)
        cursor.commit()
        print("gst_basic insert success")
    except Exception as e:
        print("gst_basic insert unsuccess",insert_query)
        print(e)
    cursor.close()

def gst_valid(str):

    regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{2}"
     
    p = re.compile(regex)
 
    if (str == None):
        return False
 
    if(re.search(p, str)):
        return True
    else:
        return False

def crowling2(url):

    # url = "https://vdocument.in/sno-firm-name-gstin-id-jurisdiction-1-ramkrishna-forgings-.html"

    payload={}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'vdocument.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    soup = BeautifulSoup(response.text,'lxml')
    # trans = soup.find('div',{'class',"transcript word-break"}).text
    try:
        obj = soup.text.split(' ')
        for robj in obj:
            if len(robj) == 15:
                val = gst_valid(robj)
                if val:
                    insert_gst_basic(robj)
                    # return robj
    except Exception as e:
        print(e)

def crowling(url):

    # url = "https://vdocument.in/sno-firm-name-gstin-id-jurisdiction-1-ramkrishna-forgings-.html"

    payload={}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'vdocument.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    soup = BeautifulSoup(response.text,'lxml')
    # trans = soup.find('div',{'class',"transcript word-break"}).text
    try:
        obj = soup.text.split(' ')
        for robj in obj:
            if len(robj) == 15:
                val = gst_valid(robj)
                if val:
                    insert_gst_basic(robj)
                    # return robj
    except Exception as e:
        print(e)
    # crowling2()
    links = soup.find_all('div',{'class','detail_recommended_right2'})
    for link in links:
        a_link = link.find('a')['href']
        crowling2(a_link)


def main():
    # url = "https://vdocument.in/search?q=gstin"
    config.read('vpdcounter.conf')
    url = config['url']['url'] if config['url']['url'] else 'https://vdocument.in/search?q=gstin'
    while True:
        # print(url)
        config['url']['url'] =url
        with open('vpdcounter.conf','w') as fil:
            config.write(fil)
        payload={}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'vdocument.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        soup2 = BeautifulSoup(response.text,'lxml')
        try:
            obj = soup2.text.split(' ')
            for robj in obj:
                if len(robj) == 15:
                    val = gst_valid(robj)
                    if val:
                        insert_gst_basic(robj)
                        # return robj
        except Exception as e:
            print(e)
        links = soup2.find_all('div',{'class','content_main_search_box'})
        for link in links:
            a_link = link.find('a')['href']
            crowling(a_link)
        try:
            pagin =soup2.find('div',{"class":'pagination'})
            nextpa = pagin.find('span',{"class":"next"})
            url = nextpa.find('a')['href']
            print(url)
        except:
            break
        
if __name__ == "__main__":
    while True:
        main()
    