import time
from typing import Dict
import serial
from yaml import load
from enum import Enum, unique
from monitor import Monitor
from request import Request

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


@unique
class Property(Enum):
    Warning = "Warning"
    Temperature = "Temperature"
    Humidity = "Humidity"
    Camera = "Camera"


def main():
    config: Dict
    with open("./config.yaml", 'r') as f:
        config = load(f, Loader)

    monitor = Monitor(config)
    monitor.open()
    req = Request(config)
    img_path = config["image"]["path"]
    img_name = config["image"]["new_name"]
    while True:
        temperature, humidity, shake = monitor.get_state()
        
        print(req.post_property(Property.Temperature.name, temperature))
        print(req.post_property(Property.Humidity.name, humidity))
        #
        # obj_detect_rsp = req.post_object_detect()
        warning = shake

        print(req.post_property(Property.Warning.name, str(bin(warning))[-3:]))
        print("post image %s/%s" % (img_path, img_name))
        print(req.post_picture(Property.Camera.name, "%s/%s" % (img_path, img_name)))
        monitor.print_state()
        if shake == 1:
            monitor.shake = 0
        time.sleep(int(config["interval"]))


if __name__ == "__main__":
    main()
