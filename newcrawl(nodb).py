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
import csv
import pytesseract
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common import exceptions  

check=0
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
deletelist=[]

#가로로 붙어있는 이미지를 자르기 위한 함수
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
  
#세로로 붙어 있는 이미지를 자르기위한 함수        
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

#현재 메인 함수에서 사용하고 있는 통이미지 자르기 함수
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

#메인 페이지의 이미지 url 주소와 링크 url정보를 가지고 있는 리스트를 만드는 과정 이 리스트를 통해 향후 이미지를 다운로드 하고 다운받은 이미지의 링크 url을 이용해 관련 이미지들을 긁어온다.
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

#이미지에 링크된 주소로 이동하여 관련된 이미지들을 긁어오는 함수이다.
def godir(clothes,num):
    context = ssl._create_unverified_context()
    for i in range(len(clothes)):
        if i not in deletelist:
            try:
                if len(clothes[i])>1:
                    if not(os.path.isdir("{}/{}".format(num,i))):
                        os.makedirs(os.path.join("{}/{}".format(num,i)))
                    if "htt" in clothes[i][0]:
                        try:
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
                        except:
                            pass
                    filelist=os.listdir("{}/{}".format(num,i))
                    for k in filelist:
                        path1="{}/{}".format(num,i)+"/"+str(k)               
                        select(path1)
                    crop("{}/{}".format(num,i),num,i)

            except exceptions.StaleElementReferenceException as e:
                print(e)
                filelist=os.listdir("{}/{}".format(num,i))
                for k in filelist:
                    path1="{}/{}".format(num,i)+"/"+str(k)               
                    select(path1)
                crop("{}/{}".format(num,i),num,i)
  
                
#쇼핑몰 메인 페이지의 이미지들을 긁어오고 db에 저장하는 함수
def download(clothes,num):
    global deletelist
    context = ssl._create_unverified_context()
    for i in range(len(clothes)):
        if len(clothes[i])>1:
            if clothes[i][1] is not None:
                try:
                    if "gif" in clothes[i][1]:
                        urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.gif".format(num,num,i))
                        print("{}/{}-{}.gif".format(num,num,i))
                        capturegif("{}/{}-{}.gif".format(num,num,i),num)
                        if select("{}/{}-{}.jpg".format(num,num,i)) == 1:
                            deletelist.append(i)   
                        
                    elif "webp" in clothes[i][1]or "jpg" in clothes[i][1]:
                        urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.jpg".format(num,num,i))
                        print("{}/{}-{}.jpg".format(num,num,i))
                        if select("{}/{}-{}.jpg".format(num,num,i)) == 1:
                            deletelist.append(i)
                        
                    elif  "png" in clothes[i][1]:
                        urllib.request.urlretrieve(clothes[i][1],"{}/{}-{}.png".format(num,num,i))
                        print("{}/{}-{}.png".format(num,num,i))
                        if select("{}/{}-{}.png".format(num,num,i)) == 1:
                            deletelist.append(i)                       
                except:
                    pass
    
#gif 파일의 첫번째 프레임을 대표이미지로 삼아 저장하는 함수
def capturegif(path,num):
    name=str(path).replace(".gif","")
    print(name)
    cap=cv2.VideoCapture(path)
    cnt=0
    while(cap.isOpened):
        ret, frame = cap.read()
        cv2.imwrite(name+".jpg",frame)
        cnt+=1
        if cnt==1:
            break
    cap.release()
    os.remove(path)

#크기와 글자 유무에 따라 이미지를 선별해주는 함수

def select(path):
    check=0
    image=Image.open(path)
    print(path)
    if image.size[0]<200 or image.size[1]<200:
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
    return check


#main함수 영역
if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    f = open('fashionurl.csv','r',newline='')
    wr=csv.reader(f)
    for i in range(len(wr)):
        deletelist=[]
        url = wr[i][1]
        
        num =i #폴더 번호-해당 번호의 쇼핑몰 url을 의미한다.
        if i==0:
            continue
    
        count=0
        clothes=[]
        if not(os.path.isdir("{}".format(num))):
            os.makedirs(os.path.join("{}".format(num)))
        clothes=show(url)
        download(clothes,num)                     
        godir(clothes,num)
        print(deletelist)
      

        
