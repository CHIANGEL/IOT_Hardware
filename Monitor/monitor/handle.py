#!/usr/bin/python3

import serial
import wiringpi as wpi


SEND_MSG = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xc4, 0x0b]


def __th_transfer(hbyte, lbyte):
    data = float((hbyte << 8) + lbyte) / 10

    if hbyte >= (1 << 7):
        return data - (1 << 8)
    else:
        return data


def __th_parity(buf):
    try:
        assert (buf.__len__() == 9)
        assert (buf[0] == 0x01)
        assert (buf[1] == 0x03)
        assert (buf[2] == 0x04)
        humidity = __th_transfer(buf[3], buf[4])
        temperature = __th_transfer(buf[5], buf[6])
        return humidity, temperature
    except AssertionError as ae:
        print(ae)


def open_th(device: str, baud: int):
    th_ = serial.Serial(device, baud)
    if not th_.isOpen():
        print("%s open failed!" % device)
        return None
    return th_


def read_th(th_: serial.Serial):
    th_.write(SEND_MSG)
    res = th_.read(9)
    humidity, temperature = __th_parity(res)
    return temperature, humidity


def open_sk():
    wpi.wiringPiSetup()
    wpi.pinMode(1, 0)


def read_sk():
    return int(wpi.digitalRead(1) == 0)

