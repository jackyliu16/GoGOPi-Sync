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
__Area = []
__BinarizationThreshold = 80

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

def init(resolution: Tuple[int, int]):
    global __Area, __isStart, __isRunning 
    print("init")
    # CAM = cv2.VideoCapture(0) # resolution = (int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH)))
    __Area = [
        # (x, y)
        (int(resolution[0]*0.70), 0), 
        (int(resolution[0]*0.80), resolution[1])
    ]
    __isStart = True
    __isRunning = False

from MyFunction.imageProcess import detect_color_item
from MyFunction.imageProcess import binarization
def run(img):
    global __isStart, __isRunning
    global __Area
    if not __isStart:
        print("error: unstart")
        return img
    
    if __isStart:
        if detect_color_item(img, "red"):
            __isRunning = True
    if __isRunning:
        gray = binarization(img)
        print(type(gray))
        return gray
    
    
    return img
        