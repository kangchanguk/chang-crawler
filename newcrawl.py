from selenium import webdriver
from requests import get
from PIL import Image
import urllib.request
import os
import cv2
import io
import time
import numpy as np
import ssl
import pytesseract
import mysql.connector
from reader import load_data_mall

check=0


def hcropimg(path,num):
    im=Image.open(path)
    pix=np.array(im)
    count=0
    arraylist=[]
    arr=[]
    for i in range(pix.shape[1]):
        if (pix[:,i]>235).sum() == 3*pix.shape[0]:
            arraylist.append(i)
    if len(arraylist)>1:        
        for i in range(len(arraylist)-1):
            if arraylist[i+1]-arraylist[i]>50:
                area=(arraylist[i],0,arraylist[i+1],pix.shape[0])
                im=im.crop(area)
                im.show()

    pix=np.array(im)
    for i in range(pix.shape[0]):
        if (pix[i,:]>235).sum() ==3*pix.shape[1]:
            arr.append(i)

    if len(arr)>1:
        for i in range(len(arr)-1):
            if arr[i+1]-arr[i]>50:
                area=(0,arr[i],pix.shape[1],arr[i+1])
                cropimg =im.crop(area)
                cropimg.save("cropfolder{}/{}.jpg".format(num,count))
                count+=1
    return count
  
        
def wcropimg(num,count):
    filelist=os.listdir("cropfolder{}/".format(num))
    for i in filelist:
        path="cropfolder{}/".format(num)+str(i)
        print(path)
        im=Image.open(path)
        pix=np.array(im)
        arraylist=[]
        arr=[]
    
        for i in range(pix.shape[0]):
            if (pix[i,:]>235).sum() ==3*pix.shape[1]:
                arr.append(i)

        if len(arr)>1:
            for i in range(len(arr)-1):
                if arr[i+1]-arr[i]>50:
                    area=(0,arr[i],pix.shape[1],arr[i+1])
                    im=im.crop(area)
                    im.show()

        pix=np.array(im)
        for i in range(pix.shape[1]):
            if (pix[:,i]>200).sum() == 3*pix.shape[0]:
                arraylist.append(i)
        if len(arraylist)>1:        
            for i in range(len(arraylist)-1):
                if arraylist[i+1]-arraylist[i]>50:
                    area=(arraylist[i],0,arraylist[i+1],pix.shape[0])
                    cropimg =im.crop(area)
                    cropimg.save("cropfolder{}/{}.jpg".format(num,count))
                    count+=1
        print(arraylist)
    return count 

def crop(path1,num,num1):
    filelist=os.listdir(path1)
    count=0
    for i in filelist:
        path=path1+"/"+str(i)
        im=Image.open(path)
        pix=np.array(im)
        if im.size[1]>1000:
            
            arraylist=[]
            arr=[]
            for i in range(pix.shape[1]):
                if (pix[:,i]>235).sum() == 3*pix.shape[0]:
                    arraylist.append(i)
            if len(arraylist)>1:        
                for i in range(len(arraylist)-1):
                    if arraylist[i+1]-arraylist[i]>50:
                        area=(arraylist[i],0,arraylist[i+1],pix.shape[0])
                        im=im.crop(area)
                        im.show()

            pix=np.array(im)
            for i in range(pix.shape[0]):
                if (pix[i,:]>235).sum() ==3*pix.shape[1]:
                    arr.append(i)

            if len(arr)>1:
                for i in range(len(arr)-1):
                    if arr[i+1]-arr[i]>50:
                        area=(0,arr[i],pix.shape[1],arr[i+1])
                        cropimg =im.crop(area)
                        cropimg.save("{}/{}/crop{}.jpg".format(num,num1,count))
                        count+=1
                im.close()
                os.remove(path)
        else:
            im.close()
            os.remove(path)

def show(url):
    browser = webdriver.Chrome("chromedriver.exe")
    browser.get(url)
    clothes=[]
    a=browser.find_elements_by_tag_name("a")
    for i in range(len(a)):
        x=a[i].get_attribute("href")
        b=a[i].find_elements_by_tag_name("img")
        if len(b)>0 and x != None:
            li=[]
            li.append(x)
            li.append(b[0].get_attribute("src"))
            li1=[]
            li1.append(x)
            li1.append(b[0].get_attribute("ec-data-src"))
            if len(li)==2:
                if li[1] is not None:
                    if 'base64' not in str(li[1]):
                        clothes.append(li)
            if len(li1)==2:
                if li1[1] is not None:
                    if 'base64' not in str(li[1]):
                        clothes.append(li)
    for i in range(len(clothes)):
        print(i)
        print(clothes[i][1])

    
    
            
    browser.close()
    return clothes

def godir(clothes,num):
    context = ssl._create_unverified_context()
 
    for i in range(len(clothes)):
        if len(clothes[i])>1:
            if not(os.path.isdir("{}/{}".format(num,i))):
                os.makedirs(os.path.join("{}/{}".format(num,i)))
            if "htt" in clothes[i][0]:
                browser = webdriver.Chrome("chromedriver.exe")
                browser.get(clothes[i][0])
                a=browser.find_elements_by_tag_name("img")
                for j in range(len(a)):
                    x=a[j].get_attribute("src")
                    if len(x)>0:
                        if "htt" in x:
                            print(x)
                            urllib.request.urlretrieve(x,"{}/{}/{}.png".format(num,i,j))
                    
                browser.close()

            filelist=os.listdir("{}/{}".format(num,i))
            for k in filelist:
                path1="{}/{}".format(num,i)+"/"+str(k)               
                select(path1)
            crop("{}/{}".format(num,i),num,i)

            

def check(path,clothes,num):
    image=Image.open(path)
    if image.size[0]<300 or image.size[1]<300:
        image.close()
        os.remove(path)
    else:    
        try:
            clothesline=pytesseract.image.image_to_string(path)
            if len(clothesline)>5:
                image.close()
                os.remove(path)
        except:
            pass
    
def download(clothes,num):
    context = ssl._create_unverified_context()
    for i in range(len(clothes)):
        if len(clothes[i])>1:
            if clothes[i][1] is not None:
                
                f.write(str(clothes[i][0]))
                f.write("\n")
             
                if "gif" in clothes[i][1]:
                    urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.gif".format(num,num,i))
                    print("{}/{}-{}.gif".format(num,num,i))

                elif "webp" in clothes[i][1]or "jpg" in clothes[i][1]:
                    urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.jpg".format(num,num,i))
                    print("{}/{}-{}.jpg".format(num,num,i))

                elif  "png" in clothes[i][1]:
                    urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.png".format(num,num,i))
                    print("{}/{}-{}.png".format(num,num,i))

def capturegif(path,num):
    filelist=os.listdir(path)
    for im in filelist:
        if ".gif" in str(im):
            adr=path+str(im)
            name=str(im).replace(".gif","")
            print(name)
            cap=cv2.VideoCapture(adr)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if length > 5:
                continue
            print(length)
            cnt=0
            while(cap.isOpened):
                if length-1<cnt:
                    break
                ret, frame = cap.read()
                cv2.imwrite("{}/".format(num)+name+"-{}.jpg".format(cnt),frame)
                cnt+=1
            cap.release()
            os.remove(adr)

def select(path):
    image=Image.open(path)
    print(path)
    global check
    if image.size[0]<300 or image.size[1]<300:
        image.close()
        os.remove(path)
        check=1
    else:    
        try:
            clothesline=pytesseract.image_to_string(path)
            if len(clothesline)>3:
                image.close()
                os.remove(path)
                check=1

        except:
            pass
 
#main함수 영역


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    row=load_data_mall()
    for i in range(len(row)):
        url = row[i][1]
        num =i #몇번째 줄의 쇼핑몰 주소로 부터 크롤링 해오는 지를 알려주는 index
        sentence=""#같은 url의 페이지를 크롤링하는 것을 방지하기 위한 변수
        if sentence in url:
            count=0
            clothes=[]
            if not(os.path.isdir("{}".format(num))):
                os.makedirs(os.path.join("{}".format(num)))
            f=open('{}/{}suburl.txt'.format(num,num),'w',encoding='utf-8',newline='')
            f.write(url)
            clothes=show(url)
            download(clothes,num)
            f.close()
            
            path="{}/".format(num)
            capturegif(path,num)
            filelist=os.listdir("{}/".format(num))
            for i in range(len(filelist)):
                if ".jpg" in str(i) or ".png" in str(i):
                    check=0
                    path="{}/".format(num)+str(i)
                    select(path)
                                    
            godir(clothes,num)
            sentence=url
    
            