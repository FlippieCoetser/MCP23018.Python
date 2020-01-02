# ensure all depdencies are installed and environment variables set.
import os
cmd = 'pip install adafruit-blinka hidapi'
os.system(cmd)
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

# Load Libraries
from MCP23018 import MCP23018, Direction, State

# Load the G0 pin and the i2c interface into MCP2308
mcp23018 = MCP23018(reset_pin = pin, i2c = i2c)

# Configure MCP23018 Port A and Port B Pins as output
mcp23018.configure_gpio(mcp23018.port.A, Direction.OUT)
mcp23018.configure_gpio(mcp23018.port.B, Direction.OUT)

# Wait one second then toggle gpio pins state, three times
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, State.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, State.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, State.LOW)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, State.LOW)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, State.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, State.HIGH)


