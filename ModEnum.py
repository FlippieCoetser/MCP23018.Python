from enum import Enum, auto

class EnumWithDocstring(Enum):
    def __new__(cls, value, doc=None):
        member = object.__new__(cls)
        member._value_ = value
        member.__doc__ = doc
        return member

Parameters = {
    'ONE': EnumWithDocstring(
        value = 'Options',
        names = [
            ('SEPARATE', (0b1, 'test docstring')),
            ('SEQUENTIAL', 0b0)
        ]
    )
}

print(Parameters['ONE'].SEPARATE.__doc__)

#python -m pydoc -w MCP23018_2



# Left(d,q) -> d << q
# Right(d,q) -> d >> q
# Mask(d, b) -> d & ~b 
# Mask(d, b) -> d & ~(0b1 << b) 
# Unmask(d, b) -> (d << b) & (0b1 << bit)
# Value(d, ENUM) -> ENUM(d)

# READ BIT
# A = Left(0b1, bit)
# B = current & A
# C = Right(B, bit)
# D = Value(C, ENUM)

# READ BIT
# shiftLeft = 0b1 << bit
# current = register
# value = (current & shiftLeft) >> bit
# return ENUM(value)

# WRITE BIT
# A = Left(0b1, bit)
# B = Mask(current, A)
# C = Left(data, bit)
# D = C & A
# E = ( B | D )
# register = E

# WRITE BIT
# shiftLeft = 0b1 << bit
# current = register & ~(shiftLeft)
# value = (config << bit) & shiftLeft
# value = ( value | current)
# register = value

# pylint: disable=maybe-no-member
# (mcp23018
#     .reset()
#     .wait(1)
#     .GPIO.set_value(State.HIGH)
#     .GPIO.set_direction(Direction.OUT)
#     .wait(1)
#     .GPIO.set_value(State.LOW)
#     .wait(1)
#     .GPIO.set_value(State.HIGH)
#     .wait(1)
#     .GPIO.Port[PORT.A].set_value(State.LOW)
#     .wait(1)
#     .GPIO.Port[PORT.B].set_value(State.LOW)
#     .wait(1)
#     .GPIO.Port[PORT.A].set_value(State.HIGH)
#     .wait(1)
#     .GPIO.Port[PORT.B].set_value(State.HIGH)
#     .wait(1)
#     .GPIO.Port[PORT.A]
#          .Pin[PIN.GP0].set_value(State.LOW)
#          .Pin[PIN.GP1].set_value(State.LOW)
#          .Pin[PIN.GP2].set_value(State.LOW)
#          .Pin[PIN.GP3].set_value(State.LOW)
#          .Pin[PIN.GP4].set_value(State.LOW)
#          .Pin[PIN.GP5].set_value(State.LOW)
#          .Pin[PIN.GP6].set_value(State.LOW)
#          .Pin[PIN.GP7].set_value(State.LOW)
#     .exist()
#     .GPIO.Port[PORT.B]
#          .Pin[PIN.GP0].set_value(State.LOW)
#          .Pin[PIN.GP1].set_value(State.LOW)
#          .Pin[PIN.GP2].set_value(State.LOW)
#          .Pin[PIN.GP3].set_value(State.LOW)
#          .Pin[PIN.GP4].set_value(State.LOW)
#          .Pin[PIN.GP5].set_value(State.LOW)
#          .Pin[PIN.GP6].set_value(State.LOW)
#          .Pin[PIN.GP7].set_value(State.LOW)
#     .exist()
#     .GPIO.Port[PORT.A]
#          .Pin[PIN.GP0].set_value(State.HIGH)
#          .Pin[PIN.GP1].set_value(State.HIGH)
#          .Pin[PIN.GP2].set_value(State.HIGH)
#          .Pin[PIN.GP3].set_value(State.HIGH)
#          .Pin[PIN.GP4].set_value(State.HIGH)
#          .Pin[PIN.GP5].set_value(State.HIGH)
#          .Pin[PIN.GP6].set_value(State.HIGH)
#          .Pin[PIN.GP7].set_value(State.HIGH)
#     .exist()
#     .GPIO.Port[PORT.B]
#          .Pin[PIN.GP0].set_value(State.HIGH)
#          .Pin[PIN.GP1].set_value(State.HIGH)
#          .Pin[PIN.GP2].set_value(State.HIGH)
#          .Pin[PIN.GP3].set_value(State.HIGH)
#          .Pin[PIN.GP4].set_value(State.HIGH)
#          .Pin[PIN.GP5].set_value(State.HIGH)
#          .Pin[PIN.GP6].set_value(State.HIGH)
#          .Pin[PIN.GP7].set_value(State.HIGH))

