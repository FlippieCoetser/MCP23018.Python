from enum import Enum
import time

class Direction(Enum):
    OUT = 0b0
    IN = 0b1

class State(Enum):
    HIGH = 0b1
    LOW = 0b0


# TODO: Move into Register and transfrom from port level to pin level
class resistor(Enum):
    ENABLED = 0xff
    DISABLED = 0X00

class Register:
    def __init__(self, device, memory_bank="bank0"):
        if memory_bank == "bank0":
            self.addresses = self.bank0
        elif memory_bank == "bank1":
            self.addresses = self.bank1
        else:
            raise Exception("invalid memory bank")
        self.device = device
    
    # TODO: Transfrom from Port level to Pin level
    class polarity(Enum):
        OPPOSITE : 0xff
        SAME: 0x00
    
    # TODO: Transfrom from Port level to Pin level
    class interrupt_on_change(Enum):
        ENABLED: 0xff
        DISABLED: 0x00
    
    # TODO: Transfrom from Port level to Pin level
    class interrupt_on_change_control(Enum):
        DEFVAL: 0xff
        PREVIOUS: 0x00

    class bank0(Enum): 
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

    class bank1(Enum): 
        IODIRA = 0x00
        IPOLA = 0x01
        GPINTENA = 0x02
        DEFVALA = 0x03
        INTCONA = 0x04
        IOCONA = 0x05
        GPPUA = 0x06
        INTFA = 0x07
        INTCAPA = 0x08
        GPIOA = 0x09
        IODIRB = 0x10
        OLATA = 0x0a
        IPOLB = 0x11
        GPINTENB = 0x12
        DEFVALB = 0x13
        INTCONB = 0x14
        IOCONB = 0x15
        GPPUB = 0x16
        INTFB = 0x17
        INTCAPB = 0x18
        GPIOB = 0x19
        OLATB = 0x1a

    @property
    def IODIRA(self):
        """
        I/O DIRECTION REGISTER: Controls the direction of the data I/O for port A
        """
        register = self.addresses.IODIRA 
        return self.device.readFrom(register)
        
    @IODIRA.setter
    def IODIRA(self, direction):
        register = self.addresses.IODIRA
        data = direction
        self.device.writeTo(register, data)
    
    @property
    def IODIRB(self):
        """
        I/O DIRECTION REGISTER: Controls the direction of the data I/O for port B
        """
        register = self.addresses.IODIRB
        return self.device.readFrom(register)
        
    @IODIRB.setter
    def IODIRB(self, direction):
        register = self.addresses.IODIRB
        data = direction
        self.device.writeTo(register, data)
    
    @property
    def IPOLA(self):
        """
        INPUT POLIRITY REGISTER: Configure the polarity of GPIO Port A
        """
        register = self.addresses.IPOLA
        return self.device.readFrom(register)
        
    @IPOLA.setter
    def IPOLA(self, polarity):
        register = self.addresses.IPOLA
        data = polarity.value
        self.device.writeTo(register, data)

    @property
    def IPOLB(self):
        """
        INPUT POLIRITY REGISTER: Configure the polarity of GPIO Port B
        """
        register = self.addresses.IPOLB
        return self.device.readFrom(register)
        
    @IPOLB.setter
    def IPOLB(self, polarity):
        register = self.addresses.IPOLB
        data = polarity.value
        self.device.writeTo(register, data)

    @property
    def GPINTENA(self):
        """
        INTERRUPT-ON-CHANGE CONTROL REGISTER: Controls the interrupt-on-change feature of each pin of Port A
        """
        register = self.addresses.GPINTENA
        return self.device.readFrom(register)
        
    @GPINTENA.setter
    def GPINTENA(self, interrupt_on_change):
        register = self.addresses.GPINTENA
        data = interrupt_on_change.value
        self.device.writeTo(register, data)
    
    @property
    def GPINTENB(self):
        """
        INTERRUPT-ON-CHANGE CONTROL REGISTER: Controls the interrupt-on-change feature of each pin of Port B
        """
        register = self.addresses.GPINTENA
        return self.device.readFrom(register)
        
    @GPINTENB.setter
    def GPINTENB(self, interrupt_on_change):
        register = self.addresses.GPINTENB
        data = interrupt_on_change.value
        self.device.writeTo(register, data)
    
    @property
    def DEFVALA(self):
        """
        DEFAULT COMPARE REGISTER FOR INTERRUPT-ON-CHANGE: Configure default comparison value of the interrupt-on-change of Port A
        """
        register = self.addresses.DEFVALA
        return self.device.readFrom(register)
        
    @DEFVALA.setter
    def DEFVALA(self, value):
        register = self.addresses.DEFVALA
        self.device.writeTo(register, value)

    @property
    def DEFVALB(self):
        """
        DEFAULT COMPARE REGISTER FOR INTERRUPT-ON-CHANGE: Configure default comparison value of the interrupt-on-change of Port B
        """
        register = self.addresses.DEFVALB
        return self.device.readFrom(register)
        
    @DEFVALB.setter
    def DEFVALB(self, value):
        register = self.addresses.DEFVALB
        self.device.writeTo(register, value)

    @property
    def INTCONA(self):
        """
        INTERRUPT CONTROL REGISTER: Control how the associated pin value is compared for the interrupt-on-change of Port A
        """
        register = self.addresses.INTCONA
        return self.device.readFrom(register)
        
    @INTCONA.setter
    def INTCONA(self, interrupt_on_change_control):
        register = self.addresses.INTCONA
        data = interrupt_on_change_control.value
        self.device.writeTo(register, data)
    
    @property
    def INTCONB(self):
        """
        INTERRUPT CONTROL REGISTER: Control how the associated pin value is compared for the interrupt-on-change of Port B
        """
        register = self.addresses.INTCONB
        return self.device.readFrom(register)
        
    @INTCONB.setter
    def INTCONB(self, interrupt_on_change_control):
        register = self.addresses.INTCONB
        data = interrupt_on_change_control.value
        self.device.writeTo(register, data)
    
    # TODO: Implement detail configuration options
    @property
    def IOCON(self):
        """
        I/O EXPANDER CONFIGURATION: Configures the device
        """
        register = self.addresses.IOCONA
        return self.device.readFrom(register)
        
    @IOCON.setter
    def IOCON(self, data):
        register = self.addresses.IOCONA
        self.device.writeTo(register, data)

    @property
    def GPPUA(self):
        """
        PULL-UP RESISTOR CONFIGURATION REGISTER: Controls the pull-up resistors for port A pins
        """
        register = self.addresses.GPPUA
        return self.device.readFrom(register)
        
    @GPPUA.setter
    def GPPUA(self, resistor):
        register = self.addresses.GPPUA
        data = resistor.value
        self.device.writeTo(register, data)

    @property
    def GPPUB(self):
        """
        PULL-UP RESISTOR CONFIGURATION REGISTER: Controls the pull-up resistors for port B pins
        """
        register = self.addresses.GPPUB
        return self.device.readFrom(register)
        
    @GPPUB.setter
    def GPPUB(self, resitor):
        register = self.addresses.GPPUB
        data = resitor.value
        self.device.writeTo(register, data)

    # TODO: Implent ENUM and Return correct value
    @property
    def INTFA(self):
        """
        INTERRUPT FLAG REGISTER: Reflects the interrupt condition on any interrupt enabled pins on port A
        """
        register = self.addresses.INTFA
        return self.device.readFrom(register)
        
    @INTFA.setter
    def INTFA(self, data):
        raise Exception("INTFA is a read-only register")

    # TODO: Implent ENUM and Return correct value
    @property
    def INTFB(self):
        """
        INTERRUPT FLAG REGISTER: Reflects the interrupt condition on any interrupt enabled pins on port B
        """
        register = self.addresses.INTFB
        return self.device.readFrom(register)
        
    @INTFB.setter
    def INTFB(self, data):
        raise Exception("INTFB is a read-only register")

    @property
    def INTCAPA(self):
        """
        INTERRUPT CAPTURE REGISTER: Captures the GPIO port A value at time of Interrupt
        """
        register = self.addresses.INTCAPA
        return self.device.readFrom(register)
        
    @INTCAPA.setter
    def INTCAPA(self, data):
        raise Exception("INTCAPA is a read-only register")

    @property
    def INTCAPB(self):
        """
        INTERRUPT CAPTURE REGISTER: Captures the GPIO port B value at time of Interrupt
        """
        register = self.addresses.INTCAPB
        return self.device.readFrom(register)
        
    @INTCAPB.setter
    def INTCAPB(self, data):
        raise Exception("INTCAPB is a read-only register")
    
    @property
    def GPIOA(self):
        """
        PORT REGISTER: The GPIO Register reflects the value on port A
        """
        register = self.addresses.GPIOA
        return self.device.readFrom(register)
        
    @GPIOA.setter
    def GPIOA(self, data):
        register = self.addresses.GPIOA
        self.device.writeTo(register, data)

    @property
    def GPIOB(self):
        """
        PORT REGISTER: The GPIO Register reflects the value on port B
        """
        register = self.addresses.GPIOB
        return self.device.readFrom(register)
        
    @GPIOB.setter
    def GPIOB(self, data):
        register = self.addresses.GPIOB
        self.device.writeTo(register, data)

    @property
    def OLATA(self):
        """
        OUTPUT LATCH REGISTER: Provides access to the ouput latches of port A
        """
        register = self.addresses.OLATA
        return self.device.readFrom(register)
        
    @OLATA.setter
    def OLATA(self, data):
        register = self.addresses.OLATA
        self.device.writeTo(register, data)

    @property
    def OLATB(self):
        """
        OUTPUT LATCH REGISTER: Provides access to the ouput latches of port B
        """
        register = self.addresses.OLATB
        return self.device.readFrom(register)
        
    @OLATB.setter
    def OLATB(self, data):
        register = self.addresses.OLATB
        self.device.writeTo(register, data)

class PortA:
    def __init__(self, device):
        self.device = device
        self.reset()
    
    def reset(self):
        self._direction = Direction.IN
        self._value = State.LOW
        return

    def set_direction(self, direction):
        """
        Fluent API to set Direction of all GPIO Pins on Port A
        """
        self.direction = direction
        return self.device
    
    def set_value(self, state):
        """
        Fluent API to set the State of all GPIO Pins on Port A
        """
        self.value = state
        return self.device
    
    @property
    def direction(self):
        """
        Set Direction of all GPIO Pins on Port A
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        if self._direction == direction:
            return
        if direction == Direction.IN:
            # TODO: Remove hard coded values
            self.device.Register.IODIRA = 0xff
            self._direction = Direction.IN
        if direction == Direction.OUT:
            # TODO: Remove hard coded values
            self.device.Register.IODIRA = 0x00
            self._direction = Direction.OUT

    @property
    def value(self):
        """
        Set State of all GPIO Pins on Port A
        """
        return self._direction
    @value.setter
    def value(self, state):
        if self._value == state:
            return
        if state == State.LOW:
            # TODO: Remove hard coded values
            self.device.Register.GPIOA = 0x00
            self._value = State.LOW
        if state == State.HIGH:
            # TODO: Remove hard coded values
            self.device.Register.GPIOA = 0xff
            self._value = State.HIGH

class PortB:
    def __init__(self, device):
        self.device = device
        self.reset()

    def reset(self):
        self._direction = Direction.IN
        self._value = State.LOW
        return
        
    def set_direction(self, direction):
        """
        Fluent API to set Direction of all GPIO Pins on Port B
        """
        self.direction = direction
        return self.device
    
    def set_value(self, state):
        """
        Fluent API to set the State of all GPIO Pins on Port B
        """
        self.value = state
        return self.device
    
    @property
    def direction(self):
        """
        Set Direction of all GPIO Pins on Port B
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        if self._direction == direction:
            return
        if direction == Direction.IN:
            # TODO: Remove hard coded values
            self.device.Register.IODIRB = 0xff
            self._direction = Direction.IN
        if direction == Direction.OUT:
            # TODO: Remove hard coded values
            self.device.Register.IODIRB = 0x00
            self._direction = Direction.OUT

    @property
    def value(self):
        """
        Set State of all GPIO Pins on Port B
        """
        return self._direction
    @value.setter
    def value(self, state):
        if self._value == state:
            return
        if state == State.LOW:
            # TODO: Remove hard coded values
            self.device.Register.GPIOB = 0x00
            self._value = State.LOW
        if state == State.HIGH:
            # TODO: Remove hard coded values
            self.device.Register.GPIOB = 0xff
            self._value = State.HIGH

class GPIO:
    def __init__(self, device):
        self.device = device
        self.Ports = {
            "A" : PortA(device),
            "B" : PortB(device)
        }
        self.reset()

    def reset(self):
        self._direction = Direction.IN
        self._value = State.LOW
        for port in self.Ports:
            self.Ports[port].reset()
        return

    def set_direction(self, direction):
        """
        Fluent API to set Direction of all GPIO Pins
        """
        self.direction = direction
        return self.device
    
    def set_value(self, state):
        """
        Fluent API to set the State of all GPIO Pins
        """
        self.value = state
        return self.device

    @property
    def direction(self):
        """
        Set Direction of all GPIO Pins
        """
        return self._direction
    @direction.setter
    def direction(self, direction):
        if self._direction == direction:
            return
        if direction == Direction.IN:
            for port in self.Ports:
                self.Ports[port].direction = Direction.IN
            self._direction = Direction.IN
        if direction == Direction.OUT:
            for port in self.Ports:
                self.Ports[port].direction = Direction.OUT
            self._direction = Direction.OUT

    @property
    def value(self):
        """
        Set State of all GPIO Pins
        """
        return self._direction
    @value.setter
    def value(self, state):
        if self._value == state:
            return
        if state == State.LOW:
            for port in self.Ports:
                self.Ports[port].value = State.LOW
            self._value = State.LOW
        if state == State.HIGH:
            for port in self.Ports:
                self.Ports[port].value = State.HIGH
            self._value = State.HIGH


class MCP23018:
    I2C_ADDRESS = 0x20

    def __init__(self, reset_pin, i2c):
        self.reset_pin = reset_pin
        self.i2c = i2c
        self.Register = Register(self)
        self.GPIO = GPIO(self)
        self.reset()
    
    def reset(self):
        self.reset_pin.value = True
        self.reset_pin.value = False
        self.reset_pin.value = True
        self.GPIO.reset()
        return self
    
    def wait(self, duration):
        time.sleep(duration)
        return self

    def writeTo(self, register, data):
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register.value, data]))
    
    def readFrom(self, register):
        data = bytearray(1)
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register.value]), stop=False)
        self.i2c.readfrom_into(self.I2C_ADDRESS, data)
        data = int.from_bytes(data,"big")
        return data