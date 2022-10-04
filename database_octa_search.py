import read_write_database as db
import time
import octa_cloud as oc
def update_name(name_old):
    
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

    cursor = db.connect()
    cur = cursor.cursor()

    insert_query = f" update  `gst_name_tab` set name = '{name}' WHERE id = 0 "

    try:
        cur.execute(insert_query)
        cursor.commit()
        print(f"{name} update success")
    except Exception as e:
        print("update unsuccess")
        print(e)
def main2():
    cursor = db.connect()
    cur = cursor.cursor()
    
    select_query = "SELECT name FROM `gst_name_tab` WHERE id = 0" 
    cur.execute(select_query)
    rows =  cur.fetchone()
    print(rows[0])
    oc.cloud_octa(rows[0])
    update_name(rows[0])
  
if __name__ == "__main__":
    while True:
        start_time = time.time()
        main2()
        print("--- %s seconds ---" % (time.time() - start_time))
