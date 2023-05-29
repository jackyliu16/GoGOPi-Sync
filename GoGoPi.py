#coding=utf-8
import sys
if sys.version_info.major != 3:
    print('Please run this program with python3!')
    sys.exit(0)

import os
if os.geteuid() != 0:
    print('This program must be run as root!')
    sys.exit(0)

import argparse
import cv2
import time
import queue
import threading
import logging
import MjpgServer
import Camera
import RPCServer
import numpy as np
import HiwonderSDK.Board as Board
import HiwonderSDK.Sonar as Sonar
import HiwonderSDK.Misc as Misc
import Functions.Running as Running
import Functions.EmptyFunc as EmptyFunc
import Functions.Avoidance as Avoidance
import Functions.ColorTracking as ColorTracking
import Functions.FaceTracking as FaceTracking
import Functions.FingerDetect as FingerDetect
import Functions.RemoteControl as RemoteControl

HW_DBG = True 
HWSONAR = Sonar.Sonar() #超声波传感器
QUEUE_RPC = queue.Queue(10)
CAM = None

def startGoGoPi():
    global HWEXT, HWSONIC, HW_DBG, CAM
    #
    if HW_DBG == False: #没有加-f 参数，不直接运行玩法需要 rpc 控制，启动 rpc、mjpg 服务器
        threading.Thread(target=RPCServer.startRPCServer,
                     daemon=True).start()  # rpc 服务器
        threading.Thread(target=MjpgServer.startMjpgServer,
                     daemon=True).start()  # mjpg 服务器
    #
    while True:
        time.sleep(0.03)
        # 执行需要在本线程中执行的 RPC 命令
        while True:
            try:
                req, ret = QUEUE_RPC.get(False)
                event, params, *_ = ret
                ret[2] = req(params)  # 执行 RPC 命令
                event.set()
            except:
                break
        #####
        # 执行功能玩法程序：
        try:
            if Running.RunningFunc in Running.FUNCTIONS:
                if CAM.frame is not None:
                    if HW_DBG: #命令行启动玩法，在 x 中显示画面
                        cv2.imshow('frame',  Running.CurrentEXE().run(CAM.frame.copy()))
                        cv2.waitKey(1) 
                    else: #rpc 控制启动玩法，通过 mjpg 服务器显示画面
                        frame = CAM.frame.copy()
                        img = Running.CurrentEXE().run(frame).copy()
                        if Running.RunningFunc == '9':
                            MjpgServer.img_show = np.vstack((img, frame))
                        else:
                            MjpgServer.img_show = frame
                else:
                    MjpgServer.img_show = None
            else:
                CAM.frame = None
        except Exception as e:
            print(e)
            time.sleep(1)
        #####

if __name__ == '__main__':
    print('''
    **********************************************************
    *******功能：所有玩法的集合，可通过不同指令进行调用********
    **********************************************************
    ----------------------------------------------------------
    Official website:http://www.hiwonder.com/
    ----------------------------------------------------------
    以下指令均需在 LX 终端使用，LX 终端可通过 ctrl+alt+t 打开，或点
    击上栏的黑色 LX 终端图标。
    ----------------------------------------------------------
    Usage:
      -f 1 | --启动遥控小车
      -f 2 | --启动颜色跟踪
      -f 3 | --启动人脸跟踪
      -f 4 | --启动手指识别
      -f 5 | --启动自动避障
    ----------------------------------------------------------
    Example #1:
      显示图像，追踪红颜色小球
      python3 GoGoPi.py -f 2 -c red
    Example #2:
      显示图像，追踪绿颜色小球
      python3 GoGoPi.py -f 2 -c green
    Example #3:
      自动避障，指定避障距离为 30cm
      python3 GoGoPi.py -f 5 -t 30
    ----------------------------------------------------------
    Version: --V2.0  2020/07/20
    ----------------------------------------------------------
    Tips:
     * 按下 Ctrl+C 可关闭此次程序运行，若失败请多次尝试！
    ----------------------------------------------------------
    ''')
    Board.setMotor(1, 0)
    Board.setMotor(2, 0)
    Board.setPWMServoPulse(1, 1500)
    Board.setPWMServoPulse(2, 1500)
    HWSONAR.setRGBMode(0)
    HWSONAR.setPixelColor(0, 0)
    HWSONAR.setPixelColor(1, 0)
    #
    Avoidance.HWSONAR = HWSONAR
    ColorTracking.HWSONAR = HWSONAR
    FaceTracking.HWSONAR = HWSONAR
    FingerDetect.HWSONR = HWSONAR
    RPCServer.HWSONAR = HWSONAR
    RPCServer.QUEUE = QUEUE_RPC
    CAM = Camera.Camera()  # 相机读取
    Running.cam = CAM
    #
    logging.basicConfig(level=logging.ERROR)
    #
    #命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--func', help='选择要运行的玩法')
    parser.add_argument('-w', '--wheel',action='store_true', help='人脸追踪时使用轮子')
    parser.add_argument('-c', '--color', default='green', help='设置颜色追踪的目标颜色')
    parser.add_argument('-t', '--threshold', default=20, help='设置超声波避障的距离阈值')
    args = parser.parse_args()
    #
    if args.func is not None: #通过-f 参数选择了要运行的玩法
        HW_DBG = True
        try:
            db = int(args.func)
            if 1 <= db <= 6:
                Running.DisableHeartbeat = True
                Running.loadFunc((db,))
                if db == 2:
                    ColorTracking.setTargetColor((args.color, ))#设置颜色追踪的目标颜色
                if db == 3:
                    if args.wheel is True:
                        FaceTracking.setWheel((1,)) #设置人脸识别启动车身跟随
                elif db == 5:
                    Avoidance.setThreshold((int(args.threshold),)) #设置超声波避障阈值
                else:
                    pass
                Running.startFunc() #启动玩法
            else:
                print("Invalid Function num", db, 1)
                sys.exit(-1)
        except:
            print("Invalid Function num" ,  db, 2)
            sys.exit(-1)
    #
    print(os.getpid())
    try:
        startGoGoPi() #启动运行
    except:
        pass
    finally:
        Board.setMotor(1, 0)
        Board.setMotor(2, 0)
