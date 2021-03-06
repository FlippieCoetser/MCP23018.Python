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

#-------------------------------------------------
# Register Mapping
#-------------------------------------------------

class Port_Registers:
    def __init__(self, id, memory_map, device):
        self.device = device
        self.id = id
        self.Address = Enum(
            value = 'Address',
            names = memory_map
        )
    
    @property
    def IODIR(self):
        """
        I/O DIRECTION REGISTER: Controls the direction of the data I/O
        """
        register = self.Address.IODIR 
        return self.device.read_from(register)
        
    @IODIR.setter
    def IODIR(self, direction):
        register = self.Address.IODIR
        data = direction
        self.device.write_to(register, data)
    
    @property
    def IPOL(self):
        """
        INPUT POLIRITY REGISTER: Configure the polarity of GPIO Port
        """
        register = self.Address.IPOL
        return self.device.read_from(register)
        
    @IPOL.setter
    def IPOL(self, polarity):
        register = self.Address.IPOL
        data = polarity.value
        self.device.write_to(register, data)

    @property
    def GPINTEN(self):
        """
        INTERRUPT-ON-CHANGE CONTROL REGISTER: Controls the interrupt-on-change feature of each pin of Port
        """
        register = self.Address.GPINTEN
        return self.device.read_from(register)
        
    @GPINTEN.setter
    def GPINTEN(self, interrupt_on_change):
        register = self.Address.GPINTEN
        data = interrupt_on_change.value
        self.device.write_to(register, data)
    
    @property
    def DEFVAL(self):
        """
        DEFAULT COMPARE REGISTER FOR INTERRUPT-ON-CHANGE: Configure default comparison value of the interrupt-on-change of Port
        """
        register = self.Address.DEFVAL
        return self.device.read_from(register)
        
    @DEFVAL.setter
    def DEFVAL(self, value):
        register = self.Address.DEFVAL
        self.device.write_to(register, value)

    @property
    def INTCON(self):
        """
        INTERRUPT CONTROL REGISTER: Control how the associated pin value is compared for the interrupt-on-change of Port
        """
        register = self.Address.INTCON
        return self.device.read_from(register)
        
    @INTCON.setter
    def INTCON(self, interrupt_on_change_control):
        register = self.Address.INTCON
        data = interrupt_on_change_control.value
        self.device.write_to(register, data)
    
    # TODO: Implement detail configuration options
    @property
    def IOCON(self):
        """
        I/O EXPANDER CONFIGURATION: Configures the device
        """
        register = self.Address.IOCON
        return self.device.read_from(register)
        
    @IOCON.setter
    def IOCON(self, data):
        register = self.Address.IOCON
        self.device.write_to(register, data)

    @property
    def GPPU(self):
        """
        PULL-UP RESISTOR CONFIGURATION REGISTER: Controls the pull-up resistors for port A pins
        """
        register = self.Address.GPPU
        return self.device.read_from(register)
        
    @GPPU.setter
    def GPPU(self, resistor):
        register = self.Address.GPPU
        data = resistor.value
        self.device.write_to(register, data)

    # TODO: Implent ENUM and Return correct value
    @property
    def INTF(self):
        """
        INTERRUPT FLAG REGISTER: Reflects the interrupt condition on any interrupt enabled pins
        """
        register = self.Address.INTF
        return self.device.read_from(register)
        
    @INTF.setter
    def INTF(self, data):
        raise Exception("INTF is a read-only register")

    @property
    def INTCAP(self):
        """
        INTERRUPT CAPTURE REGISTER: Captures the GPIO port value at time of Interrupt
        """
        register = self.Address.INTCAP
        return self.device.read_from(register)
        
    @INTCAP.setter
    def INTCAP(self, data):
        raise Exception("INTCAP is a read-only register")
    
    @property
    def GPIO(self):
        """
        PORT REGISTER: The GPIO Register reflects the value on port
        """
        register = self.Address.GPIO
        return self.device.read_from(register)
        
    @GPIO.setter
    def GPIO(self, data):
        register = self.Address.GPIO
        self.device.write_to(register, data)

    @property
    def OLAT(self):
        """
        OUTPUT LATCH REGISTER: Provides access to the ouput latches of the port
        """
        register = self.Address.OLAT
        return self.device.read_from(register)
        
    @OLAT.setter
    def OLAT(self, data):
        register = self.Address.OLAT
        self.device.write_to(register, data)

#-------------------------------------------------
# CHIP SETTINGS MAP
#-------------------------------------------------

# CHIPSETTING0 REGISTER (R/W):
# - BIT 0-1: CHIPPROT (Chip Settings Protection Level)
# > 00 = Chip setting unprotected (default)
# > 01 = Password protection
# > 10 = Permenently locked
# > 11 = Reserved
# - BIT 2: USBCFGINST (USBCFG Inactive State)
# > 1 = USBCFG is inactive high and active low (default)
# > 0 = USBCFG is inactive low and active high
# - BIT 3: SSPNDINST (SSPND Inactive State)
# > 1 = SSPND is inactive high and active low (default)
# > 0 = SSPND is inactive low and active high
# - BIT 4: LEDI2C (LED I2C Inactive State)
# > 1 = LED I2C is inactive high and active low (default)
# > 0 = LED I2C is inactive low and active high
# - BIT 5: LEDUTXINST (LED UART Tx Inactive State)
# > 1 = LED UART Tx is inactive high and active low (default)
# > 0 = LED UART Tx is inactive low and active high
# - BIT 6: LEDURXINST (LED UART Rx Inactive State)
# > 1 = LED UART Rx is inactive high and active low (default)
# > 0 = LED UART Rx is inactive low and active high
# - BIT 7: CDCSNEN (USB CDC Serial Number Enable)
# > 1 = USB CDC Serial Number is enumerated
# > 0 = NO USB CDC Serial Number enumeration (default)

# CHIPSETTING1 REGISTER (R/W):
# - BIT 0 - 2: CLKDIV (CLock-Out Divider Output)
# > 111 = 375 kHz clock output
# > 110 = 750 kHz clock output
# > 101 = 1.5 MHz clock output
# > 100 = 3 MHz clock output
# > 011 = 6 MHz clock output
# > 010 = 12 MHz clock output (default)
# > 001 = 24MHz clock output
# > 000 = Reserved
# - BIT 3 - 4: CLKDC (Clock-out Duty Cycle)
# > 11 = Duty cycle 75%
# > 10 = Duty cycle 50% (default)
# > 01 = Duty cycle 25%
# > 00 = Duty cycle 0%
# - BIT 5 - 7: Reserved = Set to 0

# CHIPSETTING2 REGISTER (R/W)
# - BIT 0 - 4: DACVAL (Initial DAC Output Value)
# > 5 bit value for the DAC Output (default = 8 decimal)
# - BIT 5: DACREF (DAC Reference Output Select)
# > 1 = DAC Reference output is DAC VRM voltage selection
# > 0 = DAC reference output is Vdd (default)
# - Bit 6 - 7: DACVRM (DAC Internal Voltage Reference selection)

# CHIPSETTING3 REGISTER (R/W)
# - BIT 0 - 1: Reserved = Set to 0
# - BIT 2: ADCREG (ADC Reference Output Selection1)
# > 1 = ADC Reference output is ADC VRM voltage selection (default)
# - BIT 3 - 4: ADCVRM (ADC Reference Output Selection)
# > 11 = VRM voltage is 4.096V 
# > 10 = VRM voltage is 2.048V
# > 01 = VRM voltage is 1.024V (default)
# > 00 = VRM is off
# - BIT 5: INTDETREEN (Interrupt Rising Edge Detect Enable)
# > 1 = Interrupt detector will trigger when a falling edge is detected (default)
# > 0 = Rising edges will not trigger the detector
# - BIT 6: INTDETFEEN (Interrupt Falling Edge Detect Enable)
# > 1 = Interrupt detector will trigger when a falling edge is detected (default)
# > 0 = Falling edges will not trigger the detector
# - BIT 7: Reserved Set to 0

# USBVIDL REGISTER (R/W)
# - BIT 0 - 7: USBVIDL (USB VID Lower Byte) (default = 0xd8)

# USBVIDH REGISTER (R/W)
# - BIT 0 - 7: USBVIHL (USB VID Higher Byte) (default = 0x04)

# USBPIDL REGISTER (R/W)
# - BIT 0 - 7: USB PID Lower Byte (default = 0xdd)

# USBPIDH REGISTER (R/W)
# - BIT 0 - 7: USB PID Higher Byte (default = 0x00)

# USBPWRATTR REGISTER (R/W)
# - BIT 0 - 4: Reserved Set all bit to 0 (default)
# - BIT 5: REMWKUP (USB Remote Wake-Up Capability)
# > 1 = Chip will enumerate on the USB bus as being able to wake-up the USB host
# > 0 = Chip will enumarate as not being capable of remote wake-up of the USB host (default)
# - BIT 6: SELFPWR (USB Self-Powered Attribute)
# > 1 = Chip will enumerate on the USB bus as being self-powered
# > 0 = Chip will enumerate on the USB bus as being USB-bus powered (default)
# > BIT 7: Reserved set to 1

# USBREQCRT REGISTER (R/W)
# - BIT 0 - 7: USBREQCRT (USB Bus-Powered Required Current Amount)
# Factory default is 50 (decimal); the USB enumeration interprets this value as a current requirement of 100 mA

# PASS0 - PASS7 REGISTER (R/W)
# - BIT 0 - 7: PASSx (Password Byte X Value) (default = 0)

#-------------------------------------------------
# GP SETTINGS MAP
#-------------------------------------------------

# GPSETTING0 REGISTER (R/W)
# - BIT 0 - 2: GPDES (GP0 Designation)
# > 111 = Reserved 
# > 110 = Reserved
# > 101 = Reserved
# > 100 = Reserved
# > 011 = Reserved
# > 010 = Alternate function 0 (LED UART Rx - LEDURX) (default)
# > 001 = Dedicated function operation (SSPND)
# > 000 = GPIO operation (GPIO0)  

# GPSETTING1 REGISTER (R/W)
# - BIT 0 - 2: GPDES (GP1 Designation)
# > 111 = Reserved
# > 110 = Reserved
# > 101 = Reserved
# > 100 = Alternate function 2 (Interrupt deterctor)
# > 011 = Alternate function 1 (LED UART Tx - LEDUTX) (default)
# > 010 = Alternate function 0 (ADC1)
# > 001 = Dedicated function operation (Clock Output)
# > 000 = GPIO operation (GPIO1)
# - BIT 3: GPIODIR (GPIO Direction. Valid only when GP1 is set for GPIO operation)
# > 1 = GPIO Input
# > 0 = GPIO Output (default)
# - BIT 4: GPIOOUTVAL (GPIO Output Value. Valid only when GP1 is set for GPIO operation)
# > 1 = Default output value is logic 1 (default)
# > 0 = Default output value is logc 0
# - BIT 5 - 7: Reserved Set to 0

# GPSETTING2 REGISTER (R/W)
# - BIT 0 - 2: GPDES (GP2 Designation)  
# > 111 = Reserved
# > 110 = Reserved
# > 101 = Reserved
# > 100 = Reserved
# > 011 = Alternate function 1 (DAC1)
# > 010 = Alternate function 0 (ADC2)
# > 001 = Dedicated function operation (USBCFG) (default)
# > 000 = GPIO operation (GPIO2)
# - BIT 3: GPIODIR (GPIO Direction. Valid only when GP2 is set for GPIO operation)
# > 1 = GPIO Input
# > 0 = GPIO Output (default)
# - BIT 4: GPIOOUTVAL (GPIO Output Value. Valid only when GP2 is set for GPIO operation)
# > 1 = Default output value is logic 1 (default)
# > 0 = Default output value is logic 0
# - BIT 5 - 7: Reserved

# GPSETTING3 REGISTER (R/W)
# - BIT 0 - 2: GPDES (GP3 Designation)
# > 111 = Reserved
# > 110 = Reserved
# > 101 = Reserved
# > 100 = Reserved
# > 011 = Alternate function 1 (DAC2)
# > 010 = Alternate function 0 (ADC3)
# > 001 = Dedicated function operation (LEDI2C) (default)
# > 000 = GPIO operation (GPIO3) 
# - BIT 3: GPIODIR (GPIO Direction. Valid only when GP3 is set for GPIO operation)
# > 1 = GPIO Input
# > 0 = GPIO Output (default)
# - BIT 4: GPIOOUTVAL (GPIO Output. Valid only when GP3 is set for GPIO operation)
# > 1 = Default output value is logic 1
# > 0 = Default output value is logic 0 
# - BIT 5 - 7: Reserved Set 0


class Register:
    def __init__(self, device):
        self.device = device
        self.load_addresses()
    
    def load_addresses(self):
        self.Bank = {}
        for bank in self.device.MEMORY_BANKS:
            self.Bank[bank] = {}
        self.Bank[0]["A"] = Port_Registers("A",[
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
            ], self.device)
        self.Bank[0]["B"] = Port_Registers("B",[
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
            ], self.device)
        self.Bank[1]["A"] = Port_Registers("A",[
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
            ], self.device)
        self.Bank[1]["B"] = Port_Registers("B",[
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
            ], self.device)

#-------------------------------------------------
# Functionality
#-------------------------------------------------

class Pin:
    def __init__(self, id, address, port):
        self.id = id
        self.address = address
        self.port = port
        self.device = port.device
    
    def set_value(self, state):
        self.value = state
        return self.port

    @property
    def value(self):
        return  "TODO: Return Pin State"

    @value.setter
    def value(self, state):
        if State.HIGH == state:
            state_new = (0xff & self.address)
        if State.LOW == state:
            state_new = 0x00
        state_current = self.device.Registers.Bank[self.device.BANK][self.port.id].OLAT
        state_current = (state_current & ~self.address)
        data = (state_new | state_current)
        self.device.Registers.Bank[self.device.BANK][self.port.id].GPIO = data

class Port:
    def __init__(self, device, id):
        self.id = id
        self.device = device
        self.reset()
        self.load_pins()
    
    def load_pins(self):
        self.Pin = {}
        self.Pin["GP0"] = Pin("GP0",0b00000001, self)
        self.Pin["GP0"] = Pin("GP0",0b00000001, self)
        self.Pin["GP1"] = Pin("GP1",0b00000010, self)
        self.Pin["GP2"] = Pin("GP2",0b00000100, self)
        self.Pin["GP3"] = Pin("GP3",0b00001000, self)
        self.Pin["GP4"] = Pin("GP4",0b00010000, self)
        self.Pin["GP5"] = Pin("GP5",0b00100000, self)
        self.Pin["GP6"] = Pin("GP6",0b01000000, self)
        self.Pin["GP7"] = Pin("GP7",0b10000000, self)

    def reset(self):
        self._direction = Direction.IN
        self._value = State.LOW
        return

    def exist(self):
        return self.device
        
    def set_direction(self, direction):
        """
        Fluent API to set Direction of GPIO Pins on Port
        """
        self.direction = direction
        return self.device
    
    def set_value(self, state):
        """
        Fluent API to set the State of GPIO Pins on Port
        """
        self.value = state
        return self.device
    
    @property
    def direction(self):
        """
        Set Direction of GPIO Pins on Port
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        if self._direction == direction:
            return
        if direction == Direction.IN:
            # TODO: Remove hard coded values
            self.device.Registers.Bank[self.device.BANK][self.id].IODIR = 0xff
            self._direction = Direction.IN
        if direction == Direction.OUT:
            # TODO: Remove hard coded values
            self.device.Registers.Bank[self.device.BANK][self.id].IODIR = 0x00
            self._direction = Direction.OUT

    @property
    def value(self):
        """
        Set State of GPIO Pins on Port
        """
        return self._direction
   
    @value.setter
    def value(self, state):
        if self._value == state:
            return
        if state == State.LOW:
            # TODO: Remove hard coded values
            self.device.Registers.Bank[self.device.BANK][self.id].GPIO = 0x00
            self._value = State.LOW
        if state == State.HIGH:
            # TODO: Remove hard coded values
            self.device.Registers.Bank[self.device.BANK][self.id].GPIO = 0xff
            self._value = State.HIGH

class GPIO:
    def __init__(self, device):
        self.device = device
        self.load_ports(device)
        self.reset()
    
    def load_ports(self, device):
        self.Port = {}
        for port in device.PORTS:
            self.Port[port] = Port(device, port)

    def reset(self):
        for port in self.Port:
            self.Port[port].reset()
        return self.device

    def set_direction(self, direction):
        """
        Fluent API to set Direction of all GPIO Pins
        """
        if direction == Direction.IN:
            for port in self.Port:
                self.Port[port].direction = Direction.IN
        if direction == Direction.OUT:
            for port in self.Port:
                self.Port[port].direction = Direction.OUT
        return self.device
    
    def set_value(self, state):
        """
        Fluent API to set the State of all GPIO Pins
        """
        if state == State.LOW:
            for port in self.Port:
                self.Port[port].value = State.LOW
        if state == State.HIGH:
            for port in self.Port:
                self.Port[port].value = State.HIGH
        return self.device


# HID for I2C, GPIO, ADC, DEC. CDC for USB-to-UART

#------------------------------------------------------------------
# USB HID Commands/Responses
#------------------------------------------------------------------
# STATUS/SET PARAMETERS
# -----------------------------------------------------------------
# READ FLASH DATA
# WRITE FLASH DATA
# -----------------------------------------------------------------
# SEND FLASH ACCESS PASSWORD
# -----------------------------------------------------------------
# I2C WRITE DATA
# I2C WRITE DATA REPEATED-START
# I2C WRITE DATA NO STOP
# I2C READ DATA
# I2C READ DATA REPEATED-START
# I2C READ DATA - GET I2C DATA
# -----------------------------------------------------------------
# SET GPIO OUTPUT VALUES
# GET GPIO VALUES
# -----------------------------------------------------------------
# SET SRAM SETTINGS
# GET SRAM SETTINGS
# -----------------------------------------------------------------
# RESET CHIP
# -----------------------------------------------------------------





class MCP2221:
    I2C_ADDRESS_RANGE = [
        0x20, 
        0x21,
        0x22,
        0x23,
        0x24,
        0x25,
        0x26,
        0x27
        ]
    """
    MCP23018 I2C Address is configurable via an analog input on ADDR pin.
    A total of 8 addresses is available and configurable via a voltage devider circuit.
    Setting ADDR = VDD will set the I2C Address to 0x27 (0b100111)
    Setting the ADDR = VSS will set the I2C Address to 0x20 (0b100000)
    See MCP23018 datasheet Figure 1-2 and Figure 1-3 for more details.
    """
    I2C_ADDRESS = 0x20
    """
    Connecting ADDR to VSS will set the device I2C Address to 0x20
    """
    MEMORY_BANKS = [0, 1]
    """
    Memory Banks are controlled via bit 7 for IOCON Regsiter 
    """
    BANK = 0
    """
    Default Memory Bank in use after Reset is 0 
    """
    PORTS = ["A", "B"]

    def __init__(self, reset_pin, i2c_interface, i2c_address= 0x20):
        self.set_address(i2c_address)
        self.RESET_PIN = reset_pin
        self.I2C = i2c_interface
        self.Registers = Register(self)
        self.GPIO = GPIO(self)
        self.reset()
    
    def reset(self):
        self.RESET_PIN.value = True
        self.RESET_PIN.value = False
        self.RESET_PIN.value = True
        self.GPIO.reset()
        return self
    
    def set_address(self, i2c_address):
        """
        Sets the I2C Address of the MCP23018 or raise an exception if invalid value are provided.
        """
        if self.I2C_ADDRESS == i2c_address:
            return
        if i2c_address not in self.I2C_ADDRESS_RANGE:
            raise Exception("Invalid I2C Address")
        self.I2C_ADDRESS = i2c_address

    def set_bank(self, bank):
        if bank not in self.MEMORY_BANKS:
            raise Exception("Invalid memory bank")
        self.MEMORY_BANKS = bank

    def wait(self, duration):
        time.sleep(duration)
        return self

    def write_to(self, register, data):
        self.I2C.writeto(self.I2C_ADDRESS, bytes([register.value, data]))
    
    def read_from(self, register):
        data = bytearray(1)
        self.I2C.writeto(self.I2C_ADDRESS, bytes([register.value]))
        self.I2C.readfrom_into(self.I2C_ADDRESS, data)
        data = int.from_bytes(data,"big")
        return data