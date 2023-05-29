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
    # monitoring_area = binary[__Area[0][1]: __Area[1][1], __Area[0][0]:__Area[1][0]]
    monitoring_area_inv = cv2.bitwise_not(monitoring_area, _)
    contours = cv2.findContours(monitoring_area_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 找出所有外轮廓

    cv2.drawContours(monitoring_area, contours, -1, (120), 3)
    areaMaxContour, value = getAreaMaxContour(contours)  # 找到最大的轮廓


    # tracking(__Area, areaMaxContour)
    # TODO change the other part
    img_center_x = math.fabs((__Area[0][1] + __Area[1][1])/2)
    # img_center_y = math.fabs(__Area[0][1] - __Area[0][1])

    (centerX, centerY), radius = cv2.minEnclosingCircle(
        areaMaxContour)  # 获取最小外接圆
 
    # print(f"centerX: {centerX}, img_center_X:{img_center_x}")
    diff = math.fabs(img_center_x - centerX)
    
    
    # 尝试将这个图像合并到原始图像上来方便看    
    # print(f"x:{centerX}, y:{centerY}")
    cv2.circle(binary, (int(centerX), int(centerY + __Area[0][0])), 1, (127), 3) 
    
    # tracking(__Area, areaMaxContour)
    
    return binary

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
