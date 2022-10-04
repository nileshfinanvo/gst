import requests
from openpyxl import load_workbook
import read_write_database as db

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

def get_file():
    url = "https://tutorial.gst.gov.in/downloads/HSN_SAC.xlsx"

    payload={}
    headers = {
    'Host': 'tutorial.gst.gov.in'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    with open('hsn_directory.xlsx','wb') as f:
        f.write(response.content)

def main():
    get_file()
    cursor = db.connect()
    cur = cursor.cursor()
    wb = load_workbook('hsn_directory.xlsx')
    hsns = wb['HSN']
    try:
        for hsno,hsdet in hsns.values:
            try:
                if 'HSN' in hsno:
                    continue
            except:
                pass
            insert_data(hsno,cur._connection.converter.escape(hsdet),'HSN')
    except Exception as e:
        print(e)
    sacs = wb['SAC']
    try:
        for saco,sacdet in sacs.values:
            try:
                if 'SAC Code' in saco:
                    continue 
            except:
                pass
            insert_data(saco,cur._connection.converter.escape(sacdet),'SAC')
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()