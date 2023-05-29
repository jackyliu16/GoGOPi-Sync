#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import time
import numpy as np
from MyFunction.config import *
from typing import *

__isStart = False
__isRunning = False
__endingFlags = False # will be using in other ways, not just as bool
__method = method.DETACT
area = []

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

def init(resolution: Tuple[int, int]):
    global area, __isStart, __isRunning, __endingFlags
    import HiwonderSDK.Board as Board
    print("init")
    Board.setPWMServoPulse(1, 1000, 300)
    # CAM = cv2.VideoCapture(0) # resolution = (int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH)))
    area = [
        # (x, y)
        (int(resolution[0]*0.60), 0), 
        (int(resolution[0]*0.80), resolution[1])
    ]
    __isStart = True
    __isRunning = True #TODO
    __endingFlags = False

# from MyFunction.imageProcess import detect_color_item
# from MyFunction.imageProcess import binarization
# from MyFunction.imageProcess import get_monitoring_area 
from MyFunction.imageProcess import *
import MyFunction.montor as montor
def run(img):
    global __isStart, __isRunning, __endingFlags
    global area
    if not __isStart:
        print("error: unstart")
        return img
    montor.init()
    if __isStart and not __isRunning:
        if detect_color_item(img, "red"):
            __isRunning = True
    if __isRunning:

        if __endingFlags:
            import HiwonderSDK.Board as Board
            Board.setBuzzer(1)
            time.sleep(2)
            Board.setBuzzer(0)
            print(time.time() - __endingFlags)
            if time.time() - __endingFlags >= WAITING_TIME:
                reset()
        
        gray = binarization(img)
        monitoring_area = get_monitoring_area(gray)

        (x, y) = get_center_of_maximum_area(monitoring_area)
        # print((x, y))
        add_mark_point(gray, (x, y + area[0][0]))
        cv2.line(gray, (area[0][1], area[0][0]), (area[1][1], area[0][0]), 100, 2)
        cv2.line(gray, (area[0][1], area[1][0]), (area[1][1], area[1][0]), 100, 2)
        # add_mark_point(monitoring_area, (x, y))
        
        montor.move((x, y + area[0][0]))        
        
        # check_if_get_ending_point(monitoring_area)
        if not __endingFlags:
            __endingFlags = time.time() if check_if_get_ending_point(monitoring_area) else None 
        return gray
            
    return img
        

def reset():
    import HiwonderSDK.Board as Board
    Board.setMotor(1, 0)
    Board.setMotor(2, 0)
    for i in range(1, 6):
        Board.setPWMServoPulse(i, 1500, 500)
    sys.exit(0)