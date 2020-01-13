from PIL import Image
import numpy as np
import cv2

img=cv2.imread("photo4.jpg",cv2.IMREAD_COLOR)
x=img.shape
arraylist=[]
widthlist=[]
croplist=[]
count=3
print(x[1])
for i in range(x[1]):
    if (img[:,i]>235).sum() == 3*x[0]:
        widthlist.append(i)

for i in range(len(widthlist)-1):
    if (widthlist[i+1]-widthlist[i])>50:
        croplist.append(widthlist[i])
        croplist.append(widthlist[i+1])
if len(croplist)>1:
    img=img[0:x[0],croplist[0]:croplist[len(croplist)-1]]    
x=img.shape
for i in range(x[0]):
    if (img[i,:] > 235).sum() == 3*x[1]:
        arraylist.append(i)

if len(arraylist)>1:
    for i in range(len(arraylist)-1):
        if (arraylist[i+1]-arraylist[i])>50:
            
            cropimage=img[arraylist[i]:arraylist[i+1],0:x[1]]
            cv2.imwrite("{}.png".format(count),cropimage)
            count+=1




