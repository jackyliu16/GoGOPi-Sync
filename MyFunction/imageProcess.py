from MyFunction.config import *
import MyFunction.lib as lib
import cv2
import yaml_handle
import numpy as np
import math
from typing import *

lab_data = None
def detect_color_item(img: np.ndarray, target_color: str) -> bool:
    """if detect color max than DETACT_LIMIT the true
    """
    from MyFunction.config import DETACT_SIZE_LIMIT
    lab_data = yaml_handle.get_yaml_data(yaml_handle.lab_file_path)
    
    frame_resize = cv2.resize(img, (320, 240), interpolation=cv2.INTER_NEAREST)

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

    areaMaxContour, maxvalue = lib.getAreaMaxContour(contours)  # 找到最大的轮廓

    return maxvalue > DETACT_SIZE_LIMIT

def binarization(img: np.ndarray) -> np.ndarray:
    """binarization and return image
    """
    from MyFunction.config import BINARIZATION_LIMIT
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary =  cv2.threshold(gray, BINARIZATION_LIMIT, 255, cv2.THRESH_BINARY)
    return binary

def get_monitoring_area(img: np.ndarray) -> np.ndarray:
    """using the area env viriable to shrink the area and return it 
    """
    from MyFunction.run import area
    monitoring_area = img[area[0][0]:area[1][0], area[0][1]: area[1][1]]
    return monitoring_area

def add_mark_point(img: np.ndarray, point: Tuple[int, int]) -> np.ndarray:
    """add a mark point into image

    Args:
        point (Tuple[int, int]): (x, y) 
    """
    cv2.circle(img, (int(point[0]), int(point[1])), 1, 127, 10)

def get_center_of_maximum_area(img: np.ndarray) -> Tuple[int, int]:
    """get the center of the largest region(min peripheral circle) in the image.
    """
    img_INV = cv2.bitwise_not(img) # whiled but neccessary
    contours = cv2.findContours(img_INV, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓
    areaMaxContour, value = lib.getAreaMaxContour(contours)  # 找到最大的轮廓

    (centerX, centerY), radius = cv2.minEnclosingCircle(areaMaxContour)  # 获取最小外接圆
    
    return (centerX, centerY)
