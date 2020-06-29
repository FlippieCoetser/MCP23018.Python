from enum import Enum, auto
import time


# TODO: Refactor MCP2221; Implement standard I2C Class
class I2C:
    """
    Description object represented by class

    ...
    Attributes
    __________
    address
        I2C Slave Address.
        The ADDR pin is used to set the slave address of the I2C Interface.
        Connecting ADDR to VSS will set MCP23018 slave address to I2C_ADDRESS_RANGE.ONE: 0x20.
        During instantiation I2C_ADDESS_RANGE.ONE is used as the default address.
    
    Methods
    _______
    method(paramters): return type
        description
    """

    """
    External device I2C Interface connected to SCL and SDA pins on MCP23018
    """
    def __init__(self, I2C_Interface, I2C_Address):
        self._interface = I2C_Interface()
        self._address = I2C_Address
        self.debug = False
        
    def write(self, register, data):
        address = register.value
        self._interface.writeto(self._address.value, bytes([address, data]))
        self._log("write",register, data)
        return
    def read(self, register):
        address = register.value
        data = bytearray(1)
        self._interface.writeto(self._address.value, bytes([address]))
        self._interface.readfrom_into(self._address.value, data)
        data = int.from_bytes(data,"big")
        self._log("read ", register, data)
        return data
    
    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, address):
        if self._address == address:
            return
        if address not in I2C_ADDRESS_RANGE:
            raise Exception("Invalid I2C Address!")
        self._address = address
    
    def _log(self, type, register, data):
        if self.debug:
            print("I2C Interface - Type: ", type, " Register: ", register, "[", register.value, "] Data: ", data )
        return

# TODO: Refactor MCP2221; Implement standard PIN Class
class RESET_PIN:
    """
    External device GPIO Pin connected to the RESET pin on MCP23018
    """
    def __init__(self, reset_pin):
        self._gpio = reset_pin
        self._state = STATE.HIGH
        self.debug = False

    @property
    def value(self):
        return self._state
    @value.setter
    def value(self, value):
        if value == STATE.HIGH:
            self._gpio.value = True
            self._state = STATE.HIGH
        if value == STATE.LOW:
            self._gpio.value = False
            self._state = STATE.LOW
        self._log(value)
    
    def _log(self, state):
        if self.debug:
            print("RESET - State: ", state)
        return

class DIRECTION(Enum):
    IN = 0b1
    OUT = 0b0

class STATE(Enum):
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

class PORT(Enum):
    A = 'A'
    B = 'B'

class PIN(Enum):
    GP0 = 0
    GP1 = 1
    GP2 = 2
    GP3 = 3
    GP4 = 4
    GP5 = 5
    GP6 = 6
    GP7 = 7

class PARAMETER(Enum):
    INTCC = 'INTCC'
    INTPOL = 'INTPOL'
    ODR = 'ODR'
    SEQOP = 'SEQOP'
    MIRRIOR = 'MIRRIOR'
    BANK = 'BANK'

PARAMETERS = {
        PARAMETER.INTCC: Enum(
            value = 'INTCC',
            names = [
                ('INTCAP', 0b1), # Reading INTCAP register clears the interrupt
                ('GPIO' , 0b0)   # Reading GPIO register clear the interrupt
                ]
            ),
        PARAMETER.INTPOL: Enum(
            value = 'INTPOL',
            names = [
                ('ACTIVE_HIGH',0b1), # Active-high
                ('ACTIVE_LOW',0b0)   # Active-low
                ]
            ),
        PARAMETER.ODR: Enum(
            value = 'ODR',
            names = [
                ('OVERRIDE_INTPOL',0b1), # Open-drain output (overrides the INTPOL bit)
                ('INTPOL',0b0)           # Active driver output (INTPOL bit sets the polarity)
                ]
            ),
        PARAMETER.SEQOP: Enum(
            value = 'SEQOP',
            names = [
                ('NOT_INCREMENT',0b1), # Sequential operation disabled, address pointer does not increment
                ('INCREMENT',0b0)      # Sequential operation enabled, address pointer increments
                ]
            ),
        PARAMETER.MIRRIOR: Enum(
            value = 'MIRRIOR',
            names = [
                ('CONNECTED',0b1),    # The INT pins are internally connected in a wired OR configuration
                ('NOT_CONNECTED',0b0) # The INT pins are connexted. INTA is associated with Port A and INT B is associated with Port B
                ]
            ),
        PARAMETER.BANK: Enum(
            value = 'BANK',
            names = [
                ('SEPARATE', 0b1),    # The registers associated with each port are separated into different banks
                ('SEQUENTIAL',0b0)    # The registers are in the same bank (addresses are sequential)
                ]
            )
    }

class Register:
    """
    Class used to represent all regesitesr available on MCP23018
    
    ...
    Private Properties
    __________________
    _address: int
        description
    _i2C:
        description

    Getters
    _______
    IODIR
    IPOL
    GPINTEN
    DEFVAL
    INTCON
    IOCON
    GPPU
    INTF
    INTCAP
    GPIO
    OLAT

    Setters
    _______
    IODIR
    IPOL
    GPINTEN
    DEFVAL
    INTCON
    IOCON
    GPPU
    GPIO
    OLAT
        
    Private methods
    ______________
    _read(int):int
        description
    _write(int)
        description
    """
    def __init__(self, address, i2c):
        self._address = address
        self._i2c = i2c
   
    def _read(self, address):
        """
        Get the contents of a specific register
        """
        return self._i2c.read(address)

    def _write(self, address, data):
        """
        Set the contents of a specific register
        """
        self._i2c.write(address, data)

    @property
    def IODIR(self):
        """
        I/O DIRECTION REGISTER: Controls the direction of the data I/O
        """
        return self._read(self._address.IODIR)  
    @IODIR.setter
    def IODIR(self, data):
        self._write(self._address.IODIR, data)

    @property
    def IPOL(self):
        """
        INPUT POLIRITY REGISTER: Configure the polarity of GPIO Port
        """
        return self._read(self._address.IPOL)       
    @IPOL.setter
    def IPOL(self, data):
        self._write(self._address.IPOL, data)

    @property
    def GPINTEN(self):
        """
        INTERRUPT-ON-CHANGE CONTROL REGISTER: Controls the interrupt-on-change feature of each pin of Port
        """
        return self._read(self._address.GPINTEN)    
    @GPINTEN.setter
    def GPINTEN(self, data):
        self._write(self._address.GPINTEN, data)
    
    @property
    def DEFVAL(self):
        """
        DEFAULT COMPARE REGISTER FOR INTERRUPT-ON-CHANGE: Configure default comparison value of the interrupt-on-change of Port
        """
        return self._read(self._address.DEFVAL)    
    @DEFVAL.setter
    def DEFVAL(self, data):
        self._write(self._address.DEFVAL, data)

    @property
    def INTCON(self):
        """
        INTERRUPT CONTROL REGISTER: Control how the associated pin value is compared for the interrupt-on-change of Port
        """ 
        return self._read(self._address.INTCON)     
    @INTCON.setter
    def INTCON(self, data):
        self._write(self._address.INTCON, data)
    
    @property
    def IOCON(self):
        """
        I/O EXPANDER CONFIGURATION: Configures the device
        """
        return self._read(self._address.IOCON)    
    @IOCON.setter
    def IOCON(self, data): 
        self._write(self._address.IOCON, data)

    @property
    def GPPU(self):
        """
        PULL-UP RESISTOR CONFIGURATION REGISTER: Controls the pull-up resistors for port A pins
        """
        return self._read(self._address.GPPU)   
    @GPPU.setter
    def GPPU(self, data):
        self._write(self._address.GPPU, data)

    @property
    def INTF(self):
        """
        INTERRUPT FLAG REGISTER: Reflects the interrupt condition on any interrupt enabled pins
        """
        return self._read(self._address.INTF)      
    @INTF.setter
    def INTF(self, data):
        raise Exception("INTF is a read-only register")

    @property
    def INTCAP(self):
        """
        INTERRUPT CAPTURE REGISTER: Captures the GPIO port value at time of Interrupt
        """
        return self._read(self._address.INTCAP)    
    @INTCAP.setter
    def INTCAP(self, data):
        raise Exception("INTCAP is a read-only register")
    
    @property
    def GPIO(self):
        """
        PORT REGISTER: The GPIO Register reflects the value on port
        """
        return self._read(self._address.GPIO)     
    @GPIO.setter
    def GPIO(self, data):
        self._write(self._address.GPIO, data)

    @property
    def OLAT(self):
        """
        OUTPUT LATCH REGISTER: Provides access to the ouput latches of the port
        """
        return self._read(self._address.OLAT)      
    @OLAT.setter
    def OLAT(self, data): 
        self._write(self._address.OLAT, data)

class Registers:
    """
    Description object represented by class
    
    ...
    Static Properties
    _________________
    ADDRESSES:
        description

    Private Properties
    __________________
    _i2c: type
        description

    Public Properties
    _________________
    port:
        description
    bank:
        Default Memory Bank after Reset is BANK.ZERO = 0

    Methods
    _______
    load_ports():
        description
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
    """
    A complete map of all registers addresses for all memory banks and ports 
    """
    def __init__(self, i2c):
        self._i2c = i2c
        self.bank = BANK.ZERO
        self.port = {}
        self.load_ports()
    
    def load_ports(self):
        """
        Based on the MCP23018 Memory Bank in use get registers address
        Create a port for each available port on MCP23018 and load correct registers address.

        """
        for port in PORT:
            address = Registers.ADDRESSES[self.bank][port]
            self.port[port] = Register(address, self._i2c)

class Configuration:
    """
    A class used to set and get the different confguration registers available on MCP23018
    
    ...
    Private Properties
    __________________
    _device: type
        description
    _register:
        description
    
    Getters
    _______
    bank: Configuration.BANK
        description

    Setters
    _______
    bank: Configuration.BANK
        description

    Private Method
    ______________
    _load_ports(BANK):
        description
    
    Public Method
    _____________
    reset():
        description
    """

    def __init__(self, device):
        self._device = device
        self._register = device.registers.port[PORT.A]
        self.debug = False

    @property
    def bank(self):
        bit = 7
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.BANK](value)
        self._log("read ",PARAMETER.BANK, value)
        return value
    @bank.setter
    def bank(self, config):
        bit = 7
        if config in PARAMETERS[PARAMETER.BANK]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
            if config == PARAMETERS[PARAMETER.BANK].SEPARATE:
                self._load_ports(BANK.ONE)
            if config == PARAMETERS[PARAMETER.BANK].SEQUENTIAL:
                self._load_ports(BANK.ZERO)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.BANK, config)
    
    @property
    def mirror(self):
        bit = 6
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.MIRRIOR](value)
        self._log("read ", PARAMETER.MIRRIOR, value)
        return value
    @mirror.setter
    def mirror(self, config):
        bit = 6
        if config in PARAMETERS[PARAMETER.MIRRIOR]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.MIRRIOR, config)
    
    @property
    def seqop(self):
        bit = 5
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.SEQOP](value)
        self._log("read ", PARAMETER.SEQOP, value)
        return value
    @seqop.setter
    def seqop(self, config):
        bit = 5
        if config in PARAMETERS[PARAMETER.SEQOP]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.SEQOP, config)

    @property
    def odr(self):
        bit = 2
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.ODR](value)
        self._log("read ", PARAMETER.ODR, value)
        return value
    @odr.setter
    def odr(self, config):
        bit = 2
        if config in PARAMETERS[PARAMETER.ODR]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.ODR, config)
    
    @property
    def intpol(self):
        bit = 1
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.INTPOL](value)
        self._log("read ", PARAMETER.INTPOL, value)
        return value
    @intpol.setter
    def intpol(self, config):
        bit = 1
        if config in PARAMETERS[PARAMETER.INTPOL]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.INTPOL, config)

    @property
    def intcc(self):
        bit = 0
        value = Pin.READ(self._register.IOCON, bit)
        value = PARAMETERS[PARAMETER.INTCC](value)
        self._log("read ", PARAMETER.INTCC, value)
        return value
    @intcc.setter
    def intcc(self, config):
        bit = 0
        if config in PARAMETERS[PARAMETER.INTCC]:
            self._register.IOCON = Pin.WRITE(self._register.IOCON, config.value, bit)
        else:
            raise Exception("Invalid configuration!")
        self._log("write", PARAMETER.INTCC, config)

    def _load_ports(self,bank):
        self._device.registers.bank = bank
        self._device.registers.load_ports()
        self._device.GPIO.load_ports()

    def _log(self, type, parameter, value):
        if self.debug:
            print("MCP23018 CONFIG - Type: ", type, " Parameter: ", parameter, " Value: ", value)
        return

    def reset(self):
        """
        Default Memory Bank in use after device reset is BANK.ZERO
        """
        self._device.registers.Bank = BANK.ZERO
    


class Pin:
    """
    A class used to represent an GPIO Ping available on MCP23018
    
    ...
    Static Methods
    ______________
    WRITE: int

    READ: Int

    Private Properties
    __________________
    _id: int

    _register

    Getters
    _______
    direction: DIRECTION
        description
    value: STATE
        description

    Setters
    _______
    direction: DIRECTION
        description
    value: STATE
        description
    """
    def __init__(self, id, register):
        self._id = id.value
        self._register = register
        self.debug = False
 
    WRITE = lambda current, new, bit: current & ~(0b1 << bit) | (new << bit) & (0b1 << bit)
    """
    Static Method used to change a single bit of a bus
    """
    READ = lambda current, bit: (current & (0b1 << bit)) >> bit
    """
    Static Method used to extract a single bit from a bus
    """

    @property
    def direction(self):
        """
        Get or set pin direction: Direction.IN or Direction.OUT
        """
        direction = Pin.READ(self._register.IODIR, self._id)
        direction = DIRECTION(direction)
        self._log("read ", direction)
        return direction 
    @direction.setter
    def direction(self, direction):
        self._register.IODIR = Pin.WRITE(self._register.IODIR, direction.value, self._id)
        self._log("write", direction)

    @property
    def value(self):
        """
        Get or set pin value: State.HIGH or State.LOW
        """
        if self.direction == DIRECTION.IN:
            register = self._register.GPIO
            state = STATE(Pin.READ(register, self._id))
            self._log("read ",state)
            return state
        else:
            register = self._register.OLAT
            state = STATE(Pin.READ(register, self._id))
            self._log("read ",state)
            return state
    @value.setter
    def value(self, state):
        self._register.GPIO = Pin.WRITE(self._register.OLAT, state.value, self._id)
        self._log("write", state)

    def _log(self, type, value):
        if self.debug:
            print("MCP23018 GPIO PIN ", self._id, "- Type: ", type, " Value: ", value)
        return
    
class Port:
    """
    A class used to represent an 8-bit GPIO Port available on MCP23018

    ...
    Private Properties
    __________________
    _register: type
        addresses of each register on port

    Public Properties
    _________________
    pin: Pin[]
        Dictionary containg 8 GPIO pins
    size: int
        size of the port    
    
    Public Methods
    ______________
    load_pins():
        Load the pin dicionary with each ping defined in ENUM PIN

    Getters
    _______
    size: int
        get the size of port
    direction: DIRECTION
        get the direction of all pins on port
    value: DIRECTION
        get the value of all pins on port

    Setters
    _______
    direction:
        set the direction of all pins on port
    value:
        set the value of all pins on port
    """
    def __init__(self, register):
        """
        Load private register property with the address of each register based on the current mode and memory bank in operation
        Create a new pin for each PIN in enum and load into local pin dictionary
        """
        self._register = register
        self.load_pins()

    def load_pins(self):
        """
        Create a new pin for each PIN in enum and load into local pin dictionary
        """
        self.pin = {}
        self.pin[PIN.GP0] = Pin(PIN.GP0, self._register)
        self.pin[PIN.GP1] = Pin(PIN.GP1, self._register)
        self.pin[PIN.GP2] = Pin(PIN.GP2, self._register)
        self.pin[PIN.GP3] = Pin(PIN.GP3, self._register)
        self.pin[PIN.GP4] = Pin(PIN.GP4, self._register)
        self.pin[PIN.GP5] = Pin(PIN.GP5, self._register)
        self.pin[PIN.GP6] = Pin(PIN.GP6, self._register)
        self.pin[PIN.GP7] = Pin(PIN.GP7, self._register)
    
    @property
    def size(self):
        """
        calculate the port size using number of pins available in port
        """
        return (2 ** len(self.pin)) - 1

    @property
    def direction(self):
        """
        Read the direction of all ports in a specific port
        if all pins do not have the same direction, return a binary representation of the direction of all pins
        """
        # TODO: Refactor to loop through Pins
        iodir = self._register.IODIR
        if iodir == 0b11111111:
            return DIRECTION(0b1)
        elif iodir == 0b00000000:
            return DIRECTION(0b0)
        else:
            return bin(iodir)
    @direction.setter
    def direction(self, direction):
        """
        Set direction of all pin in a specific port
        """
        # TODO: Refactor to loop through Pins
        self._register.IODIR = direction.value * self.size

    @property
    def value(self):
        """
        Read the value of all ports in a specific port
        if all pins do not have the same state, return a binary representation of the state of all pins
        """
        # TODO: Refactor to loop through Pins
        if self.direction == DIRECTION.IN:
            state = self._register.GPIO
            return bin(state)
        else:
            state = self._register.OLAT
            return bin(state)
    @value.setter
    def value(self, state):
        """
        Set the state of all pins in a specific port
        """
        # TODO: Refactor to loop through Pins
        if isinstance(state, STATE):
            self._register.GPIO = state.value * self.size
        elif isinstance(state, int):
            self._register.GPIO = state
        else:
            raise Exception("Value must be STATE or int")

class GPIO:
    """
    A class used to represent the 16-bit GPIO available on MCP23018

    ...
    Private Properties
    __________________
    _device: MCP23018
        Private navigation property linking back to MCP23018
    
    Public Properties
    _________________
    port: port[]
        Dictionary containg two 8-bit ports: PORT.A and PORT.B
        
    Public Methods
    ______________
    load_ports():
        Load the port dictionary with each port defined in ENUM PORT

    Setters
    _______
    direction:
        Set direction of all 16 GPIO Pins available on MCP23018 at once
    value:
        Set value of all 16 GPIO Pins available on MCP23018 at once
    """
    def __init__(self, device):
        """
        Load MCP23018 Parent instance into private property
        Load all available ports into into public property
        """
        self._device = device
        self.load_ports()
    
    def load_ports(self):
        """
        Create a new port for each PORT in enum and load into local port dictionary
        """
        self.port = {}
        for port in PORT:
            register = self._device.registers.port[port]
            self.port[port] = Port(register)

    @property
    def direction(self):
        raise Exception("Read direction on PORT of interest and not on GPIO!")
    @direction.setter
    def direction(self, direction):
        """
        Set all ports direction at once
        """
        for port in self.port:
            self.port[port].direction = direction
    
    @property
    def value(self):
        raise Exception("Read value on PORT of interest and not on entire GPIO")
    @value.setter
    def value(self, state):
        """
        Set all ports value at once
        """
        for port in self.port:
            self.port[port].value = state

class MCP23018:
    """
    A class used to represent a 16-bit I/O Expander with Open-Drain Outputs from Microchip

    ...
    Public Properties
    _________________
    RESET : PIN
        External device GPIO Pin connect to the RESET on MCP23018
        PDIP / SOIC: RESET = Pin 16
        SSOP: RESET = Pin 14
    I2C : I2C
        External device I2C Interface connected to SCL and SDA on MCP23018
        PDIP / SOIC: SCL = Pin 12, SDA = Pin 13
        SSOP: SCL = Pin 11, SDA = Pin 12
    registers: 
        Addresses of all registers available on MCP23018
        Initialized using Bank ZERO and Mode SEQUENTIAL
    GPIO: GPIO
        General Purpose Input Output Port
        Initialised with two 8 bit Ports
    configuration: Configuration
        MCP23018 Configuration
        Used to configure the 6 configuration paramters via register IOCON
    
    Public Methods
    ______________
    reset()
        Resets MCP23018 via external GPIO PIN
    wait(duration)
        Wait specified number of miliseconds
    """
    def __init__(self, RESET_Pin, I2C_Interface, I2C_Address=I2C_ADDRESS_RANGE.ONE):
        """
        Parameters
        __________
        RESET_Pin: RESET_PIN
            See RESET Property on MCP23018 Class
        I2C_Interface: I2C
            See I2C Property on MCP23018 Class
        I2C_Address: I2C_ADDRESS_RANGE.ONE
            MCP23018 I2C Slave Address 
            See Address Property on I2C Class
        """
        self.RESET = RESET_PIN(RESET_Pin)
        self.I2C = I2C(I2C_Interface, I2C_Address)
        self.registers = Registers(self.I2C)
        self.GPIO = GPIO(self)
        self.Configuration = Configuration(self)
        
    def reset(self):
        """
        Apply a sequence of state changes on external RESET pin
        """
        sequence = [STATE.HIGH, STATE.LOW, STATE.HIGH]
        [self.RESET.__setattr__('value',state) for state in sequence]
        self.Configuration.reset()

    def wait(self, duration):
        """
        Use external library to Wait for a specified number of seconds
        """
        time.sleep(duration)
