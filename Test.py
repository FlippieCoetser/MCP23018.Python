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
mcp23018 = MCP23018(reset_pin = pin, i2c = i2c)

# GPIO Level 
# Traditional API
mcp23018.reset()
mcp23018.wait(1)
mcp23018.GPIO.value = State.HIGH
mcp23018.GPIO.direction = Direction.OUT
mcp23018.wait(1)
mcp23018.GPIO.value = State.LOW
mcp23018.wait(1)
mcp23018.GPIO.value = State.HIGH

# Fluent API
# pylint: disable=maybe-no-member
(mcp23018
    .reset()
    .wait(1)
    .GPIO.set_value(State.HIGH)
    .GPIO.set_direction(Direction.OUT)
    .wait(1)
    .GPIO.set_value(State.LOW)
    .wait(1)
    .GPIO.set_value(State.HIGH))

# Port Level
# Traditional API
mcp23018.reset()
mcp23018.wait(1)
mcp23018.GPIO.Ports["A"].value = State.HIGH
mcp23018.GPIO.Ports["B"].value = State.HIGH
mcp23018.GPIO.Ports["A"].direction = Direction.OUT
mcp23018.GPIO.Ports["B"].direction = Direction.OUT
mcp23018.GPIO.Ports["A"].value = State.LOW
mcp23018.wait(1)
mcp23018.GPIO.Ports["B"].value = State.LOW
mcp23018.wait(1)
mcp23018.GPIO.Ports["A"].value = State.HIGH
mcp23018.wait(1)
mcp23018.GPIO.Ports["B"].value = State.HIGH

# Fluent API
(mcp23018
    .reset()
    .wait(1)
    .GPIO.Ports["A"].set_value(State.HIGH)
    .GPIO.Ports["B"].set_value(State.HIGH)
    .GPIO.Ports["A"].set_direction(Direction.OUT)
    .GPIO.Ports["B"].set_direction(Direction.OUT)
    .GPIO.Ports["A"].set_value(State.LOW)
    .wait(1)
    .GPIO.Ports["B"].set_value(State.LOW)
    .wait(1)
    .GPIO.Ports["A"].set_value(State.HIGH)
    .wait(1)
    .GPIO.Ports["B"].set_value(State.HIGH))
