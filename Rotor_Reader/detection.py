import cv2
import numpy as np
import img2file
import os

img = cv2.imread('1.png')
print(img.shape)

digits=img[156:188,540:780]

#divide 8
print(digits.shape)

tmp = 30

digit=np.empty([32,30,3,8],dtype=int)     #32=188-156， 30=（780-540）/8

for i in range(8):
    digit[:,:,:,i]=digits[:,i*30:(i+1)*30]
    filename='%s.jpg' %(i+10)
    cv2.imwrite(filename,digit[:,:,:,i])



print(digit.shape)

path='table_cut_img'
files=os.listdir(path)
for file in files:
    if os.path.splitext(file)[1]== '.jpg':
        s=file.split('.')[0]
        img2file.img2txt('table_cut_img/%s'%file,'table_cut_txt/%s.txt'%s)

#detected_digits_whole = ["X", "X", "X", "X", "X", "X", "X", "X"]

#cv2.namedWindow("Image")

#cv2.imshow("Image",digits)

#cv2.waitKey(0)

#cv2.destroyAllWindows()
