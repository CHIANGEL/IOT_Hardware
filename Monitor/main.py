import time
from typing import Dict
import serial
from yaml import load
from enum import Enum, unique
from .monitor import Monitor
from .request import Request

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from Object_Detection_Deployment.detect_response_process import *


@unique
class Property(Enum):
    Warning = "Warning"
    Temperature = "Temperature"
    Humidity = "Humidity"
    Camera = "Camera"


def load_classes(path):
    """
    加载label信息
    """
    fp = open(path, "r")
    names = fp.read().split("\n")[:-1]
    return names


def main():
    config: Dict
    with open("./config.yaml", 'r') as f:
        config = load(f, Loader)

    monitor = Monitor(config)
    monitor.open()
    req = Request(config)
    img_path = config["image"]["path"]
    img_name = config["image"]["new_name"]
    classes = load_classes(config["classes"])  # 支持的所有质押物 ( 假装是

    while True:
        temperature, humidity, shake = monitor.get_state()
        if shake == 1:
            monitor.shake = 0
        print(req.post_property(Property.Temperature.name, temperature))
        print(req.post_property(Property.Humidity.name, humidity))
        obj_detect_rsp = req.post_object_detect()
        warning = detect_response_process(shake, obj_detect_rsp, classes[int(config["target"])])
        print(req.post_property(Property.Warning, warning))
        print(req.post_picture(Property.Camera, "%s/%s" % (img_path, img_name)))
        monitor.print_state()
        if shake == 1:
            monitor.shake = 0
        time.sleep(int(config["interval"]))


if __name__ == "__main__":
    main()
