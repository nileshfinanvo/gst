import requests
from bs4 import BeautifulSoup
import read_write_database as db
import configparser
config = configparser.ConfigParser()

def insert_gst_basic(data):
    cursor = db.connect()
    cur = cursor.cursor()
    
    insert_query = ''' insert ignore into
    gst_basic (gstid,source) values ('{0}','gstserver') '''.format(data)
    try:
        cur.execute(insert_query)
        cursor.commit()
        print("gst_basic insert success")
    except Exception as e:
        print("gst_basic insert unsuccess",insert_query)
        print(e)
    cursor.close()


def get_gst_numbers(url):
    # url = "https://gstserver.com/gst/andaman-nicobar-islands/35"
    print(url)
    payload={}
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'gstserver.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response
def process_gst(url):
    response = get_gst_numbers(url)
    soup = BeautifulSoup(response.text,"lxml")
    try:
        rows = soup.find('div',{'class':'row mb-4'})
        cols = rows.find_all('div',{'class':'col-md-6 col-lg-4 mb-2'})
        for col in cols:
            # pass
            insert_gst_basic(col.text.strip())
        return 'success'
    except:
        return 'error'

# get_gst_numbers('https://gstserver.com/gst/andaman-nicobar-islands/35/2')
def get_last_number(url):
    response = get_gst_numbers(url)
    soup = BeautifulSoup(response.text,"lxml")
    last = soup.find('div',{'class','dataTables_info'})
    # print(last.text.split(' ')[-3])
    lp = int(int(last.text.split(' ')[-3]) / 30) +1
    print(lp)
    return lp
def main():
    urls_lists = ['/gst/andaman-nicobar-islands/35', '/gst/andrapradesh-new/37', '/gst/arunachal-pradesh/12', '/gst/assam/18', '/gst/bihar/10', '/gst/center-jurisdiction/99', '/gst/chandigarh/04', '/gst/chhattisgarh/22', '/gst/dadra-and-nagar-haveli-and-daman-and-diu-new-merged-ut/26', '/gst/daman-diu-old/25', '/gst/delhi/07', '/gst/goa/30', '/gst/gujarat/24', '/gst/haryana/06', '/gst/himachal-pradesh/02', '/gst/jammu-kashmir/01', '/gst/jharkhand/20', '/gst/karnataka/29', '/gst/kerala/32', '/gst/ladakh-new/38', '/gst/lakshadweep/31', '/gst/madhya-pradesh/23', '/gst/maharashtra/27', '/gst/manipur/14', '/gst/meghalaya/17', '/gst/mizoram/15', '/gst/nagaland/13', '/gst/orissa/21', '/gst/other-territory/97', '/gst/puducherry/34', '/gst/punjab/03', '/gst/rajasthan/08', '/gst/sikkim/11', '/gst/tamil-nadu/33', '/gst/telengana/36', '/gst/tripura/16', '/gst/uttar-pradesh/09', '/gst/uttarakhand/05', '/gst/west-bengal/19']
    config.read('counter.conf')
    c_url = config['url']['url'] if config['url']['url'] else '/gst/andaman-nicobar-islands/35'
    c_page = int(config['page']['page']) if config['page']['page'] else 1
    for urls in urls_lists[urls_lists.index(c_url):]:
        pages = get_last_number('https://gstserver.com'+urls)
        # print(c_page,pages+1,1)
        for page in range(int(c_page),pages+1,1):
            config['url']['url'] =urls
            config['page']['page'] = str(page)
            with open('counter.conf','w') as fil:
                config.write(fil)
            if page!= 1:
                process_gst('https://gstserver.com'+urls+f'/{page}')
            else:
                process_gst('https://gstserver.com'+urls)
            # print(page,type(page),pages,type(pages))
            if page == pages:
                config['page']['page'] = ''
                with open('counter.conf','w') as fil:
                    config.write(fil)
        c_page = 1
            
if __name__ == "__main__":
    main()
    # get_last_number('https://gstserver.com'+'/gst/andrapradesh-new/37')