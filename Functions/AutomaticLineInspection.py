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
    global isRunning
    isRunning = True

def exit():
    """退出玩法
    """
    global isRunning

    isRunning = False

def run(img):
    return img

