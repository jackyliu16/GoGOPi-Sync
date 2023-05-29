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
BINARIZATION_LIMIT = 80
