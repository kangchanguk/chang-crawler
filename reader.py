import mysql.connector
import csv
import os

config={

        "user":"root",

        "password":"koetri322",

        "host":"localhost",   

        "database":"acloset",

        "port":3306

    }

def write_url_to_csv(name, url):
    f = open('fashionurl.csv','a',newline='')
    wr=csv.writer(f)
    wr.writerow([name,url,False])
    f.close()

def read_url_from_csv():
    f= open('fashionurl.csv','r')
    rdr= csv.reader(f)
    return rdr

def save_data_mall(name,url):
    try:
        conn = mysql.connector.connect(**config)
        cursor=conn.cursor()
        sql = "INSERT into mall(id,url,done) values (%s, %s, %s)"
        cursor.execute(sql,(name,url,False))
        conn.commit()
        conn.close()
    except:
        pass
def load_data_mall():
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    sql1 = "select * from mall"
    cursor.execute(sql1)
    rows= cursor.fetchall()
    conn.close()
    return rows

def clear_table_mall():
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    sql1 = "truncate mall"
    cursor.execute(sql1)
    conn.commit()
    conn.close()

def clear_csv():
    os.remove("fashionurl.csv")





if __name__ == '__main__':
    write_url_to_csv("benito","https://www.benito.co.kr/")
    write_url_to_csv("hypnotic","http://www.hypnotic.co.kr")
    write_url_to_csv("sedy","https://sedy.co.kr")
    write_url_to_csv("naning9","https://www.naning9.com")
    write_url_to_csv("frombeginning","http://beginning.kr")

    list=read_url_from_csv()

    for row in list:
        save_data_mall(row[0],row[1])
    print(load_data_mall())




