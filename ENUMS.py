from enum import Enum, auto

class DIRECTION(Enum):
    IN = 0b1
    OUT = 0b0

class STATE(Enum):
    HIGH = 0b1
    LOW = 0b0