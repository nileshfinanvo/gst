import requests
import read_write_database as db
import json
import configparser
config = configparser.ConfigParser()

def insert_gst_basic(*data):
    cursor = db.connect()
    cur = cursor.cursor()
    insert_query = f''' insert ignore into gst_basic (gstid,name,source) values ('{data[0]}','{data[1]}','textpayer') '''
    try:
        cur.execute(insert_query)
        cursor.commit()
        print("gst_basic insert success")
    except Exception as e:
        print("gst_basic insert unsuccess",insert_query)
        print(e)
    
    cursor.close()
def get_data(op,state,fy):
    cursor = db.connect()
    cur = cursor.cursor()

    url = "https://services.gst.gov.in/services/auth/api/search/tplist/opteddata"

    payload = "{"+f'"op":"{op}","stcd":"{state}","fy":"{fy}"' +"}"
    try:
        f = open('auth.txt', 'r')
        at_val = f.readline()
        f.close()
    except:
        print('auth removed')
        return 0

    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '48',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': f'AuthToken={at_val};',
    'Host': 'services.gst.gov.in',
    'Origin': 'https://services.gst.gov.in',
    'Referer': 'https://services.gst.gov.in/services/auth/listoftaxpayer',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    
    response = requests.request("POST", url, headers=headers, data=payload)
    if response:
        try:
            textpayerdata = json.loads(response.text)
            # print(textpayerdata)
            try:
                if textpayerdata['error']:
                    return 1
            except:
                # pass
                for datas in textpayerdata:
                    insert_gst_basic(datas['gstin'],cur._connection.converter.escape(datas['lnm']))
                return 1
        except Exception as e:
            print(e)
    else:
        print("File remove")
        return 0
    cursor.close()
# get_data("R","35","2021-2022")       

def main():
    try:
        state_list = ['35','37','12','18','10','4','22','26','7','30','24','6','2','1','20','29','32','38','31','27','23','14','17','15','13','21','97','34','3','8','11','33','36','16','9','5','19']
        config.read('statecounter.conf')
        stcounter = config['state']['state'] if config['state']['state'] else '35'
        for state in state_list[state_list.index(stcounter):]:
            config['state']['state'] =state
            with open('statecounter.conf','w') as fil:
                config.write(fil)
            for op in ["O","R"]:
                for fy in ["2020-2021","2021-2022","2022-2023"]:
                    while True:
                        print(op,state,fy)
                        gd = get_data(op,state,fy)
                        if gd != 0:
                            break 
       
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()