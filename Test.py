# ensure all depdencies are installed and environment variables set.
import os
#cmd = 'pip install hidapi'
#os.system(cmd)

# Import all required dependecies
import sys
from MCP2221_A import I2C, DigitalInOut, Direction, G0

import time
time.sleep(1)

# Configure MCP2221 pin G0 as output. 
# G0 is connected to the reset pin of the MCP23018
pin = DigitalInOut(G0)
pin.direction = Direction.OUTPUT

# Import the MCP23018 Library and ENUMS
from MCP23018 import MCP23018 , PORT, PIN, STATE, DIRECTION, PARAMETERS, PARAMETER

# Load the G0 pin and the i2c interface into MCP2308
mcp23018 = MCP23018(RESET_Pin = pin, I2C_Interface=I2C)

# Initialize
mcp23018.reset()
mcp23018.wait(1)

#Configure GPIO at OUTPUT
mcp23018.GPIO.value = STATE.HIGH
mcp23018.GPIO.direction = DIRECTION.OUT
mcp23018.wait(1)

# Set GPIO Low and High
mcp23018.GPIO.value = STATE.LOW
mcp23018.wait(1)
mcp23018.GPIO.value = STATE.HIGH
mcp23018.wait(1)

# Set PORT.A and PORT.B Low and High
mcp23018.GPIO.port[PORT.A].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].value = STATE.LOW
mcp23018.wait(1)
mcp23018.GPIO.port[PORT.A].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].value = STATE.HIGH
mcp23018.wait(1)

# Set PIN.GP0 - GP7 Low and High
mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP1].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP2].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP3].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP4].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP5].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP6].value = STATE.LOW
mcp23018.GPIO.port[PORT.A].pin[PIN.GP7].value = STATE.LOW

mcp23018.GPIO.port[PORT.B].pin[PIN.GP0].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP1].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP2].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP3].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP4].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP6].value = STATE.LOW
mcp23018.GPIO.port[PORT.B].pin[PIN.GP7].value = STATE.LOW
    
mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP1].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP2].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP3].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP4].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP5].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP6].value = STATE.HIGH
mcp23018.GPIO.port[PORT.A].pin[PIN.GP7].value = STATE.HIGH

mcp23018.GPIO.port[PORT.B].pin[PIN.GP0].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP1].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP2].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP3].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP4].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP6].value = STATE.HIGH
mcp23018.GPIO.port[PORT.B].pin[PIN.GP7].value = STATE.HIGH
mcp23018.wait(1)

# Set and Get GPIO PIN
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.LOW
print("MCP23018 GPIO - Read PORT.B PIN.GP5: ", mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value)
mcp23018.wait(1)
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.HIGH
print("MCP23018 GPIO - Read PORT.B PIN.GP5: ", mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value)
mcp23018.wait(1)

# Set and Get Configuration and Test
print("MCP23018 CONFIG - Read bank: ", mcp23018.Configuration.bank)
mcp23018.Configuration.bank = PARAMETERS[PARAMETER.BANK].SEPARATE
print("MCP23018 CONFIG - Read bank: ", mcp23018.Configuration.bank)
mcp23018.wait(1)
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.LOW
mcp23018.wait(1)
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].value = STATE.HIGH
mcp23018.wait(1)



