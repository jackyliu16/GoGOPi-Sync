from MyFunction.config import *
import cv2
import yaml_handle
import numpy as np
import math
from MyFunction import lib
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

