#!/usr/bin/python3
# coding=utf8
import os
import sys
import cv2
import math
import time
import datetime
import threading
import queue
from enum import Enum
import numpy as np
from MyFunction.config import *
from typing import *

__isStart = False
__isRunning = False
__method = method.DETACT
area = []

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

def init(resolution: Tuple[int, int]):
    global area, __isStart, __isRunning 
    print("init")
    # CAM = cv2.VideoCapture(0) # resolution = (int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH)))
    area = [
        # (x, y)
        (int(resolution[0]*0.70), 0), 
        (int(resolution[0]*0.80), resolution[1])
    ]
    __isStart = True
    #TODO 
    __isRunning = True

# from MyFunction.imageProcess import detect_color_item
# from MyFunction.imageProcess import binarization
# from MyFunction.imageProcess import get_monitoring_area 
from MyFunction.imageProcess import *
def run(img):
    global __isStart, __isRunning
    global area
    if not __isStart:
        print("error: unstart")
        return img
    
    if __isStart:
        if detect_color_item(img, "red"):
            __isRunning = True
    if __isRunning:
        gray = binarization(img)
        monitoring_area = get_monitoring_area(gray)

        (x, y) = get_center_of_maximum_area(monitoring_area)
        print(f"({x}, {y})")
        print(f"[{x + area[0][0]}, {y}]")
        add_mark_point(gray, (x, y + area[0][0]))
        cv2.line(gray, (area[0][1], area[0][0]), (area[1][1], area[0][0]), 100, 2)
        cv2.line(gray, (area[0][1], area[1][0]), (area[1][1], area[1][0]), 100, 2)
        # add_mark_point(monitoring_area, (x, y))

        
        return gray 
    return img
        