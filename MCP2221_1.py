import hid
"""
Library to interface with USB HID-Class devices on Windows, Linux, FreeBSD, and macOS.
"""
from enum import Enum, auto
import time

from ENUMS import DIRECTION, STATE

class I2C_SPEED(Enum):
    STANDARD = 100000
    FAST = 400000
    HIGH = 3400000

class PARAMETER(Enum):
    I2C_SPEED = 'I2C_SPEED'

class MODE(Enum):
    GPIO = 0b000
    SSPND = 0b001
    CLK = 0b001
    USBCFG = 0b001
    LED_I2C = 0b001
    ADC = 0b010
    LED_RX = 0b010
    LED_TX = 0b011
    DAC = 0b011
    INTRP = 0b100

class DRIVE_MODE(Enum):
    PUSH_PULL = 'PUSH_PULL'
    OPEN_DRAIN = 'OPEN_DRAIN'

MCP2221_MAX_I2C_DATA_LEN    = 60
MCP2221_RETRY_MAX           = 50
RESP_I2C_START_TOUT         = 0x12
RESP_I2C_WRADDRL_TOUT       = 0x23
RESP_ADDR_NACK              = 0x25
RESP_I2C_WRADDRL_NACK       = 0x25
RESP_I2C_PARTIALDATA        = 0x41
RESP_I2C_WRDATA_TOUT        = 0x44
RESP_I2C_WRITINGNOSTOP      = 0x45
RESP_I2C_STOP_TOUT          = 0x62
MASK_ADDR_NACK              = 0x40
RESP_READ_ERR               = 0x7F
RESP_READ_COMPL             = 0x55
RESP_READ_PARTIAL           = 0x54

class MCP2221:
    GP_GPIO = 0b000
    GP_DEDICATED = 0b001
    GP_ALT0 = 0b010
    GP_ALT1 = 0b011
    GP_ALT2 = 0b100

    HID_ReportSize = 64
    """
    The USB HID Protocol uses 64-byte reports
    """
    INETERNAL_CLOCK = 12000000
    """
    MCP2221 Internal Clock Frequency 12 MHz
    """
    GET_STATUS = bytearray([0x10, 0x00])
    """
    GET DEVICE STATUS
    Response on Page 24
    """
    SET_PARAMETER = bytearray([0x10, 0x00]) 
    """
    SET DEVICE STATUS
    Page 24
    """
    GET_I2C_DATA = bytearray([0x40])
    """
    GET I2C DATA
    Page 44
    """
    SET_GPIO_OUTPUT_VALUES = bytearray([0x50])
    """
    SET GPIO OUTPUT VALUES
    Page 45
    """
    GET_GPIO_VALUES = bytearray([0x51])
    """
    GET GPIO VALUES
    Page 48
    """
    SET_SRAM_SETTINGS = bytearray([0x60])
    """
    SET SRAM SETTINGS
    Page 49
    """
    GET_SRAM_SETTINGS = bytearray([0x61])
    """
    GET SRAM SETTINGS
    Page 53
    """
    RESET_CHIP = bytearray([0x70,
                            0xAB,
                            0xCD,
                            0xEF])
    """
    RESET CHIP command is used to force a Reset of the MCP2221 device. 
    This command is useful when the Flash memory is updated with new data. 
    The MCP2221 would need to be re-enumerated to see the new data
    This is the only command that does not expect a response.

    Page 57:
    Index | Functiona Descriptions | Value | 
    0     | Reset Chip             | 0x70  |
    1     |                        | 0xAB  |  
    2     |                        | 0xCD  |
    3     |                        | 0xEF  |
    4 - 63|                        | 0x00  |
    """
    WRITE_I2C_DATA = bytearray([0x90])
    """
    I2C WRITE DATA 
    Page 39
    """ 
    READ_I2C_DATA = bytearray([0x91])
    """
    READ I2C DATA
    Page 40
    """
    WRITE_I2C_REPEATED_START = bytearray([0x92])
    """
    I2C WRITE DATA REPEATED START
    Page 40
    """
    READ_I2C_REPEATED_START = bytearray([0x93])
    """
    I2C WRITE DATA REPEATED START
    Page 43
    """
    WRITE_I2C_NO_STOP = bytearray([0x94])
    """
    I2C WRITE DATA REPEATED START
    Page 41
    """
    READ_FLASH_DATA = bytearray([0xB0])
    """
    READ FLASH DATA
    Page 26
    """
    WRITE_FLASH_DATA = bytearray([0xB1]) 
    """
    WRITE FLASH DATA
    Page 32
    """
    SEND_FLASH_ACCESS_PASSWORD = bytearray([0xB2])
    """
    SEND FLASH ACCESS PASSWORD
    Page 32
    """
    EMPTY_REPORT = bytearray([0x00]) * 63
    CANCEL_TRANSFER = bytearray([0x10])
    """
    CANCEL I2C TRANSFER 
    Page 23
    """
    SET_I2C_SPEED = lambda speed:bytearray([0x00,
                                            0x20,
                                            MCP2221.INETERNAL_CLOCK // speed.value - 3])
    """
    SET I2C SPEED 
    Typical Values
    Standard mode   = 100 Kbps
    Fast mode       = 400 Kbps
    High Speed mode = 3.4 Mbps
    Page 23
    """
    VID = 0x04D8
    """
    Vendor ID factory default = 0x04D8
    Using Microchip provided utility the Vendor ID can be customized
    """
    PID = 0x00DD
    """
    Product ID factory default = 0x00DD
    Using Microchip provided utility the Product ID can be customized
    """
    SET_PIN_MODE = bytearray([0x00,
                              0x00,
                              0x00,
                              0x00,
                              0x00,
                              0x00,
                              0xff]) + bytearray([0x00]) * 56
    SET_VALUE = lambda pin: 2 + 4 * pin
    GET_VALUE = lambda pin: 2 + 2 * pin
    SET_DIRECTION = lambda pin: 4 * (pin + 1)

    def __init__(self):
        self._hid = hid.device()
        self._hid.open(MCP2221.VID, MCP2221.PID)
        self._reset()
        time.sleep(0.5) #Required to stop Freezing

    def _hid_xfer(self, report, response=True):
        """
        used to transfer a 64 byte data report
        first byte is the report ID and set to 0 for MCP2221
        """
        self._hid.write(b'\0' + report + b'\0'*(MCP2221.HID_ReportSize-len(report)))
        if response:
            return self._hid.read(MCP2221.HID_ReportSize)

    def _reset(self):
        """
        Reset device by sending Reset Chip command.
        After reset a new connection is openend. 
        """
        print('MCP2221: RESET')
        self._hid_xfer(MCP2221.RESET_CHIP, response=False)
        start = time.monotonic()
        while time.monotonic() - start < 5:
            try:
                self._hid.open(MCP2221.VID, MCP2221.PID)
            except OSError:
                time.sleep(0.1)
                continue
            return
        raise OSError("open failed")

    def reset(self):
        pass

    def wait(self, duration):
        """
        Use external library to Wait for a specified number of seconds
        """
        time.sleep(duration)

    def i2c_configure(self, speed):
        if speed in I2C_SPEED:
            print('MCP2221 CONFIG - Type: set Parameter: ', PARAMETER.I2C_SPEED, 'Value: ', speed)
            self._hid_xfer(MCP2221.SET_PARAMETER + MCP2221.SET_I2C_SPEED(speed))
        else:
            raise Exception("Invalid configuration")
    
    def _i2c_status(self):
        device_status = self._hid_xfer(MCP2221.GET_STATUS)
        successfull = 0
        if device_status[1] != successfull:
            raise RuntimeError("Get Device Status Failed")
        return device_status
    
    def _i2c_state(self):
        I2C_state = self._i2c_status()[8]
        return I2C_state

    def _i2c_cancel(self):
        device_status = self._hid_xfer(MCP2221.SET_PARAMETER + MCP2221.CANCEL_TRANSFER)
        successfull = 0
        if device_status[1] != successfull:
            raise RuntimeError("Get Device Status Failed")

        request_status = device_status[2]
        if request_status != successfull:
            raise RuntimeError("I2C Transfer Cancel Request Failed")

        if request_status == 0x10:
            print('MCP2221 I2C Transfer Cancel Request In-Progress')
            time.sleep(0.001)

    def _i2c_write(self, address, buffer, start=0, end=None):
        """
        cmd: 0x90 (I2C Write Data Command)
        address: I2C Slave Address 
        buffer: bytes([register_address, data])
        """

        # Check Status of Interernal I2C Module
        I2C_state = self._i2c_state()
        successfull = 0x00
        if I2C_state != successfull:
            self._i2c_cancel()

        # Calculate end position
        end = end if end else len(buffer)
        length = end - start
        retries = 0

        while (end - start) > 0:
            chunk = min(end - start, MCP2221_MAX_I2C_DATA_LEN)
            # write out current chunk
            response = self._hid_xfer(MCP2221.WRITE_I2C_DATA + bytes([length & 0xFF,
                                                   (length >> 8) & 0xFF,
                                                   address << 1]) +
                                                   buffer[start:(start+chunk)])
            # check for success
            transfer_status = response[1]
            I2C_enginge_status = response[2]
            successfull = 0x00
            if transfer_status != successfull:
                # TODO: Check the meaning of each and raise correct error
                if I2C_enginge_status in (RESP_I2C_START_TOUT,
                                          RESP_I2C_WRADDRL_TOUT,
                                          RESP_I2C_WRADDRL_NACK,
                                          RESP_I2C_WRDATA_TOUT,
                                          RESP_I2C_STOP_TOUT):
                    raise RuntimeError("I2C write failure")
                
                # Retry if failed
                retries += 1
                if retries >= MCP2221_RETRY_MAX:
                    raise RuntimeError("I2C write error, max retries reached.")
                time.sleep(0.001)
                continue

            # Wait until I2C Ready for next write
            while self._i2c_state() == RESP_I2C_PARTIALDATA:
                time.sleep(0.001)

            # Change start position of next chunk and reset retries    
            start += chunk
            retries = 0

        # check status in another loop
        for _ in range(MCP2221_RETRY_MAX):
            status = self._i2c_status()
            if status[20] & MASK_ADDR_NACK:
                raise RuntimeError("I2C slave address was NACK'd")
            I2C_state = status[8]
            if I2C_state == 0:
                break
            # Command always 0x90 for I2C Write, TODO: Investigate
            if I2C_state == RESP_I2C_WRITINGNOSTOP and cmd == 0x94:
                break   # this is OK too!
            if I2C_state in (RESP_I2C_START_TOUT,
                                  RESP_I2C_WRADDRL_TOUT,
                                  RESP_I2C_WRADDRL_NACK,
                                  RESP_I2C_WRDATA_TOUT,
                                  RESP_I2C_STOP_TOUT):
                raise RuntimeError("Unrecoverable I2C state failure")
            time.sleep(0.001)
        else:
            raise RuntimeError("I2C write error: max retries reached.")

    def _i2c_read(self, address, buffer, start=0, end=None):
        if self._i2c_state() not in (RESP_I2C_WRITINGNOSTOP, 0):
            self._i2c_cancel()

        end = end if end else len(buffer)
        length = end - start

        # tell it we want to read
        resp = self._hid_xfer(MCP2221.READ_I2C_DATA + bytes([length & 0xFF,
                                          (length >> 8) & 0xFF,
                                          (address << 1) | 0x01]))

        # check for success
        if resp[1] != 0x00:
            raise RuntimeError("Unrecoverable I2C read failure")

        # and now the read part
        while (end - start) > 0:
            for retry in range(MCP2221_RETRY_MAX):
                # the actual read
                resp = self._hid_xfer(MCP2221.GET_I2C_DATA)
                # check for success
                if resp[1] == RESP_I2C_PARTIALDATA:
                    time.sleep(0.001)
                    continue
                if resp[1] != 0x00:
                    raise RuntimeError("Unrecoverable I2C read failure")
                if resp[2] == RESP_ADDR_NACK:
                    raise RuntimeError("I2C NACK")
                if resp[3] == 0x00 and resp[2] == 0x00:
                    break
                if resp[3] == RESP_READ_ERR:
                    time.sleep(0.001)
                    continue
                if resp[2] in (RESP_READ_COMPL, RESP_READ_PARTIAL):
                    break

            # move data into buffer
            chunk = min(end - start, 60)
            for i, k in enumerate(range(start, start+chunk)):
                buffer[k] = resp[4 + i]
            start += chunk
    
    def i2c_writeto(self, address, buffer, *, start=0, end=None):
        """
        address: I2C Slave Address 
        buffer: bytes([register_address, data])
        """
        self._i2c_write(address, buffer, start, end)
    
    def i2c_readfrom_into(self, address, buffer, *, start=0, end=None):
        """
        address: I2C Slave Address
        buffer: bytesarray(x) used to load response into
        """
        self._i2c_read(address, buffer, start, end)

    def gp_get_mode(self, pin):
        report = self._hid_xfer(MCP2221.GET_SRAM_SETTINGS)
        return report[22+pin] & 0x07
    
    def load_current_pin_mode(self, report):
        current = self._hid_xfer(MCP2221.GET_SRAM_SETTINGS)
        report[8]  = current[22]  # GP0
        report[9]  = current[23]  # GP1
        report[10] = current[24]  # GP2
        report[11] = current[25]  # GP3
        return report

    def gp_set_mode(self, pin, mode):
        report = MCP2221.SET_SRAM_SETTINGS + MCP2221.SET_PIN_MODE
        report = self.load_current_pin_mode(report)
        # set pin mode 
        parameter = 8 + pin
        # TODO: rather use << 0x07
        mask = lambda value: value & 0x07
        report[parameter] = mask(mode.value) 
        # and make it so
        self._hid_xfer(report)

    def update_report(self, report, offset, value):
        report[offset] = 0x01
        report[offset + 1] = value
        return report

    def gpio_set_direction(self, pin, direction):
        # report is adjusted based on pin number and expected pin state
        report = MCP2221.SET_GPIO_OUTPUT_VALUES + MCP2221.EMPTY_REPORT
        offset = MCP2221.SET_DIRECTION(pin)
        report = self.update_report(report, offset, direction.value)
        self._hid_xfer(report)

    def gpio_get_pin(self, pin):
        report = self._hid_xfer(MCP2221.GET_GPIO_VALUES)
        # Based on pin number read specific position in report
        offset = MCP2221.GET_VALUE(pin)
        if report[offset] == 0xEE:
            raise RuntimeError("Pin is not set for GPIO operation.")
        else:
            state = STATE(report[offset])
            return state
    
    def gpio_set_pin(self, pin, state):
        # report is adjusted based on pin number and expected pin state
        report = MCP2221.SET_GPIO_OUTPUT_VALUES + MCP2221.EMPTY_REPORT
        offset = MCP2221.SET_VALUE(pin)
        report = self.update_report(report, offset, state.value)
        self._hid_xfer(report)

mcp2221 = MCP2221()

class I2C():
    def __init__(self, *, frequency=I2C_SPEED.FAST):
        self._mcp2221 = mcp2221
        self._mcp2221.i2c_configure(frequency)
    
    def writeto(self, address, buffer):
        """
        address: I2C Slave Address 
        buffer: bytes([register_address, data])
        """
        self._mcp2221.i2c_writeto(address, buffer, start=0, end=None)

    def readfrom_into(self, address, buffer):
        """
        address: I2C Slave Address
        buffer: bytesarray(x) used to load response into
        """
        self._mcp2221.i2c_readfrom_into(address, buffer, start=0, end=None)

class Pin:
    def __init__(self, pin_id=None):
        self.id = pin_id
        self._direction = None

    def init(self, direction):
        mcp2221.gp_set_mode(self.id, MODE.GPIO)
        mcp2221.gpio_set_direction(self.id, direction)
        self._direction = direction

    @property
    def value(self):
        state = mcp2221.gpio_get_pin(self.id)
        return state
    
    @value.setter
    def value(self, state):
        mcp2221.gpio_set_pin(self.id, state)
    
    @property
    def direction(self):
        return self.__direction
    
    @direction.setter
    def direction(self, direction):
        self.__direction = direction
        if direction is DIRECTION.OUT:
            self.init(direction=DIRECTION.OUT)
            self.value = STATE.LOW
        elif direction is DIRECTION.IN:
            self.init(direction=DIRECTION.IN)
        else:
            raise AttributeError("Not a Direction")

