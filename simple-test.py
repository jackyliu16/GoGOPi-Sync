import cv2
import numpy as np
# from Functions.ColorTracking import getAreaMaxContour
from Functions.JackyLab import *

__BinarizationThreshold = 80
__Area = []
def binary_image(frame):
    global resolution, __Area
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, __BinarizationThreshold, 255, cv2.THRESH_BINARY)
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
    (centerX, centerY), radius = cv2.minEnclosingCircle(areaMaxContour)  # 获取最小外接圆
    img_center_y = ((__Area[0][1]+__Area[1][1])/2) 

    # cv2.circle(binary, (centerX, centerY), 10, 120, -1)

    return binary 

if __name__ == "__main__":
    global resolution
    cap = cv2.VideoCapture(0)
    
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    while True:
        ret, frame = cap.read()
        # binary = binary_image(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
