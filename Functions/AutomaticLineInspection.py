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

__isStart = False
__isRunning = False
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
    
    # 设置掩码以获取部分图像数据进行判断
    resolution = cam.get_camera_resolution
    __mask = np.zeros(resolution, dtype=np.uint8)
    __mask = cv2.rectangle(__mask, (0, int(resolution[0]*0.75)), (resolution[1], int(resolution[0]*0.8)), 255, thickness=-1)

def exit():
    """退出玩法
    """
    global __isStart, __isRunning
    __isRunning = True

def run(img):
    global __isRunning
    
    if not __isRunning:
        return img
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)

    # 获取掩码部分的数据
    
    
    
    
    # 将掩码叠加在原始图像上返回
    
    return img

