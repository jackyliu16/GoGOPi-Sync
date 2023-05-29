range_rgb = {
    'red': (255, 0, 255),
    'blue': (255, 255,),
    'green': (0, 255, 255),
    'black': (0, 0, 0),
}

from enum import Enum
class method(Enum):
    DETACT = 1
    FLLOW = 2

# DEFINE
DETACT_SIZE_LIMIT = 1000
BINARIZATION_LIMIT = 100
ADD_SPEED = 7   #2
BASE_SPEED = 80 #30

MONITORING_AREA = (
    (0.60, 0.0),
    (0.80, 1.0),
)

# END POINT DETACT
WAITING_TIME = 1
ENDING_SIZE_LIMIT = 7000 
END_DETACT_AREA = (
    (0.4, 0.0),
    (0.5, 1.0),
)