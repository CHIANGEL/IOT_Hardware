#导入包
from hyperlpr import *
#导入OpenCV库
import cv2
#读入图片
print('demo1.png')
image = cv2.imread("demo1.png")

res = HyperLPR_PlateRecogntion(image)

for item in res:
    if item[1] > 0.9:
        print(item)

