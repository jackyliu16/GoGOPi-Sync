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
import numpy as np
import JackyLab as lab


# env virable
from Running import cam
from enum import Enum

class method(Enum):
    DETACT = 1
    FLLOW = 2

__isStart = False
__isRunning = False
__method = method.DETACT
__Area = []
__BinarizationThreshold = 80

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


def reset():
    """重置到初始状态
    """
    lab.setBothMotor(0)

def init():
    """初始化玩法
    """
    return None

def start():
    """准备运行玩法
    """
    global cam
    global __isStart, __isRunning
    global __mask
    __isStart = True
    __method = method.DETACT
    
    # 设置掩码以获取部分图像数据进行判断
    resolution = cam.get_camera_resolution
    __mask = np.zeros(resolution, dtype=np.uint8)
    # __mask = cv2.rectangle(__mask, (0, int(resolution[0]*0.75)), (resolution[1], int(resolution[0]*0.8)), 255, thickness=-1)
    __Area = [
        # (宽度，长度)
        (0, int(resolution[0]*0.75)),
        (resolution[1], int(resolution[0]*0.8))
    ]

def exit():
    """退出玩法
    """
    global __isStart, __isRunning
    __isRunning = True

def run(img):
    global __isRunning
    
    if not __isRunning:
        return img
    
    if __method == method.DETACT:
        pass
    else:
        pass
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)

    # 获取掩码部分的数据
    monitoring_area = thresh[__Area[0][1]: __Area[1][1], __Area[0][0]:__Area[1][0]]

    contours = cv2.findContours(monitoring_area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓
    areaMaxContour = lab.getAreaMaxContour(contours)  # 找到最大的轮廓

    # 调用 tracking 自动控制马达
    lab.tracking(__Area, areaMaxContour)
        
    
    
    
    # 将掩码叠加在原始图像上返回
    
    return img

