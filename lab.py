import time
from Functions.JackyLab import *
import HiwonderSDK.Board as Board

def test_speed():
    Board.setBuzzer(0)
    setBothMotor(0)

    buzzer_for_second(2)
    setMotorSpeedDiff(5)  # 5,  0
    time.sleep(5)

    buzzer_for_second(2)
    setMotorSpeedDiff(-5) # 5， -5
    time.sleep(5)

    buzzer_for_second(2)
    setMotorSpeedDiff(30) # 35，-5
    time.sleep(5)

    buzzer_for_second(2)
    setMotorSpeedDiff(-30) # 5, -5
    time.sleep(5)
    
    buzzer_for_second(2)
    setMotorSpeedDiff(-30) # 5, -40
    time.sleep(5)

def test_add_speed():
    setBothMotor(0)
    
    # buzzer_for_second(1)
    diff_speed(1, 40)
    time.sleep(5)
    #  
    # buzzer_for_second(1)
    # diff_speed(2, 20)
    # time.sleep(5)

    # buzzer_for_second(1)
    # diff_speed(1, 20)
    # time.sleep(5)
    
    # buzzer_for_second(1)
    # diff_speed(2, -20)
    # time.sleep(5)


if __name__ == "__main__":
    import HiwonderSDK.Board as Board
    test_add_speed()

    
    setBothMotor(0)