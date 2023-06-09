#!/usr/bin/python3
# coding=utf8
import MyFunction.montor as montor
from MyFunction.imageProcess import *
import sys
import cv2
import time
import numpy as np
from MyFunction.config import *
from typing import *

__isStart = False
__isRunning = False
__endingFlags = False  # will be using in other ways, not just as bool
__method = method.DETACT
area = []
camera_size = ()

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


from MyFunction.lib import mapping
def init(resolution: Tuple[int, int]):
    global area, camera_size, __isStart, __isRunning, __endingFlags
    import HiwonderSDK.Board as Board
    print("init")
    Board.setPWMServoPulse(1, 1000, 300)
    # CAM = cv2.VideoCapture(0) # resolution = (int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH)))
    # area = [
    #     # (x, y)
    #     (int(resolution[0]*0.60), 0),
    #     (int(resolution[0]*0.80), resolution[1])
    # ]
    camera_size = resolution
    area = mapping(MONITORING_AREA)

    __isStart = True
    # __isRunning = True  # TODO
    __endingFlags = False

from MyFunction.lib import setBuzzerForSecond
# from MyFunction.imageProcess import detect_color_item
# from MyFunction.imageProcess import binarization
# from MyFunction.imageProcess import get_monitoring_area
def run(img):
    global __isStart, __isRunning, __endingFlags
    global area
    if not __isStart:
        print("error: unstart")
        return img
    if __isStart and not __isRunning:
        if detect_color_item(img, "red"):
            __isRunning = time.time()
    if __isRunning and time.time() - __isRunning > 4:
    # if __isRunning:
        montor.init()
        if __endingFlags:
            import HiwonderSDK.Board as Board
            Board.setBuzzer(1)
            if time.time() - __endingFlags >= WAITING_TIME:
                reset()

        gray = binarization(img)
        monitoring_area = get_monitoring_area(gray, MONITORING_AREA)

        (x, y) = get_center_of_maximum_area(monitoring_area)
        # print((x, y))
        add_mark_point(gray, (x, y + area[0][0]))
        cv2.line(gray, (area[0][1], area[0][0]),
                 (area[1][1], area[0][0]), 100, 2)
        cv2.line(gray, (area[0][1], area[1][0]),
                 (area[1][1], area[1][0]), 100, 2)
        # add_mark_point(monitoring_area, (x, y))

        montor.move((x, y + area[0][0]))

        # check_if_get_ending_point(monitoring_area)
        # TODO
        if not __endingFlags:
            pass
            __endingFlags = time.time() if check_if_get_ending_point(get_monitoring_area(gray, END_DETACT_AREA)) else None 

        return gray
    return img


def reset():
    import HiwonderSDK.Board as Board
    Board.setMotor(1, 0)
    Board.setMotor(2, 0)
    Board.setBuzzer(0)
    for i in range(1, 6):
        Board.setPWMServoPulse(i, 1500, 500)
    sys.exit(0)
