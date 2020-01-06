# ensure all depdencies are installed and environment variables set.
import os
#cmd = 'pip install adafruit-blinka hidapi'
#os.system(cmd)
os.environ["BLINKA_MCP2221"] = "1"

# Import all required dependecies
import sys
import board
import digitalio
import busio
import time
time.sleep(1)

# Configure USB I2C Click pin G0 as output. 
# G0 is connected to the reset pin of the MCP23018
pin = digitalio.DigitalInOut(board.G0)
pin.direction = digitalio.Direction.OUTPUT

# Configure USB I2C Click I2C Interface
# The I2C interface is used to operate the MCP23018
i2c = busio.I2C(board.SCL, board.SDA)

# Load the G0 pin and the i2c interface into MCP2308
from MCP23018 import MCP23018, State, Direction
mcp23018 = MCP23018(reset_pin = pin, i2c_interface = i2c)

# Fluent API Example
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
    .GPIO.Ports["A"].set_value(State.LOW)
.wait(1)
    .GPIO.Ports["B"].set_value(State.LOW)
.wait(1)
    .GPIO.Ports["A"].set_value(State.HIGH)
.wait(1)
    .GPIO.Ports["B"].set_value(State.HIGH)
.wait(1)
    .GPIO.Ports["A"]
        .Pin["GP0"].set_value(State.LOW)
        .Pin["GP1"].set_value(State.LOW)
        .Pin["GP2"].set_value(State.LOW)
        .Pin["GP3"].set_value(State.LOW)
        .Pin["GP4"].set_value(State.LOW)
        .Pin["GP5"].set_value(State.LOW)
        .Pin["GP6"].set_value(State.LOW)
        .Pin["GP7"].set_value(State.LOW)
.exist()
    .GPIO.Ports["B"]
        .Pin["GP0"].set_value(State.LOW)
        .Pin["GP1"].set_value(State.LOW)
        .Pin["GP2"].set_value(State.LOW)
        .Pin["GP3"].set_value(State.LOW)
        .Pin["GP4"].set_value(State.LOW)
        .Pin["GP5"].set_value(State.LOW)
        .Pin["GP6"].set_value(State.LOW)
        .Pin["GP7"].set_value(State.LOW)
.exist()
    .GPIO.Ports["A"]
        .Pin["GP0"].set_value(State.HIGH)
        .Pin["GP1"].set_value(State.HIGH)
        .Pin["GP2"].set_value(State.HIGH)
        .Pin["GP3"].set_value(State.HIGH)
        .Pin["GP4"].set_value(State.HIGH)
        .Pin["GP5"].set_value(State.HIGH)
        .Pin["GP6"].set_value(State.HIGH)
        .Pin["GP7"].set_value(State.HIGH)
.exist()
    .GPIO.Ports["B"]
        .Pin["GP0"].set_value(State.HIGH)
        .Pin["GP1"].set_value(State.HIGH)
        .Pin["GP2"].set_value(State.HIGH)
        .Pin["GP3"].set_value(State.HIGH)
        .Pin["GP4"].set_value(State.HIGH)
        .Pin["GP5"].set_value(State.HIGH)
        .Pin["GP6"].set_value(State.HIGH)
        .Pin["GP7"].set_value(State.HIGH))