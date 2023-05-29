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
import Functions.JackyLab as lab

range_rgb = {
    'red': (255, 0, 255),
    'blue': (255, 255,),
    'green': (0, 255, 255),
    'black': (0, 0, 0),
}

# env virable
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

import Camera
def start():
    """准备运行玩法
    """
    print("start")
    global __isStart, __isRunning
    global __mask, __cam
    __isStart = True
    __method = method.DETACT
    
    # 设置掩码以获取部分图像数据进行判断
    resolution = (480, 640)
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

#设置目标颜色
def setTargetColor(target_color_new = ('red', )):
    global target_color
    target_color = target_color_new[0]
    set_rgb(target_color)
    return (True, ())

import yaml_handle
lab_data = None
def load_config():
    global lab_data
    
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)
target_color = "red"
def run(img):
    global __isRunning
    
    if not __isRunning:
        return img
    
    if __method == method.DETACT:
        print("run")
        if target_color == "":
            return img
        frame_resize = cv2.resize(img, (320, 240), interpolation=cv2.INTER_NEAREST)
        img_center_x = frame_resize.shape[:2][1]/2  # 获取缩小图像的宽度值的一半
        img_center_y = frame_resize.shape[:2][0]/2

        frame_lab = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2LAB)  # 将图像转换到 LAB 空间
        frame_mask = cv2.inRange(frame_lab,
                                (lab_data[target_color]['min'][0],
                                lab_data[target_color]['min'][1],
                                lab_data[target_color]['min'][2]),
                                (lab_data[target_color]['max'][0],
                                lab_data[target_color]['max'][1],
                                lab_data[target_color]['max'][2]))  #对原图像和掩模进行位运算    

        opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # 开运算
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE,np.ones((6, 6), np.uint8))  # 闭运算
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓

        areaMaxContour, maxvalue = lab.getAreaMaxContour(contours)  # 找到最大的轮廓

        print(maxvalue)
        
    else:
        pass
        
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)

    # # 获取掩码部分的数据
    # monitoring_area = thresh[__Area[0][1]: __Area[1][1], __Area[0][0]:__Area[1][0]]

    # contours = cv2.findContours(monitoring_area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓
    # areaMaxContour = lab.getAreaMaxContour(contours)  # 找到最大的轮廓


    # # 调用 tracking 自动控制马达
    # lab.tracking(__Area, areaMaxContour)
        
    # 将掩码叠加在原始图像上返回
    
    return img




def set_rgb(color):
    if color == "red":
        Board.RGB.setPixelColor(0, Board.PixelColor(255, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(255, 0, 0))
        Board.RGB.show()
    elif color == "green":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 255, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 255, 0))
        Board.RGB.show()
    elif color == "blue":
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 255))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 255))
        Board.RGB.show()
    else:
        Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
        Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))
        Board.RGB.show()