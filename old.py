from enum import Enum

class direction(Enum):
    OUT = 0x00
    IN = 0xff

class state(Enum):
    HIGH = 0xff
    LOW = 0x00

# MCP23018.GPIO.set_direction(Direction.OUT)
# Should set GPIO of both Port A and Port B as Output
# MCP23018.GPIO.Port(A).set_direction(Direction.OUT)
# Should set GPIO of Port A as Output
# MCP23018.GPIO.Port(A).Pin(0).set_direction(Direction.OUT)
# Should set GPIO Pin 0 of Port A as Output

class Pin:
    def __init__(self, id, address):
        self.id = id
        self.value = state.LOW # Initialize with Logic-Low
        self.direction = direction.IN # Initialize as Input
        self.address = address

class MCP23018:
    I2C_ADDRESS = 0x20
    
    class port(Enum):
        A = 0x00
        B = 0x01
    
    class register(Enum): 
        IODIRA = 0x00
        IODIRB = 0x01
        IPOLA = 0x02
        IPOLB = 0x03
        GPINTENA = 0x04
        GPINTENB = 0x05
        DEFVALA = 0x06
        DEFVALB = 0x07
        INTCONA = 0x08
        INTCONB = 0x09
        IOCONA = 0x0a
        IOCONB = 0x0b
        GPPUA = 0x0c
        GPPUB = 0x0d
        INTFA = 0x0e
        INTFB = 0x0f
        INTCAPA = 0x10
        INTCAPB = 0x11
        GPIOA = 0x12
        GPIOB = 0x13
        OLATA = 0x14
        OLATB = 0x15

    class pins(Enum):
        GPB0 = 3
        GPB1 = 4
        GPB2 = 5
        GPB3 = 6
        GPB4 = 7
        GPB5 = 8
        GPB6 = 9
        GPB7 = 10
        GPA0 = 20
        GPA1 = 21
        GPA2 = 22
        GPA3 = 23
        GPA4 = 34
        GPA5 = 35
        GPA6 = 36
        GPA7 = 37
    
    def __init__(self, reset_pin, i2c):
        self.reset_pin = reset_pin
        self.i2c = i2c
        self.reset()

    def reset(self):
        self.reset_pin.value = True
        self.reset_pin.value = False
        self.reset_pin.value = True


    def configure_gpio(self, port, direction):
        if port == self.port.A :
            register = self.register.IODIRA
        if port == self.port.B :
            register = self.register.IODIRB
        self.writeTo(register, direction.value)
    
    def set_gpio(self, port, state):
        if port == self.port.A:
            register = self.register.GPIOA
        if port == self.port.B:
            register = self.register.GPIOB
        self.writeTo(register, state.value)

    def set_gpio_pin(self, port, pin, state):
        if port == self.port.A:
            self.set_gpio_port_a_pin(pin, state)
        if port == self.port.B:
            self.set_gpio_port_b_pin(pin, state)


    def set_gpio_port_a_pin(self, pin, state):
        state_new = (state.value & pin.address)

        register = self.register.OLATA
        state_current  = self.readFrom(register)
        state_current = (state_current & ~pin.address)
        
        data = (state_new | state_current)

        register = self.register.GPIOA
        self.writeTo(register, data)
    
    def set_gpio_port_b_pin(self, pin, state):
        state_new = (state.value & pin.address)

        register = self.register.OLATB
        state_current  = self.readFrom(register)
        state_current = (state_current & ~pin.address)
        
        data = (state_new | state_current)

        register = self.register.GPIOB
        self.writeTo(register, data)

    def writeTo(self, register, data):
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register.value, data]))
    
    def readFrom(self, register):
        data = bytearray(1)
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register.value]), stop=False)
        self.i2c.readfrom_into(self.I2C_ADDRESS, data)
        data = int.from_bytes(data,"big")
        return data


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
mcp23018 = MCP23018(reset_pin = pin, i2c = i2c)

# Configure MCP23018 Port A and Port B Pins as output
mcp23018.configure_gpio(mcp23018.port.A, direction.OUT)
mcp23018.configure_gpio(mcp23018.port.B, direction.OUT)

# Wait one second then toggle port a and b pins state, three times
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, state.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, state.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, state.LOW)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, state.LOW)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, state.HIGH)
time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, state.HIGH)

# Change the status of a particular pin
GPA0 = Pin("GP0",0b00000001)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA0, state.LOW)
GPA1 = Pin("GP1",0b00000010)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA1, state.LOW)
GPA2 = Pin("GP2",0b00000100)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA2, state.LOW)
GPA3 = Pin("GP3",0b00001000)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA3, state.LOW)
GPA4 = Pin("GP4",0b00010000)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA4, state.LOW)
GPA5 = Pin("GP5",0b00100000)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA5, state.LOW)
GPA6 = Pin("GP6",0b01000000)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA6, state.LOW)
GPA7 = Pin("GP7",0b10000000)
mcp23018.set_gpio_pin(mcp23018.port.A, GPA7, state.LOW)

time.sleep(1)
mcp23018.set_gpio(mcp23018.port.A, state.HIGH)

# Change the status of a particular pin
GPB0 = Pin("GP0",0b00000001)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB0, state.LOW)
GPB1 = Pin("GP1",0b00000010)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB1, state.LOW)
GPB2 = Pin("GP2",0b00000100)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB2, state.LOW)
GPB3 = Pin("GP3",0b00001000)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB3, state.LOW)
GPB4 = Pin("GP4",0b00010000)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB4, state.LOW)
GPB5 = Pin("GP5",0b00100000)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB5, state.LOW)
GPB6 = Pin("GP6",0b01000000)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB6, state.LOW)
GPB7 = Pin("GP7",0b10000000)
mcp23018.set_gpio_pin(mcp23018.port.B, GPB7, state.LOW)

time.sleep(1)
mcp23018.set_gpio(mcp23018.port.B, state.HIGH)