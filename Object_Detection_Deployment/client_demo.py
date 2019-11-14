import requests

def load_classes(path):
    """
    加载label信息
    """
    fp = open(path, "r")
    names = fp.read().split("\n")[:-1]
    return names

PyTorch_REST_API_URL = "http://127.0.0.1:32442/detect"

'''
API参数：
 - save_output_images：表示是否要将Bounding Box画在图片上并保存至某一个目录中
                 需要注意的是这个保存操作耗时相对较多，谨慎使用
                 注意，post参数传递以字符串形式进行，必须传入True或"True"，传入 1 之类的并不支持
                 default value: False
                 
返回值：
 - success：
    +type: bool
    +remarks: 指示本次调用是否成功
 - detections:
    +type: list
    +remarks: 存储所有的object detection的结果，目标目录有几个文件，这个列表就有几个条目
    +element info: 每一个条目都是一个字典dictionary:
      * img_path: 
        + type: string
        + remarks: 对应该条目图片的具体路径
               注意！因为json的原因，字符串前后有'['和']'的多余字符，交给用户自己处理（Worse is better）
      * img_detection:
        + type: 二维列表
        + remarks: 每一个子列表有七个float数（x1, y1, x2, y2, conf, cls_conf, cls_pred），具体可见下面的使用
               注意，conf到目前为止没啥用处，置信度用cls_conf表示
'''
# r = requests.post(PyTorch_REST_API_URL, data={'save_output_images': True}).json()

response = requests.post(PyTorch_REST_API_URL).json()
            
classes = load_classes("./data/coco.classes")  # 解析对应的class名称

if response['success']:
    print("Request success\n")
    for img_i, img_dic in enumerate(response["detections"]):
        
        print("(%d) Image: '%s'" % (img_i, img_dic["img_path"]))
        
        if img_dic["img_detection"] is not None:
            
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in img_dic["img_detection"]:
                
                box_w = x2 - x1 # Bounding Box的宽度
                box_h = y2 - y1 # Bounding Box的高度

                print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf))
                print("\t  (x1, y1) = (%.2f, %.2f)" % (x1, y1))
                print("\t  (x2, y2) = (%.2f, %.2f)" % (x2, y2))
                print("\t  width = %.2f, height = %.2f" % (box_w, box_h))

else:
    print("Request failed")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    