import threading

from .handle import *


class Monitor:
    th_device: str
    th_baud: int

    img_old: str
    img_new: str
    img_path: str

    th_: serial.Serial

    shake_thread: threading.Thread

    temperature: float
    humidity: float
    shake: int

    def __init__(self, config):
        self.th_device = config["th"]["device"]
        self.th_baud = int(config["th"]["baud"])
        self.img_new = config["image"]["new_name"]
        self.img_old = config["image"]["old_name"]
        self.img_path = config["image"]["path"]
        self.temerature = 0.0
        self.humidity = 0.0
        self.shake = 0


    def open(self):
        self.th_ = open_th(self.th_device, self.th_baud)
        open_sk()
        self.shake_thread = threading.Thread(target=self.read_sk_)
        self.shake_thread.start()

    def get_state(self):
        self.temperature, self.humidity = read_th(self.th_)
        # self.shake set by shake_thread
        return self.temperature, self.humidity, self.shake

    def print_state(self):
        print("##############   current state   ###############")
        print("#            temperature\t %f" % self.temperature)
        print("#            humidity   \t %f" % self.humidity)
        print("#            shake      \t %d" % self.shake)

    def read_sk_(self):
        while True:
            if read_sk() == 1:
                self.shake = 1
