from typing import *
import cv2
import math

def getAreaMaxContour(contours):
    """计算最大的 Contour

    Args:
        contours (_type_): 找到的 Contour

    Returns:
        tuple[int, int]: (MaxContour, 最大值)
    """
    # copy from ColorTracking
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = 0.0

    for c in contours:  # 历遍所有轮廓
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            area_max_contour = c
    return area_max_contour, contour_area_max  # 返回最大的轮廓