import requests
from bs4 import BeautifulSoup
import read_write_database as db
def insert_gst_basic(*data):
    # print(data)
    cursor = db.connect()
    cur = cursor.cursor()
    
    # insert_query = ''' insert ignore into
    # gst_basic (name,gstid,state,status,gst_bd,gst_gd,gst_fd,gst_pan)
    # values (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name = '{0}',
    # gstid= '{1}',state= '{2}',status= '{3}' '''.format(*data)
    insert_query = ''' insert ignore into
    gst_basic (name,gstid,state,status,gst_bd,gst_gd,gst_fd,gst_pan,source)
    values (%s,%s,%s,%s,%s,%s,%s,%s,'jamku') ON DUPLICATE KEY UPDATE name = '{0}',
    gstid= '{1}',state= '{2}',status= '{3}',source='jamku' '''.format(*data)
    try:
        cur.execute(insert_query,data)
        cursor.commit()
        print("gst_basic insert success")
    except Exception as e:
        print("gst_basic insert unsuccess",insert_query)
        print(e)

def insert_gst_details(*data):
    cursor = db.connect()
    cur = cursor.cursor()
    
    insert_query = ''' INSERT IGNORE INTO gst_detail (tradeNam,gstin,sts,lgnm,rgdt,dty,ctb,pan) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
    ON DUPLICATE KEY UPDATE tradeNam = '{0}',gstin= '{1}',sts= '{2}',lgnm= '{3}',rgdt= '{4}',dty= '{5}',ctb= '{6}',pan= '{7}' '''.format(*data)
    try:
        cur.execute(insert_query,data)
        cursor.commit()
        print("gst_details insert success")
    except Exception as e:
        print("gst_details insert unsuccess")
        print(e)

def insert_data(*data):
    cursor = db.connect()
    cur = cursor.cursor()
    
    insert_query = '''insert ignore into   gstin_hsn_sac_directory (code ,details,type)
    values (%s,%s,%s) ON DUPLICATE KEY UPDATE code = '{0}',details= '{1}',type= '{2}' '''.format(*data)
    try:
        cur.execute(insert_query,data)
        cursor.commit()
        print(f"{data[2]} insert success")
    except Exception as e:
        print(f"{data[2]} insert unsuccess")
        print(e)

def get_crawling(gst):
    cursor = db.connect()
    cur = cursor.cursor()
    url = f'https://gst.jamku.app/gstin/{gst}'
    headers = {}

    response = requests.request("GET", url, headers=headers)

    soup = BeautifulSoup(response.text,"lxml")
    main_data = soup.find('section',{'meta':'[object Object]'})
    m_rows = main_data.find_all('p',{'class','capitalize'})
    for m_row in m_rows:
        link = m_row.find('a')
        link_obj = link['href'].split('/')[-1].strip()
        code = link_obj.split('-')[-1]
        type = 'HSN' if link_obj.split('-')[0] == 'G' else 'SAC'
        details = link.text.strip()
        insert_data(code.strip(),cur._connection.converter.escape(details),type)

    data_table = soup.find('div',{'class','p-2 mt-3 shadow-md'})
    rows  = data_table.find_all('div',{'class','tax-row'})
    data = {}
    for row in rows:
        ps = row.find_all('p')
        data[ps[0].text.strip()] = ps[1].text.strip()
    # print(data)

    try:
        insert_gst_basic(data['Trade Name'],gst,data['Place of Business'].split(',')[-1].strip(),data['Registration Status'].split('\n')[0].strip(),'0','0','0','0')
    except:
        pass

    try:
        insert_gst_details(data['Trade Name'],gst,data['Registration Status'].split('\n')[0].strip(),data['Legal Name'],data['Registration Date'].split('\n')[0].strip(),data['Registration Type'],data['Entity Type'],data['PAN'])
    except:
        pass
def main(url1,id):
    print(url1)
    url = "https://gst.jamku.app/business/"+url1

    headers = {}

    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    main_data = soup.find('ol',{'class':'mt-5'})
    all_rows = main_data.find_all('li')
    gstins = []
    for row in all_rows:
        gstin = row.find('a')['href'].split('/')[-1]
        # name = row.text.strip()
        # legalname = name.split('(')[-1].split(')')[0]
        # tradename = name.split('    ')[0]
        # print(gstin,legalname.strip(),tradename.strip())
        gstins.append(gstin)
    
    for gst in gstins:
        get_crawling(gst)

    cursor = db.connect()
    cur = cursor.cursor()

    update_qu = f"update gstin_hsn_sac_directory set `flag` = 1 where `id` = '{id}'"
    try:
        cur.execute(update_qu)
        cursor.commit()
        print("update 1 success")
    except Exception as e:
        print(e)
    
def read(num):
    cursor = db.connect()
    cur = cursor.cursor()
    sql = f"SELECT id,code,type FROM gstin_hsn_sac_directory WHERE flag != 1 and type='SAC'  ORDER BY `gstin_hsn_sac_directory`.`id` DESC LIMIT {num}" 
    cur.execute(sql)
    records = cur.fetchall()
    return records

if __name__ == "__main__":
    limit_count = 2

    count = 1000

    for index in range(0,count,1):
        rows =  read(limit_count)
        for row in rows:
            if 'HSN' == row[-1]:
                type = 'G'
            else:
                type = 'S'
            url = type +'-'+row[1]
            main(url,row[0])
