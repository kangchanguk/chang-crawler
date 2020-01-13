from selenium import webdriver
from requests import get
import urllib.request
import os
from PIL import Image
from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()

myFile=open('kang.txt','r')
cnt = 7
while True:
    if myFile.readline()=="":
        break
    cnt += 1
    url=myFile.readline()
    browser = webdriver.Chrome("chromedriver.exe")

    browser.get(url)
    a= browser.find_elements_by_tag_name("img")
    for i in range(len(a)):
        if "htt" in a[i].get_attribute("src"):
            print(a[i].get_attribute("src"))
            urllib.request.urlretrieve(a[i].get_attribute("src"),"images/{}chang{}.png".format(cnt,i))
            urllib.request.urlretrieve(a[i].get_attribute("src"),"notext/{}chang{}.png".format(cnt,i))
            image=Image.open("images/{}chang{}.png".format(cnt,i))
            image1=Image.open("notext/{}chang{}.png".format(cnt,i))
            path="notext/{}chang{}.png".format(cnt,i)
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            mage = vision.types.Image(content=content)

            response = client.text_detection(image=mage)
            texts = response.text_annotations

            clothesline=""
            for text in texts:
                clothesline+=text.description

            if image1.size[0]<300:
                image1.close()
                os.remove("notext/{}chang{}.png".format(cnt,i))
            else:
                if len(clothesline)>1:
                    image1.close()
                    os.remove("notext/{}chang{}.png".format(cnt,i))
            
            if image.size[0]<300:
                image.close()
                os.remove("images/{}chang{}.png".format(cnt,i))

    browser.close()


       

