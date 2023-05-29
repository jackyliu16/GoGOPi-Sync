import cv2
import numpy as np
# from Functions.ColorTracking import getAreaMaxContour
import HiwonderSDK.Board as Board
import HiwonderSDK.PID as PID
import HiwonderSDK.Misc as Misc
from HiwonderSDK.PID import PID
from Functions.JackyLab import *

__BinarizationThreshold = 80
__Area = []
servo1_pid = PID(P=0.5, I=0.052, D=0.035)  # pid 初始化 #上下
servo2_pid = PID(P=0.45, I=0.052, D=0.05)  # pid 初始化 #左右
pitch_pid = PID(P=0.1, I=0.01, D=0.01) #车身前后
pitch_pid1 = PID(P=0.08, I=0.01, D=0.01)
yaw_pid = PID(P=0.01, I=0.01, D=0.008) #车身左右
servo1_pulse = 1500
servo2_pulse = 1500
pitch_speed = 0
yaw_speed = 0
target_color = ""
# 
def binary_image(frame):
    global resolution, __Area
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)
    __mask = np.zeros(resolution, dtype=np.uint8)
    # rectangle_mask = (__mask, resolution)
    # __mask = cv2.rectangle(__mask, (int(resolution[0] * 0.75), 0), (int(resolution[0] * 0.80), resolution[1]), (255))
    __mask = cv2.rectangle(__mask, (0, int(resolution[0]*0.75)), (resolution[1], int(resolution[0]*0.8)), 255, thickness=-1)

    # mask = cv2.bitwise_not(__mask, None)
    # masked_img = cv2.bitwise_and(binary, binary, mask=__mask)

    __Area = [
        # (x, y)
        (int(resolution[0]*0.70), 0), 
        (int(resolution[0]*0.80), resolution[1])
    ]
    # print(binary.shape)
    monitoring_area = binary[__Area[0][0]:__Area[1][0], __Area[0][1]: __Area[1][1]]
    
    contours = cv2.findContours(monitoring_area, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓

    cv2.drawContours(monitoring_area, contours, -1, (120), 3)
    areaMaxContour, maxsize = getAreaMaxContour(contours)  # 找到最大的轮廓

    (centerX, centerY), radius = cv2.minEnclosingCircle(
            areaMaxContour)  # 获取最小外接圆
    img_center_x = ((__Area[0][0]+__Area[0][1])/2) 
    print(img_center_x, centerX)
    diff = math.fabs(img_center_x - centerX)

    print(diff)

    return monitoring_area 

if __name__ == "__main__":
    global resolution
    cap = cv2.VideoCapture(0)
    
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    while True:
        ret, frame = cap.read()
        binary = binary_image(frame)
        cv2.imshow('frame', binary)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
