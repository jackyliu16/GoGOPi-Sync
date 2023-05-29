from MyFunction.lib import *
import HiwonderSDK.Board as Board
Board.setBuzzer(0)
setBothMotor(0)
print(f"{getMotor(1)}, {getMotor(2)}")
