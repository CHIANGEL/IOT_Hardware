# IOT_Hardware
王东老师 信息系统工程 大作业 硬件部分

## Object_Detection_Depolyment: 目标检测模块

注: Object_Detection_Depolyment/weights目录用于存放训练好的yolo模型，但是太大了没有上传到git，需要私聊

## Monitor: 传感器检测模块

主要分为 摄像头、温湿度、震动 三个监测部分。其中温湿度及 

## Car_Plate_Recognition: 车牌识别（TA提供）

使用了训练好的开源库Hyperlpr，但是效果差强人意，以及因为opencv-python版本问题没有部署到开发板上

## Rotor_Reader: 表器识别（TA提供）

识别算法流程：
  1. 假设摄像头固定，因此拍摄的表器的数字在图片中的像素位置也是固定的，因此detection.py可以把图片中固定位置（写死的）的图块截取出来、转换成黑白图、以01的形式存在.txt文件中
  2. 对每一个截取出来的单个数字的.txt文件，采用KNN算法进行匹配，但是准确率不高（毕竟只是KNN）

## Dockerfile usage
外层的Dockerfile是为了创建arm64上的conda，内层的Dockerfile是为了使用conda装模型需要的环境。
