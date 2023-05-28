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
import JackyLab as lab

__isRunning = False
__isStart = False

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
    global __isStart, __isRunning
    __isStart = True

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
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    
    return img

