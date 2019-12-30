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

# Load the G0 pind and the i2c interface into MCP2308
from MCP23018 import MCP23018
mcp23018 = MCP23018(reset_pin = pin, i2c = i2c)

# Configure MCP23018 Port A Pins as output
mcp23018.configure_port_a()

# Wait one second and toggle the Port A Pins state, three times
time.sleep(1)
mcp23018.set_port_a_high()
time.sleep(1)
mcp23018.set_port_a_low()
time.sleep(1)
mcp23018.set_port_a_high()



