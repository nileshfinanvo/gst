import read_write_database as db

def insert_gst_basic(*data):
    cursor = db.connect()
    cur = cursor.cursor()
    # print(data)
    
    cursor.close()
def main():
    cursor = db.connect()
    cur = cursor.cursor()
    slq_lin = []
    with open('gstnumbers.txt') as fil:
            a = fil.readlines()
            for i in a:
                val = [j.replace('"',"") for j in i.split(',')]
                data = [cur._connection.converter.escape(k) for k in val[:2]]
                insert_query = f''' insert ignore into gst_basic (gstid,name,gst_bd,gst_fd,gst_pan,gst_gd) values ('{data[0]}','{data[1]}','2','2','0','0') '''
                slq_lin.append(insert_query)
    for slq_lin1 in slq_lin:
        fil1= open('gst_numbers.sql','a') 
        fil1.write(slq_lin1+"\n")
        # try:
        #     cur.execute(insert_query)
        #     cursor.commit()
        #     print("gst_basic insert success")
        # except Exception as e:
        #     print("gst_basic insert unsuccess",insert_query)
        #     print(e)
        
 
main()