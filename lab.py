import time
from Functions.JackyLab import *
import HiwonderSDK.Board as Board

def test_speed():
    Board.setBuzzer(0)
    setBothMotor(60)
    setMotorSpeedDiff(20) #  
    time.sleep(2)

    setMotorSpeedDiff(20) # -100, 60
    time.sleep(2)
    
    setMotorSpeedDiff(-20) # -80, 60
    time.sleep(2)

    setMotorSpeedDiff(-20) # -60, 60
    time.sleep(2)
    setMotorSpeedDiff(-20) # -60, 60
    time.sleep(2)
    setMotorSpeedDiff(-20) # -60, 60
    time.sleep(2)

def test_add_speed():
    setBothMotor(40)
    
    # buzzer_for_second(1)
    diff_speed(1, 40)
    time.sleep(5)
    #  
    # buzzer_for_second(1)
    diff_speed(2, 20)
    time.sleep(5)

    # buzzer_for_second(1)
    diff_speed(1, 20)
    time.sleep(5)
    
    # buzzer_for_second(1)
    diff_speed(2, -20)
    time.sleep(5)


if __name__ == "__main__":
    import HiwonderSDK.Board as Board
    test_speed()
    # Board.setMotor(2, 80)
    time.sleep(2)
    
    setBothMotor(0)