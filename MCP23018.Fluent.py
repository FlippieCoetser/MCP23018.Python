from enum import Enum, auto
from MCP2221_A import I2C as i2c
import time

class I2C:
    def __init__(self, device):
        self.device = device
        self.Interface = i2c()

    def write_to(self, register, data):
        print("Write")
        print("Register: ", register)
        print("Address: ", register.value)
        print("Data:  ", data)
        print(" ")
        self.Interface.writeto(self.device.I2C_Address.value, bytes([register.value, data]))
        return

    def read_from(self, register):
        data = bytearray(1)
        self.Interface.writeto(self.device.I2C_Address.value, bytes([register.value]))
        self.Interface.readfrom_into(self.device.I2C_Address.value, data)
        data = int.from_bytes(data,"big")
        print("Read")
        print("Register: ", register)
        print("Address: ", register.value)
        print("Data: ", data)
        print(" ")
        return data

class Direction(Enum):
    IN = 0b1
    OUT = 0b0

class State(Enum):
    HIGH = 0b1
    LOW = 0b0

class I2C_ADDRESS_RANGE(Enum):
    """
    MCP23018 I2C Address is configurable via an analog input on ADDR pin.
    A total of 8 addresses is available and configurable via a voltage devider circuit.
    Setting ADDR = VDD will set the I2C Address to 0x27 (0b100111)
    Setting the ADDR = VSS will set the I2C Address to 0x20 (0b100000)
    See MCP23018 datasheet Figure 1-2 and Figure 1-3 for more details.
    """
    ONE = 0x20
    TWO = 0x21
    THREE = 0x22
    FOUR = 0x23
    FIVE = 0x24
    SIX = 0x25
    SEVEN = 0x26
    EIGHT = 0x27

class BANK(Enum):
    """
    Memory Banks are controlled via bit 8 for IOCON Regsiter 
    """
    ZERO = 0b0
    ONE = 0b1

class BLOCK(Enum):
    A = 'A'
    B = 'B'

class PORT(Enum):
    A = 'A'
    B = 'B'

class PIN(Enum):
    GP0 = 'GP0'
    GP1 = 'GP1'
    GP2 = 'GP2'
    GP3 = 'GP3'
    GP4 = 'GP4'
    GP5 = 'GP5'
    GP6 = 'GP6'
    GP7 = 'GP7'
# ---------------------------------

class Address:
    Registers = None
    I2C = None
    def __init__(self, registers, i2c):
        self.Registers = registers
        self.I2C = i2c

    read = lambda self, address: self.I2C.read_from(address)
    write = lambda self, address, data: self.I2C.write_to(address, data)

    @property
    def IODIR(self):
        """
        I/O DIRECTION REGISTER: Controls the direction of the data I/O
        """
        return self.read(self.Registers.IODIR)  
    @IODIR.setter
    def IODIR(self, direction):
        self.write(self.Registers.IODIR, direction)
    
    @property
    def IPOL(self):
        """
        INPUT POLIRITY REGISTER: Configure the polarity of GPIO Port
        """
        return self.read(self.Registers.IPOL)       
    @IPOL.setter
    def IPOL(self, polarity):
        self.write(self.Registers.IPOL, polarity.value)

    @property
    def GPINTEN(self):
        """
        INTERRUPT-ON-CHANGE CONTROL REGISTER: Controls the interrupt-on-change feature of each pin of Port
        """
        return self.read(self.Registers.GPINTEN)    
    @GPINTEN.setter
    def GPINTEN(self, interrupt_on_change):
        self.write(self.Registers.GPINTEN, interrupt_on_change.value)
    
    @property
    def DEFVAL(self):
        """
        DEFAULT COMPARE REGISTER FOR INTERRUPT-ON-CHANGE: Configure default comparison value of the interrupt-on-change of Port
        """
        return self.read(self.Registers.DEFVAL)    
    @DEFVAL.setter
    def DEFVAL(self, value):
        self.write(self.Registers.DEFVAL, value)

    @property
    def INTCON(self):
        """
        INTERRUPT CONTROL REGISTER: Control how the associated pin value is compared for the interrupt-on-change of Port
        """ 
        return self.read(self.Registers.INTCON)     
    @INTCON.setter
    def INTCON(self, interrupt_on_change_control):
        self.write(self.Registers.INTCON, interrupt_on_change_control.value)
    
    @property
    def IOCON(self):
        """
        I/O EXPANDER CONFIGURATION: Configures the device
        """
        return self.read(self.Registers.IOCON)    
    @IOCON.setter
    def IOCON(self, data): 
        self.write(self.Registers.IOCON, data)

    @property
    def GPPU(self):
        """
        PULL-UP RESISTOR CONFIGURATION REGISTER: Controls the pull-up resistors for port A pins
        """
        return self.read(self.Registers.GPPU)   
    @GPPU.setter
    def GPPU(self, resistor):
        self.write(self.Registers.GPPU, resistor.value)

    @property
    def INTF(self):
        """
        INTERRUPT FLAG REGISTER: Reflects the interrupt condition on any interrupt enabled pins
        """
        return self.read(self.Registers.INTF)      
    @INTF.setter
    def INTF(self, data):
        raise Exception("INTF is a read-only register")

    @property
    def INTCAP(self):
        """
        INTERRUPT CAPTURE REGISTER: Captures the GPIO port value at time of Interrupt
        """
        return self.read(self.Registers.INTCAP)    
    @INTCAP.setter
    def INTCAP(self, data):
        raise Exception("INTCAP is a read-only register")
    
    @property
    def GPIO(self):
        """
        PORT REGISTER: The GPIO Register reflects the value on port
        """
        return self.read(self.Registers.GPIO)     
    @GPIO.setter
    def GPIO(self, data):
        self.write(self.Registers.GPIO, data)

    @property
    def OLAT(self):
        """
        OUTPUT LATCH REGISTER: Provides access to the ouput latches of the port
        """
        return self.read(self.Registers.OLAT)      
    @OLAT.setter
    def OLAT(self, data): 
        self.write(self.Registers.OLAT, data)
   
class Register:
    Port = {}
    """
    Register.ADDRESSES[BANK.ZERO][PORT.A].GPIO
    """
    ADDRESSES = {
        BANK.ZERO: {
            PORT.A: Enum(
                value = 'Address',
                names = [
                    ('IODIR', 0x00),
                    ('IPOL' , 0x02),
                    ('GPINTEN', 0x04),
                    ('DEFVAL', 0x06),
                    ('INTCON', 0x08),
                    ('IOCON', 0x0a),
                    ('GPPU', 0x0c),
                    ('INTF', 0x0e),
                    ('INTCAP', 0x10),
                    ('GPIO', 0x12),
                    ('OLAT', 0x14)
                ]
            ),
            PORT.B: Enum(
                value = 'Address',
                names = [
                    ('IODIR', 0x01),
                    ('IPOL' , 0x03),
                    ('GPINTEN', 0x05),
                    ('DEFVAL', 0x07),
                    ('INTCON', 0x09),
                    ('IOCON', 0x0b),
                    ('GPPU', 0x0d),
                    ('INTF', 0x0f),
                    ('INTCAP', 0x11),
                    ('GPIO', 0x13),
                    ('OLAT', 0x15)
                ]
            )
        },
        BANK.ONE: {
            PORT.A: Enum(
                value = 'Address',
                names = [
                    ('IODIR', 0x00),
                    ('IPOL' , 0x01),
                    ('GPINTEN', 0x02),
                    ('DEFVAL', 0x03),
                    ('INTCON', 0x04),
                    ('IOCON', 0x05),
                    ('GPPU', 0x06),
                    ('INTF', 0x07),
                    ('INTCAP', 0x08),
                    ('GPIO', 0x09),
                    ('OLAT', 0x0a)
                ]
            ),
            PORT.B: Enum(
                value = 'Address',
                names = [
                    ('IODIR', 0x10),
                    ('IPOL' , 0x11),
                    ('GPINTEN', 0x12),
                    ('DEFVAL', 0x13),
                    ('INTCON', 0x14),
                    ('IOCON', 0x15),
                    ('GPPU', 0x16),
                    ('INTF', 0x17),
                    ('INTCAP', 0x18),
                    ('GPIO', 0x19),
                    ('OLAT', 0x1a)
                ]
            )
        }
    }
    Bank = BANK.ZERO
    """
    Default Memory Bank after Reset is BANK.ZERO = 0
    """
    def __init__(self, device):
        self.I2C = device.I2C
        self.load_ports()
    
    def load_ports(self):
        for port in PORT:
            registers = Register.ADDRESSES[self.Bank][port]
            self.Port[port] = Address(registers, self.I2C)

#-------------------------------------------------
# Device Configuration
#-------------------------------------------------

class Parameter:
    def __init__(self, device, parameter, bit):
        self.device = device
        self.register = device.Register.Port[PORT.A]
        self.bit = bit
        self.mask = 0b1 << bit
        self.parameter = parameter

    def set_value(self, value):
        self.value = value

    @property
    def value(self):
        value = (self.register.IOCON & self.mask) >> self.bit
        return self.patameter(value)
    
    @value.setter
    def value(self, setting):
        value = (setting.value << self.bit) & self.mask
        current = self.register.IOCON & ~(self.mask)
        value = ( value | current)
        self.register.IOCON = value
        if setting == Configuration.BANK.SEPARATE:
            self.device.set_bank(BANK.ONE)
        if setting == Configuration.BANK.SEQUENTIAL:
            self.device.set_bank(BANK.ZERO)
        
class Configuration:
    def __init__(self, device):
        self.device = device
        self.load_parameters()

    def load_parameters(self):
        self.Parameter = {}
        self.Parameter['INTCC'] = Parameter(self.device, self.INTCC, 0)
        self.Parameter['INTPOL'] = Parameter(self.device, self.INTPOL, 1)
        self.Parameter['ODR'] = Parameter(self.device, self.ODR, 2)
        self.Parameter['SEQOP'] = Parameter(self.device, self.SEQOP, 5)
        self.Parameter['MIRROR'] = Parameter(self.device, self.MIRROR, 6)
        self.Parameter['BANK'] = Parameter(self.device, self.BANK, 7)
    
    class INTCC(Enum):
        INTCAP = 0b1 
        """Reading INTCAP register clears the interrupt"""
        GPIO = 0b0 
        """Reading GPIO register clear the interrupt"""
    class INTPOL(Enum):
        ACTIVE_HIGH = 0b1 
        """Active-high"""
        ACTIVE_LOW = 0b0 
        """Active-low"""
    class ODR(Enum):
        OVERRIDE_INTPOL = 0b1 
        """Open-drain output (overrides the INTPOL bit)"""
        INTPOL = 0b0 
        """Active driver output (INTPOL bit sets the polarity)"""
    class SEQOP(Enum):
        NOT_INCREMENT = 0b1 
        """Sequential operation disabled, address pointer does not increment"""
        INCREMENT = 0b0 
        """Sequential operation enabled, address pointer increments"""
    class MIRROR(Enum):
        CONNECTED = 0b1 
        """The INT pins are internally connected in a wired OR configuration"""
        NOT_CONNECTED = 0b0 
        """The INT pins are connexted. INTA is associated with Port A and INT B is associated with Port B""" 
    class BANK(Enum):
        SEPARATE = 0b1 
        """The registers associated with each port are separated into different banks"""
        SEQUENTIAL = 0b0 
        """The registers are in the same bank (addresses are sequential)"""


#-------------------------------------------------
# Functionality
#-------------------------------------------------
class Pin:
    id = None
    address = None
    port = None

    def __init__(self, id, port):
        self.id = id
        self.address = 0b1 << id
        self.port = port
    
    def set_direction(self, direction):
        """
        Fluent API to set Direction of a Pin
        """
        self.direction = direction
        return self.port
    def set_value(self, state):
        """
        Fluent API to set Value of a Pin
        """
        self.value = state
        return self.port

    @property
    def direction(self):
        """
        Get or set pin direction: Direction.IN or Direction.OUT
        """
        direction_current = self.port.registers.IODIR
        direction = (direction_current & self.address) >> self.id
        return  Direction(direction)
    @direction.setter
    def direction(self, direction):
        direction_new = (direction.value * 0b11111111) & self.address
        direction_current = self.port.registers.IODIR & ~self.address
        data = (direction_new | direction_current)
        self.port.registers.IODIR = data

    @property
    def value(self):
        """
        Get or set pin value: State.HIGH or State.LOW
        """
        state_current = self.port.registers.OLAT
        state = (state_current & self.address) >> self.id
        return  State(state)
    @value.setter
    def value(self, state):
        state_new = (state.value * 0b11111111) & self.address
        state_current = self.port.registers.OLAT & ~self.address
        data = (state_new | state_current)
        self.port.registers.GPIO = data
    
class Port:
    Pin = {}
    device = None
    SIZE = None
    registers = None

    def __init__(self, device, registers):
        self.device = device
        self.registers = registers
        self.load_pins()

    def load_pins(self):
        self.Pin = {}
        self.Pin[PIN.GP0] = Pin(0, self)
        self.Pin[PIN.GP1] = Pin(1, self)
        self.Pin[PIN.GP2] = Pin(2, self)
        self.Pin[PIN.GP3] = Pin(3, self)
        self.Pin[PIN.GP4] = Pin(4, self)
        self.Pin[PIN.GP5] = Pin(5, self)
        self.Pin[PIN.GP6] = Pin(6, self)
        self.Pin[PIN.GP7] = Pin(7, self)
    def exist(self):
        return self.device
        
    def set_direction(self, direction):
        """
        Fluent API to set Direction of GPIO Pins on Port
        """
        self.registers.IODIR = direction.value * 0b11111111
        return self.device
    def set_value(self, state):
        """
        Fluent API to set the State of GPIO Pins on Port
        """
        self.registers.GPIO = state.value * 0b11111111
        return self.device

class GPIO:
    Port = {}
    device = None

    def __init__(self, device):
        self.device = device
        self.load_ports()
    
    def load_ports(self):
        for port in PORT:
            registers = self.device.Register.Port[port]
            self.Port[port] = Port(self.device, registers)

    def set_direction(self, direction):
        """
        Fluent API to set Direction of all GPIO Pins
        """
        for port in self.Port:
            self.Port[port].set_direction(direction)
        return self.device   
    def set_value(self, state):
        """
        Fluent API to set the State of all GPIO Pins
        """
        for port in self.Port:
            self.Port[port].set_value(state)
        return self.device

class MCP23018:
    _I2C_Address = None
    """
    Connecting ADDR to VSS will set the device I2C Address to 0x20.
    During instantiation of new MCP23018 a Default: 0x20 is set.
    """
    Register = None
    GPIO = None
    I2C = None
    RESET_PIN = None
    Configuration = None

    def __init__(self, reset_pin, I2C_Address=I2C_ADDRESS_RANGE.ONE):
        self.RESET_PIN = reset_pin
        self.I2C = I2C(self)
        self.I2C_Address = I2C_Address
        self.Register = Register(self)
        self.GPIO = GPIO(self)
        self.Configuration = Configuration(self)
        

    def reset(self):
        self.RESET_PIN.value = True
        self.RESET_PIN.value = False
        self.RESET_PIN.value = True
        return self 
    def wait(self, duration):
        time.sleep(duration)
        return self
 
    @property
    def I2C_Address(self):
        return self._I2C_Address
    @I2C_Address.setter
    def I2C_Address(self, I2C_Address):
        """
        Instantiated with default value:
        1. I2C_ADDRESS_RANGE.ONE if no value passed during class instantiation
        2. I2C_Address pass during class instantiation
        """
        if self._I2C_Address == I2C_Address:
            return
        if not isinstance(I2C_Address, I2C_ADDRESS_RANGE):
            raise Exception("Invalid I2C Address!")
        self._I2C_Address = I2C_Address
    
    def set_bank(self, bank):
        if bank not in BANK:
            raise Exception("Invalid memory bank")
        self.Register.Bank = bank
        self.Register.load_ports()
        self.GPIO.load_ports()