import os
import sys
import time
import logging
import threading
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import HiwonderSDK as hwsdk
import HiwonderSDK.Board as Board
import Functions.Running as Running
import Functions.lab_adjust as lab_adjust
import Functions.ColorTracking as ColorTracking
import Functions.Avoidance as Avoidance
import Functions.FaceTracking as FaceTracking

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

__RPC_E01 = "E01 - Invalid number of parameter!"
__RPC_E02 = "E02 - Invalid parameter!"
__RPC_E03 = "E03 - Operation failed!"
__RPC_E04 = "E04 - Operation timeout!"
__RPC_E05 = "E05 - Not callable"

HWSONAR = None
QUEUE = None

@dispatcher.add_method
def SetPWMServo(*args, **kwargs):
    ret = (True, (), 'SetPWMServo')
    arglen = len(args)
    if 0 != (arglen % 3):
        return (False, __RPC_E01, 'SetPWMServo')
    try:
        servos = args[0:arglen:3]
        pulses = args[1:arglen:3]
        use_times = args[2:arglen:3]
        for s in servos:
            if s < 1 or s > 6:
                return (False, __RPC_E02, 'SetPWMServo')
        dat = zip(servos, pulses, use_times)
        for (s, p, t) in dat:
            Board.setPWMServoPulse(s, p, t)
    except Exception as e:
        print(e)
        ret = (False, __RPC_E03, 'SetPWMServo')
    return ret

@dispatcher.add_method
def SetBrushMotor(*args, **kwargs):
    ret = (True, (), 'SetBrushMotor')
    arglen = len(args)
    print(args)
    if 0 != (arglen % 2):
        return (False, __RPC_E01, 'SetBrushMotor')
    try:
        motors = args[0:arglen:2]
        speeds = args[1:arglen:2]
        for m in motors:
            if m < 1 or m > 4:
                return (False, __RPC_E02, 'SetBrushMotor')
        dat = zip(motors, speeds)

        for m, s in dat:
            Board.setMotor(m, s)
    except:
        ret = (False, __RPC_E03, 'SetBrushMotor')
    return ret

@dispatcher.add_method
def GetSonarDistance():
    global HWSONAR
    
    ret = (True, 0, 'GetSonarDistance')
    try:
        ret = (True, HWSONAR.getDistance(), 'GetSonarDistance')
    except:
        ret = (False, __RPC_E03, 'GetSonarDistance')
    return ret

@dispatcher.add_method
def GetBatteryVoltage():
    ret = (True, 0, 'GetBatteryVoltage')
    try:
        ret = (True, Board.getBattery(), 'GetBatteryVoltage')
    except Exception as e:
        print(e)
        ret = (False, __RPC_E03, 'GetBatteryVoltage')
    return ret

@dispatcher.add_method
def SetSonarRGBMode(mode = 0):
    global HWSONAR
    
    HWSONAR.setRGBMode(mode)
    return (True, (mode,), 'SetSonarRGBMode')

@dispatcher.add_method
def SetSonarRGB(index, r, g, b):
    global HWSONAR
    
    if index == 0:
        HWSONAR.setPixelColor(0, Board.PixelColor(r, g, b))
        HWSONAR.setPixelColor(1, Board.PixelColor(r, g, b))
    else:
        HWSONAR.setPixelColor(index, (r, g, b))
    return (True, (r, g, b), 'SetSonarRGB')

@dispatcher.add_method
def SetSonarRGBBreathCycle(index, color, cycle):
    global HWSONAR
    
    HWSONAR.setBreathCycle(index, color, cycle)  
    return (True, (index, color, cycle), 'SetSonarRGBBreathCycle')

@dispatcher.add_method
def SetSonarRGBStartSymphony():
    global HWSONAR
    
    HWSONAR.startSymphony()
    return (True, (), 'SetSonarRGBStartSymphony')

def runbymainth(req, pas):
    if callable(req):
        event = threading.Event()
        ret = [event, pas, None]
        QUEUE.put((req, ret))
        count = 0
        #ret[2] =  req(pas)
        while ret[2] is None:
            time.sleep(0.01)
            count += 1
            if count > 200:
                break
        if ret[2] is not None:
            if ret[2][0]:
                return ret[2]
            else:
                return (False, __RPC_E03 + " " + ret[2][1])
        else:
            return (False, __RPC_E04)
    else:
        return (False, __RPC_E05)

@dispatcher.add_method
def SetSonarDistanceThreshold(new_threshold = 30): 
    return runbymainth(Avoidance.setThreshold, (new_threshold,))

@dispatcher.add_method
def GetSonarDistanceThreshold():
    return runbymainth(Avoidance.getThreshold, ())

@dispatcher.add_method
def LoadFunc(new_func = 0):
    return runbymainth(Running.loadFunc, (new_func, ))

@dispatcher.add_method
def UnloadFunc():
    return runbymainth(Running.unloadFunc, ())

@dispatcher.add_method
def StartFunc():
    return runbymainth(Running.startFunc, ())

@dispatcher.add_method
def StopFunc():
    return runbymainth(Running.stopFunc, ())

@dispatcher.add_method
def Heartbeat():
    return runbymainth(Running.doHeartbeat, ())

@dispatcher.add_method
def GetRunningFunc():
    #return runbymainth("GetRunningFunc", ())
    return (True, (0,))

@dispatcher.add_method
def SetTargetTrackingColor(target_color = "red"):
    return runbymainth(ColorTracking.setTargetColor, (target_color, ))

@dispatcher.add_method
def SetFaceTrackingWheel(new_st = 0):
    return runbymainth(FaceTracking.setWheel, (new_st, ))

# 设置颜色阈值
# 参数：颜色 lab
# 例如：[{'red': ((0, 0, 0), (255, 255, 255))}]
@dispatcher.add_method
def SetLABValue(*lab_value):
    #print(lab_value)
    return runbymainth(lab_adjust.setLABValue, lab_value)

# 保存颜色阈值
@dispatcher.add_method
def GetLABValue():
    return (True, lab_adjust.getLABValue()[1], 'GetLABValue')

# 保存颜色阈值
@dispatcher.add_method
def SaveLABValue(color=''):
    return runbymainth(lab_adjust.saveLABValue, (color, ))

@dispatcher.add_method
def HaveLABAdjust():
    return (True, True, 'HaveLABAdjust')

@Request.application
def application(request):
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b
#    print(request.data)
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

def startRPCServer():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    print('rpc')
    run_simple('', 9030, application)

if __name__ == '__main__':
    startRPCServer()
