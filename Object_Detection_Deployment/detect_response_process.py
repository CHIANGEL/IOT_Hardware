import math

def load_classes(path):
    """
    加载label信息
    """
    fp = open(path, "r")
    names = fp.read().split("\n")[:-1]
    return names


def compute_iou(rec1, rec2):
    # 计算两个矩形的面积
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
 
    # 计算矩形面积之和
    sum_area = S_rec1 + S_rec2
 
    # 计算四个差集的面积
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])
 
    # 判断两个矩形是否有交集
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect))*1.0

def detect_response_process(is_shaked, response, detect_target):
    # ret: 3bit(is_shaked, is_moved, amount_changed)
    # 若amount changed为真，is_moved必为真
    print('\nTarget to detect: %s\n' % detect_target)
    ret = 0
    if is_shaked: # 若发生震动
        ret |= 4
        print("Object is shaked-> Set ret to: %d\n" % ret)
    
    classes = load_classes("./data/coco.classes")  # 解析对应的class名称
    if response['success']: # 识别算法调用成功
        print("Request success\n")
        img_result = {}
        img_result['new'] = []
        img_result['old'] = []
        for img_i, img_dic in enumerate(response["detections"]):
            #print(type(img_dic['img_path'][0]))
            #print('img_i: %d, img_path: %s' % (img_i, img_dic['img_path']))
            if 'new' in img_dic['img_path'][0]: # file-new.jpg的检测结果
                print('Find file-new.jpg! img_i: %d, img_path: %s\n' % (img_i, img_dic['img_path'][0]))
                for item in img_dic["img_detection"]:
                    if classes[int(item[6])] == detect_target:
                        img_result['new'].append(item)
            elif 'old' in img_dic['img_path'][0]: # file-old.jpg的检测结果
                print('Find file-old.jpg: img_i: %d, img_path: %s\n' % (img_i, img_dic['img_path'][0]))
                for item in img_dic["img_detection"]:
                    if classes[int(item[6])] == detect_target:
                        img_result['old'].append(item)
        if len(img_result['new']) != len(img_result['old']): # 数量都不对了，赶紧报警！
            print('ALERT! Amount has chaned!\n')
            ret |= 7
            return ret
        # 数量对上后，开始匹配计算移动误差
        for new_x1, new_y1, new_x2, new_y2, new_conf, new_cls_conf, new_cls_pred in img_result['new']:
            best_old_x1 = 0
            best_old_y1 = 0
            best_old_x2 = 0
            best_old_y2 = 0
            best_old_conf = 0.0
            best_old_cls_conf = 0.0
            best_old_cls_pred = 0.0
            best_central_distance = 1000000000000.0
            new_central_x = (new_x1 + new_x2) / 2
            new_central_y = (new_y1 + new_y2) / 2
            for old_x1, old_y1, old_x2, old_y2, old_conf, old_cls_conf, old_cls_pred in img_result['old']:
                old_central_x = (old_x1 + old_x2) / 2
                old_central_y = (old_y1 + old_y2) / 2
                central_distance = math.sqrt((new_central_x - old_central_x) ** 2 + (new_central_y - old_central_y) ** 2)
                if central_distance < best_central_distance:
                    best_central_distance =central_distance
                    best_old_x1 = old_x1
                    best_old_y1 = old_y1
                    best_old_x2 = old_x2
                    best_old_y2 = old_y2
                    best_old_conf = old_conf
                    best_old_cls_conf = old_cls_conf
                    best_old_cls_pred = old_cls_pred
            if best_central_distance > 50:
                ret |= 2
                return ret
    else: # 识别失败，考虑加点动作哦？
        print("Request failed\n")
    return ret