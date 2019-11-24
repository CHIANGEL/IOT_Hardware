def detect_response_process(is_shaked, response):
    ret = 0
    if is_shaked: # 若发生震动
        ret |= 4
        print("is_shaked! ret = %d\n" % ret)

    if response['success']: # 识别算法调用成功
        print("Request success\n")
        img_result = {}
        for img_i, img_dic in enumerate(response["detections"]):
            if 'new' in img_dic['img_path']: # file-new.jpg的检测结果
                img_result['new'] = img_dic["img_detection"]
            elif 'old' in img_dic['img_path']: # file-old.jpg的检测结果
                img_result['old'] = img_dic["img_detection"]
        if len(img_result['new']) != len(img_result['old']): # 数量都不对了，赶紧报警！
            ret |= 7
            return ret
        
        for new_x1, new_y1, new_x2, new_y2, new_conf, new_cls_conf, new_cls_pred in img_result['new']:
            best_old_x1 = 0
            best_old_y1 = 0
            best_old_x2 = 0
            best_old_y2 = 0
            best_old_conf = 0.0
            best_old_cls_conf = 0.0
            best_old_cls_pred = 0.0
            best_central_distance = inf
            new_central_x = (new_x1 + new_x2) / 2
            new_central_y = (new_y1 + new_y2) / 2
            for old_x1, old_y1, old_x2, old_y2, old_conf, old_cls_conf, old_cls_pred in img_result['old']:
                old_central_x = (old_x1 + old_x2) / 2
                old_central_y = (old_y1 + old_y2) / 2
                central_distance = sqrt((new_central_x - old_central_x) ** 2 + (new_central_y - old_central_y) ** 2)
                if central_distance < best_central_distance:
                    best_central_distance =central_distance
                    best_old_x1 = old_x1
                    best_old_y1 = old_y1
                    best_old_x2 = old_x2
                    best_old_y2 = old_y2
                    best_old_conf = old_conf
                    best_old_cls_conf = old_cls_conf
                    best_old_cls_pred = old_cls_pred
            if best_central_distance > 10:
                ret |= 1
                return ret
    else: # 识别失败，考虑加点动作哦？
        print("Request failed\n")
    return ret