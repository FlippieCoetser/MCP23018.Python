class MCP23018:
    I2C_ADDRESS = 0x20
    state = {
        "HIGH" : 0x0f,
        "LOW" : 0x00
    }
    registers_bank0 = {
        "IODIRA" : 0x00,
        "IODIRB": 0x01,
        "IPOLA" : 0x02,
        "IPOLB" : 0x03,
        "GPINTENA" : 0x04,
        "GPINTENB" : 0x05,
        "DEFVALA" : 0x06,
        "DEFVALB" : 0x07,
        "INTCONA" : 0x08,
        "INTCONB" : 0x09,
        "IOCONA" : 0x0a,
        "IOCONB" : 0x0b,
        "GPPUA" : 0x0c,
        "GPPUB" : 0x0d,
        "INTFA" : 0x0e,
        "INTFB" : 0x0f,
        "INTCAPA" : 0x10,
        "INTCAPB" : 0x11,
        "GPIOA" : 0x12,
        "GPIOB" : 0x13,
        "OLATA" : 0x14,
        "OLATB" : 0x15
    } 
    def __init__(self, reset_pin, i2c):
        self.reset_pin = reset_pin
        self.i2c = i2c
        self.reset()

    def reset(self):
        self.reset_pin.value = True
        self.reset_pin.value = False
        self.reset_pin.value = True

    def configure_port_a(self):
        register = self.registers_bank0['IODIRA'] 
        data = self.state['LOW']
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register,data]))
    
    def set_port_a_high(self):
        register = self.registers_bank0['GPIOA']
        data = self.state['HIGH']
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register, data]))
    
    def set_port_a_low(self):
        register = self.registers_bank0['GPIOA']
        data = self.state['LOW']
        self.i2c.writeto(self.I2C_ADDRESS, bytes([register, data]))
