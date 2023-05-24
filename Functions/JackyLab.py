"""
this is a lab just using by jacky
"""
import HiwonderSDK.Board as Board

def setBothMotor(speed: int):
    """
    using for stop the first motor
    """
    Board.getMotor(0, speed)
    Board.getMotor(1, speed)