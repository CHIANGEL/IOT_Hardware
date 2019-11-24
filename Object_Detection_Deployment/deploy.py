from __future__ import division

from models import *
from utils.utils import *
from utils.datasets import *

import os
import sys
import time
import datetime
import argparse

from PIL import Image

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

import flask

'''
 全局变量的定义：
 - app：flask库部署需要
 - model：Yolo模型，从./weights/yolov3.weights中读取
 - device：是否能够使用gpu，不确定开发板上是否有cuda驱动
 - opt：存储本次运行的server的各项参数
'''

app = flask.Flask(__name__)
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
opt = None

def load_model():
    """
     加载模型至全局变量model中
    """
    global model
    global opt
    model = Darknet(opt.model_def, img_size=opt.img_size).to(device)
    model.load_darknet_weights(opt.weights_path)
    model.eval() # 启动 evaluation 模式

@app.route("/detect", methods=["post"])
def detect_object():
    global opt
        
    response_data = {"success": False} # 这就是要返回的对象
    
    # 提取post参数
    save_output_images = flask.request.form.get('save_output_images')
    print("\nPOST argument:")
    print("\t+ save_output_images: %s\n" % save_output_images)
    
    dataloader = DataLoader(
        ImageFolder(opt.image_folder, img_size=opt.img_size),
        batch_size=opt.batch_size,
        shuffle=False,
        num_workers=opt.n_cpu,
    )

    classes = load_classes(opt.class_path)  # 解析对应的class名称

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    imgs = []  # imgs存储每一张图片的路径
    img_detections = []  # 存储对应路径的图片的探测结果
    response_data["detections"] = list()
    
    # 开始 Detection
    print("Start object detection:")
    prev_time = time.time()
    for batch_i, (img_paths, input_imgs) in enumerate(dataloader):
        input_imgs = Variable(input_imgs.type(Tensor))

        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, opt.conf_thres, opt.nms_thres)

        imgs.extend(img_paths)
        img_detections.extend(detections)
        tmp = {"img_path": img_paths, "img_detection": detections[0].cpu().numpy().tolist()}
        response_data["detections"].append(tmp)

        current_time = time.time()
        inference_time = datetime.timedelta(seconds=current_time - prev_time)
        prev_time = current_time
        print("\t+ Batch %d, Inference Time: %s" % (batch_i, inference_time))
    
    # 将bounding box画在图上并保存
    if save_output_images == "True":
        print("\nSaving images:")

        os.makedirs("output", exist_ok=True) # 标记的输出图片将被存放在./output文件夹中

        # 决定Bounding Box的颜色
        cmap = plt.get_cmap("tab20b")
        colors = [cmap(i) for i in np.linspace(0, 1, 20)]

        # 开始画Bounding Box并保存
        for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):

            print("(%d) Image: '%s'" % (img_i, path))

            # 创建plot与底图
            img = np.array(Image.open(path))
            plt.figure()
            fig, ax = plt.subplots(1)
            ax.imshow(img)

            # 画出Bounding Box并标上 label名
            if detections is not None:
                detections = rescale_boxes(detections, opt.img_size, img.shape[:2])
                unique_labels = detections[:, -1].cpu().unique()
                n_cls_preds = len(unique_labels)
                bbox_colors = random.sample(colors, n_cls_preds)
                for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

                    print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))

                    box_w = x2 - x1
                    box_h = y2 - y1

                    color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
                    bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor="none")
                    ax.add_patch(bbox)
                    plt.text(
                        x1,
                        y1,
                        s=classes[int(cls_pred)],
                        color="white",
                        verticalalignment="top",
                        bbox={"color": color, "pad": 0},
                    )

            # 保存一张画好的图片
            plt.axis("off")
            plt.gca().xaxis.set_major_locator(NullLocator())
            plt.gca().yaxis.set_major_locator(NullLocator())
            filename = path.split("/")[-1].split(".")[0]
            plt.savefig(f"output/{filename}.png", bbox_inches="tight", pad_inches=0.0)
            plt.close()
    
    response_data["success"] = True
    return flask.jsonify(response_data)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_folder", type=str, default="data/samples", help="path to dataset")
    parser.add_argument("--model_def", type=str, default="config/yolov3.cfg", help="path to model definition file")
    parser.add_argument("--weights_path", type=str, default="weights/yolov3.weights", help="path to weights file")
    parser.add_argument("--class_path", type=str, default="data/coco.classes", help="path to class label file")
    parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    parser.add_argument("--deployIP", type=str, default="0.0.0.0", help="ip address to be depokloyed")
    parser.add_argument("--deployPORT", type=int, default=32442, help="port to be deployed")
    opt = parser.parse_args()
    print(opt)
    
    load_model()
    app.run(host=opt.deployIP, port=opt.deployPORT)
