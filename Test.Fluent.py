# ensure all depdencies are installed and environment variables set.
import os
#cmd = 'pip install hidapi'
#os.system(cmd)

# Import all required dependecies
import sys
from MCP2221_A import I2C, DigitalInOut, Direction, G0
import time
time.sleep(1)

# Configure USB I2C Click pin G0 as output. 
# G0 is connected to the reset pin of the MCP23018
pin = DigitalInOut(G0)
pin.direction = Direction.OUTPUT

# Configure USB I2C Click I2C Interface
# The I2C interface is used to operate the MCP23018

# Load the G0 pin and the i2c interface into MCP2308
from MCP23018 import MCP23018 , I2C_ADDRESS_RANGE, PORT, State, Direction, PIN, Configuration
mcp23018 = MCP23018(reset_pin = pin, I2C_Address = I2C_ADDRESS_RANGE.ONE)

# pylint: disable=maybe-no-member
(mcp23018
    .reset()
    .wait(1)
    .GPIO.set_value(State.HIGH)
    .GPIO.set_direction(Direction.OUT)
    .wait(1)
    .GPIO.set_value(State.LOW)
    .wait(1)
    .GPIO.set_value(State.HIGH)
    .wait(1)
    .GPIO.Port[PORT.A].set_value(State.LOW)
    .wait(1)
    .GPIO.Port[PORT.B].set_value(State.LOW)
    .wait(1)
    .GPIO.Port[PORT.A].set_value(State.HIGH)
    .wait(1)
    .GPIO.Port[PORT.B].set_value(State.HIGH)
    .wait(1)
    .GPIO.Port[PORT.A]
         .Pin[PIN.GP0].set_value(State.LOW)
         .Pin[PIN.GP1].set_value(State.LOW)
         .Pin[PIN.GP2].set_value(State.LOW)
         .Pin[PIN.GP3].set_value(State.LOW)
         .Pin[PIN.GP4].set_value(State.LOW)
         .Pin[PIN.GP5].set_value(State.LOW)
         .Pin[PIN.GP6].set_value(State.LOW)
         .Pin[PIN.GP7].set_value(State.LOW)
    .exist()
    .GPIO.Port[PORT.B]
         .Pin[PIN.GP0].set_value(State.LOW)
         .Pin[PIN.GP1].set_value(State.LOW)
         .Pin[PIN.GP2].set_value(State.LOW)
         .Pin[PIN.GP3].set_value(State.LOW)
         .Pin[PIN.GP4].set_value(State.LOW)
         .Pin[PIN.GP5].set_value(State.LOW)
         .Pin[PIN.GP6].set_value(State.LOW)
         .Pin[PIN.GP7].set_value(State.LOW)
    .exist()
    .GPIO.Port[PORT.A]
         .Pin[PIN.GP0].set_value(State.HIGH)
         .Pin[PIN.GP1].set_value(State.HIGH)
         .Pin[PIN.GP2].set_value(State.HIGH)
         .Pin[PIN.GP3].set_value(State.HIGH)
         .Pin[PIN.GP4].set_value(State.HIGH)
         .Pin[PIN.GP5].set_value(State.HIGH)
         .Pin[PIN.GP6].set_value(State.HIGH)
         .Pin[PIN.GP7].set_value(State.HIGH)
    .exist()
    .GPIO.Port[PORT.B]
         .Pin[PIN.GP0].set_value(State.HIGH)
         .Pin[PIN.GP1].set_value(State.HIGH)
         .Pin[PIN.GP2].set_value(State.HIGH)
         .Pin[PIN.GP3].set_value(State.HIGH)
         .Pin[PIN.GP4].set_value(State.HIGH)
         .Pin[PIN.GP5].set_value(State.HIGH)
         .Pin[PIN.GP6].set_value(State.HIGH)
         .Pin[PIN.GP7].set_value(State.HIGH))

mcp23018.GPIO.Port[PORT.A].Pin[PIN.GP5].value = State.LOW
mcp23018.GPIO.Port[PORT.B].Pin[PIN.GP5].value = State.LOW
mcp23018.wait(1)
mcp23018.GPIO.Port[PORT.A].Pin[PIN.GP5].value = State.HIGH
mcp23018.GPIO.Port[PORT.B].Pin[PIN.GP5].value = State.HIGH

mcp23018.Configuration.Parameter['BANK'].value = Configuration.BANK.SEPARATE
mcp23018.wait(1)

mcp23018.GPIO.Port[PORT.A].Pin[PIN.GP5].value = State.LOW
mcp23018.GPIO.Port[PORT.B].Pin[PIN.GP5].value = State.LOW
mcp23018.wait(1)
mcp23018.GPIO.Port[PORT.A].Pin[PIN.GP5].value = State.HIGH
mcp23018.GPIO.Port[PORT.B].Pin[PIN.GP5].value = State.HIGH




