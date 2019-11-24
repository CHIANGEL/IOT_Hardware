import base64
import requests


def _post_(url, data):
    try:
        res = requests.post(url, data)
        if res.status_code != requests.codes.ok:
            print(res)
            return {}
        return res.json()
    except ValueError as ve:
        print(ve)
        return {}


def pack_property(identifier, value):
    return {"device_name": identifier, "value": value}


def pack_picture(identifier, pic):
    return {"device_name": identifier, "picture": pic}


class Request:
    ali_server_base: str
    object_detect_base: str
    car_licence_detect_base: str

    def __init__(self, config):
        self.ali_server_base = config["server"]["ali"]["url"]
        self.object_detect_base = config["server"]["object_detect"]["url"]
        self.car_licence_detect_base = config["server"]["car_licence"]["url"]

    def post_object_detect(self):
        res = requests.post("%s/detect" % self.object_detect_base)
        try:
            data = res.json()
            return data
        except ValueError as ve:
            print(ve)
            return {}

    def post_flush(self):
        return _post_("%s/flush" % self.ali_server_base, {})

    def post_picture(self, identifier, img_path):
        with open(img_path, 'rb') as f:
            data = base64.b64encode(f.read())
        return _post_("%s/flush" % self.ali_server_base, pack_picture(identifier, data))

    def post_property(self, identifier, value):
        return _post_("%s/property" % self.ali_server_base, pack_property(identifier, value))

    def post_licence_plate(self, licence):
        return _post_("%s/plate_number" % self.ali_server_base, {"PlateNumber": licence})
