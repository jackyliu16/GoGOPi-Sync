"""
this is a lab just using by jacky
"""
import math
import cv2
import numpy as np
SPEED_LIMIT = 20

def setBothMotor(speed: int):
    import HiwonderSDK.Board as Board
    """
    using for stop the first motor
    """
    Board.setMotor(1, speed)
    Board.setMotor(2, speed)

from typing import *
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
            if contour_area_temp > 20:  # 只有在面积大于 20，最大面积的轮廓才是有效的，以过滤干扰
                area_max_contour = c
    return area_max_contour, contour_area_max  # 返回最大的轮廓

def setMotorSpeedDiff(speed: int):
    """产生速度差

    Args:
        speed (int): 当想要左边马达相较于右边马达速度提升的时候设定为负，否则为正
    """
    import HiwonderSDK.Board as Board
    montor_l = Board.getMotor(1, speed)
    montor_r = Board.getMotor(2, speed)

    diff = montor_l + montor_r # BC montor_r 是反过来的
    if speed > SPEED_LIMIT:
        print("error: out of the range")
    if diff < SPEED_LIMIT:
        # NOTE 左边增加或者右边增加
        Board.setMotor(1, montor_l + speed) if speed < 0 else Board.setMotor(2,  montor_r - speed)
    else:
        # NOTE 选择二者中相较于 0 最远的
        # TODO untest this funciton
        Board.setMotor(1, montor_l - speed) if diff < 0 else Board.setMotor(2, montor_r + speed)

def buzzer_for_second(second: int) -> None:
    import time
    import HiwonderSDK.Board as Board
    Board.setBuzzer(0)
    time.sleep(second)
    Board.setBuzzer(1)

def diff_speed(motor: int, speed: int) -> None:
    import HiwonderSDK.Board as Board
    print(f"motor {motor} add speed {speed}")
    print(f"1: {Board.getMotor(1)}, 2:{Board.getMotor(2)}")
    if motor == 2:
        print(f"motor {motor} add speed {speed}")
        Board.setMotor(motor, Board.getMotor(motor) - speed)
    else:
        print("add speed")
        Board.setMotor(motor, Board.getMotor(motor) + speed)

# 尝试能否通过这个来影响 diff
def sigmoid(x: float):
    return 1 / ( 1 + np.exp(-x) )
    
def tracking(area, areaMaxContour: tuple):
    # copy from ColorTracking
    import math
    img_center_x = math.fabs(area[0][1] - area[1][1])
    img_center_y = math.fabs(area[0][0] - area[1][0])
    if areaMaxContour is not None:  # 有找到最大面积
        (centerX, centerY), radius = cv2.minEnclosingCircle(
            areaMaxContour)  # 获取最小外接圆
        if radius >= 3:
            # 简易算法
            
            diff = abs(img_center_x - centerX)
            setMotorSpeedDiff(diff)

            # NOTE 需要提前测试
            
            ########pid 处理#########
            #以图像的中心点的 x，y 坐标作为设定的值，以当前 x，y 坐标作为输入#

            # err = abs(img_center_y + 20 - centerY) #计算 y 轴误差，+20 使目标位置处于中心偏下位置
            # if err < 30:
            #     servo1_pid.SetPoint = centerY #误差范围内
            # else:
            #     servo1_pid.SetPoint = img_center_y + 20 

            # servo1_pid.update(centerY) #更新 pid
            # tmp = int(servo1_pulse + servo1_pid.output)
            # tmp = 950 if tmp < 950 else tmp #舵机角度限幅
            # servo1_pulse = 2000 if tmp > 2000 else tmp

            # TODO 需要改造此部分以对 Montor 进行控制
            # err = abs(img_center_x - centerX) #计算 x 轴误差

            # if err < 40:
            #     servo2_pid.SetPoint = 2 * img_center_x - centerX # ‘2*'将左右对应数值反转
            # else:
            #     servo2_pid.SetPoint = img_center_x

            # servo2_pid.update(2 * img_center_x - centerX) #更新 pid
            # tmp = int(servo2_pulse - servo2_pid.output) 
            # tmp = 500 if tmp < 500 else tmp #限幅
            # servo2_pulse = 2500 if tmp > 2500 else tmp

            # NOTE 不对舵机进行任何移动
            # Board.setPWMServoPulse(1, servo1_pulse, 20)  #控制舵机运动
            # Board.setPWMServoPulse(2, servo2_pulse, 20)

            # NOTE 下面的内容无关，不涉及云台运动
            # tmp = 0
            #当舵机位置小于 1300 时，车身的前后运动由云台的俯仰角驱动
            #当舵机位置大于等于 1300 时，车声的前后运动由画面中色块的最小外接圆半径驱动
            # if servo1_pulse < 1300:
            #     if  1050 < servo1_pulse < 1200:
            #         pitch_pid.SetPoint = servo1_pulse
            #     else:
            #         pitch_pid.SetPoint = 1100
            #     pitch_pid.update(servo1_pulse)
            #     tmp = pitch_pid.output
            # else:
            #     pitch_pid.clear()
            #     pitch_pid.SetPoint = servo1_pulse
            #     if 25 < radius < 45:
            #         pitch_pid1.SetPoint = radius
            #     else:
            #         pitch_pid1.SetPoint = 30

            #     if radius > 50: #半径太大时会后退太快，做一个限幅
            #         pitch_pid1.update(50)
            #     else:
            #         pitch_pid1.update(radius)
            #     tmp = -pitch_pid1.output

            # tmp = 100 if tmp > 100 else tmp
            # tmp = -100 if tmp < -100 else tmp
            # base_speed = -tmp
        
            # #车声转向由云台 z 轴偏转来驱动
            # if 1350 < servo2_pulse < 1650:
            #     yaw_pid.clear()
            #     yaw_pid.SetPoint = servo2_pulse
            # else:
            #     yaw_pid.SetPoint = 1500

            # yaw_pid.update(servo2_pulse)
            # tmp = yaw_pid.output
            # tmp = 45 if tmp > 45 else tmp #限幅，车身转向太快摄像头跟不上
            # tmp = -45 if tmp < -45 else tmp
            # direct_speed = tmp

            # TODO 完成车身驱动部分
            # motor1 = base_speed + direct_speed
            # motor1_direct = -1 if motor1 < 0 else 1

            # motor2 = base_speed - direct_speed
            # motor2_direct = -1 if motor2 < 0 else 1

            # motor1 = Misc.map(abs(motor1), 0, 100, 30, 70) #马达在 0～30 的区间扭矩不够，动不了，做个映射
            # motor2 = Misc.map(abs(motor2), 0, 100, 30, 70)
            
            # motor1 = int(motor1_direct * motor1)
            # motor2 = int(motor2_direct * motor2)

            # if -35 < motor1 < 35:
            #     motor1 = 0
            # if -35 < motor2 < 35:
            #     motor2 = 0
            # Board.setMotor(1, motor1) #设置马达速度
            # Board.setMotor(2, motor2)

            # centerX = int(Misc.map(centerX, 0, 320, 0, 640))
            # centerY = int(Misc.map(centerY, 0, 240, 0, 480))
            # radius = int(Misc.map(radius, 0, 320, 0, 640))

            # NOTE 感觉可以去掉，直接通过前面的边缘检测来画图
            # #画面上画出正在追踪的色块
            # cv2.circle(img, (int(centerX), int(centerY)),
            #         int(radius), range_rgb[target_color], 2)
