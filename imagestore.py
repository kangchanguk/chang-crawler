import mysql.connector
import os
from PIL import Image

config={

        "user":"root",

        "password":"koetri322",

        "host":"localhost",   

        "database":"acloset",

        "port":3306

}

def save_data_mainimage(num,name,src,url):
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    try:
        sql = "INSERT into mainimage(id,mall_id,src,url) values (%s, %s, %s, %s)"
        cursor.execute(sql,(int(num),name,src,url))
        conn.commit()
    except:
        pass
    conn.close()

def load_id(num):
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    sql1 = "select * from mall"
    cursor.execute(sql1)
    rows= cursor.fetchall()
    sql ="SELECT COUNT(*) FROM mall"
    cursor.execute(sql)
    amount=cursor.fetchall()
    conn.close()
    return rows[num][0],amount[0][0],rows[num][1]

def show():
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    sql1 = "select * from mainimage"
    cursor.execute(sql1)
    rows= cursor.fetchall()
    return rows

def ref_image_store(nam,subfolderlist):
    count=0
    for folder in subfolderlist:
        conn = mysql.connector.connect(**config)
        cursor=conn.cursor() 
        try:
            filelist=os.listdir("{}/".format(nam) + folder)
            
            for file in filelist:    
                sql = "INSERT into subimage(id,ref,src) values (%s, %s, %s)"
                cursor.execute(sql,(int(count),int(folder),r"C:/Users/KHS/Documents/GitHub/chang-crawler/{}/{}/".format(nam,folder) + file))
                count=count+1
            conn.commit()
           
        except:
            pass
        conn.close()

def ref_show():
    conn = mysql.connector.connect(**config)
    cursor=conn.cursor()
    sql1 = "select * from subimage"
    cursor.execute(sql1)
    rows= cursor.fetchall()
    return rows




def auto_store_to_db(nam,clothes):
    name,num,url=load_id(nam)
    filelist=os.listdir("{}/".format(nam))
    file_list_jpg = [file for file in filelist if file.endswith(".jpg")]
    file_list_png = [file for file in filelist if file.endswith(".png")]
    file_list_txt = [file for file in filelist if file.endswith(".txt")]
    mainlist=file_list_png + file_list_jpg
    subfolderlist= [file for file in filelist if not file.endswith(".txt") and not file.endswith(".png") and not file.endswith(".jpg") and not file.endswith(".gif")] 
    ref_image_store(nam,subfolderlist)

    count=0
    for i in mainlist:
        save_data_mainimage(count,name,r"C:/Users/KHS/Documents/GitHub/chang-crawler/{}/".format(nam) + i,url)
        count=count+1   
    li=show()
    for i in li:
        print(i[2])
    print(ref_show())




