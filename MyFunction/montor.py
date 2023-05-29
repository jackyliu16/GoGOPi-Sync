from HiwonderSDK.PID import PID
from typing import *
from MyFunction.lib import setMotor, getMotor, setBothMotor
from MyFunction.config import ADD_SPEED, BASE_SPEED

motor_pid = PID(P=0.03, I=0.05, D=0.0010)
# motor_pid = PID(P=0.01, I=0.01, D=0.008)

def init():
    setBothMotor(BASE_SPEED)

def move(point: Tuple[int, int]) -> None:
    from MyFunction.run import area
    # TODO 需要明确这个地方针对的是mon还是别的
    # img_center_x = (area[1][0] + area[0][0]) / 2
    img_center_y = (area[0][1] + area[1][1]) / 2
    x, y = point
    err = abs(img_center_y - x)
    if err < 30:
        motor_pid.setPoint = x
    else:
        motor_pid.SetPoint = img_center_y
    
    motor_pid.update(x)
    tmp = motor_pid.output
    print(f"tmp: {tmp}")
    setMotor(1, int(getMotor(1) - tmp * ADD_SPEED))
    setMotor(2, int(getMotor(2) + tmp * ADD_SPEED))
    
