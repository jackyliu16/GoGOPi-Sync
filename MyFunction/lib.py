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
            # if contour_area_temp > 20:  # 只有在面积大于 20，最大面积的轮廓才是有效的，以过滤干扰
            area_max_contour = c
    return area_max_contour, contour_area_max  # 返回最大的轮廓

def getMotor(idx: int) -> int:
    """get the abs speed of motor
    """
    import HiwonderSDK.Board as Board
    return Board.getMotor(idx) if idx % 2 == 0 else -Board.getMotor(idx)

def setMotor(idx: int, speed: int):
    """set motor idx into abs speed
    """
    import HiwonderSDK.Board as Board
    Board.setMotor(idx, speed)

def setBothMotor(speed: int):
    """setting both motor into same speed
    """
    setMotor(1, speed)
    setMotor(2, speed)
