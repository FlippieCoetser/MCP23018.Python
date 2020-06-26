import time
import hid

# from the C driver
# http://ww1.microchip.com/downloads/en/DeviceDoc/mcp2221_0_1.tar.gz
# others (???) determined during driver developement
# pylint: disable=bad-whitespace
RESP_ERR_NOERR              = 0x00
RESP_ADDR_NACK              = 0x25
RESP_READ_ERR               = 0x7F
RESP_READ_COMPL             = 0x55
RESP_READ_PARTIAL           = 0x54 # ???
RESP_I2C_IDLE               = 0x00
RESP_I2C_START_TOUT         = 0x12
RESP_I2C_RSTART_TOUT        = 0x17
RESP_I2C_WRADDRL_TOUT       = 0x23
RESP_I2C_WRADDRL_WSEND      = 0x21
RESP_I2C_WRADDRL_NACK       = 0x25
RESP_I2C_WRDATA_TOUT        = 0x44
RESP_I2C_RDDATA_TOUT        = 0x52
RESP_I2C_STOP_TOUT          = 0x62

RESP_I2C_MOREDATA           = 0x43 # ???
RESP_I2C_PARTIALDATA        = 0x41 # ???
RESP_I2C_WRITINGNOSTOP      = 0x45 # ???

MCP2221_RETRY_MAX           = 50
MCP2221_MAX_I2C_DATA_LEN    = 60
MASK_ADDR_NACK              = 0x40
# pylint: enable=bad-whitespace

class MCP2221:

    VID = 0x04D8
    PID = 0x00DD

    GP_GPIO = 0b000
    GP_DEDICATED = 0b001
    GP_ALT0 = 0b010
    GP_ALT1 = 0b011
    GP_ALT2 = 0b100

    def __init__(self):
        self._hid = hid.device()
        self._hid.open(MCP2221.VID, MCP2221.PID)
        self._reset()
        time.sleep(0.25)

    def _hid_xfer(self, report, response=True):
        # first byte is report ID, which =0 for MCP2221
        # remaing bytes = 64 byte report data
        # https://github.com/libusb/hidapi/blob/083223e77952e1ef57e6b77796536a3359c1b2a3/hidapi/hidapi.h#L185
        self._hid.write(b'\0' + report + b'\0'*(64-len(report)))
        if response:
            # return is 64 byte response report
            return self._hid.read(64)

    #----------------------------------------------------------------
    # MISC
    #----------------------------------------------------------------
    def gp_get_mode(self, pin):
        return self._hid_xfer(b'\x61')[22+pin] & 0x07

    def gp_set_mode(self, pin, mode):
        # get current settings
        current = self._hid_xfer(b'\x61')
        # empty report, this is safe since 0's = no change
        report = bytearray(b'\x60'+b'\x00'*63)
        # set the alter GP flag byte
        report[7] = 0xFF
        # each pin can be set individually
        # but all 4 get set at once, so we need to
        # transpose current settings
        report[8]  = current[22]  # GP0
        report[9]  = current[23]  # GP1
        report[10] = current[24]  # GP2
        report[11] = current[25]  # GP3
        # then change only the one
        report[8+pin] = mode & 0x07
        # and make it so
        self._hid_xfer(report)

    def _pretty_report(self, report):
        print("     0  1  2  3  4  5  6  7  8  9")
        index = 0
        for row in range(7):
            print("{} : ".format(row), end='')
            for _ in range(10):
                print("{:02x} ".format(report[index]), end='')
                index += 1
                if index > 63:
                    break
            print()

    def _status_dump(self):
        self._pretty_report(self._hid_xfer(b'\x10'))

    def _sram_dump(self):
        self._pretty_report(self._hid_xfer(b'\x61'))

    def _reset(self):
        self._hid_xfer(b'\x70\xAB\xCD\xEF', response=False)
        start = time.monotonic()
        while time.monotonic() - start < 5:
            try:
                self._hid.open(MCP2221.VID, MCP2221.PID)
            except OSError:
                # try again
                time.sleep(0.1)
                continue
            return
        raise OSError("open failed")

    #----------------------------------------------------------------
    # GPIO
    #----------------------------------------------------------------
    def gpio_set_direction(self, pin, mode):
        report = bytearray(b'\x50'+b'\x00'*63)  # empty set GPIO report
        offset = 4 * (pin + 1)
        report[offset] = 0x01                   # set pin direction
        report[offset+1] = mode                 # to this
        self._hid_xfer(report)

    def gpio_set_pin(self, pin, value):
        report = bytearray(b'\x50'+b'\x00'*63)  # empty set GPIO report
        offset = 2 + 4 * pin
        report[offset] = 0x01                   # set pin value
        report[offset+1] = value                # to this
        self._hid_xfer(report)

    def gpio_get_pin(self, pin):
        resp = self._hid_xfer(b'\x51')
        offset = 2 + 2 * pin
        if resp[offset] == 0xEE:
            raise RuntimeError("Pin is not set for GPIO operation.")
        else:
            return resp[offset]

    #----------------------------------------------------------------
    # I2C
    #----------------------------------------------------------------
    def _i2c_status(self):
        resp = self._hid_xfer(b'\x10')
        if resp[1] != 0:
            raise RuntimeError("Couldn't get I2C status")
        return resp

    def _i2c_state(self):
        return self._i2c_status()[8]

    def _i2c_cancel(self):
        resp = self._hid_xfer(b'\x10\x00\x10')
        if resp[1] != 0x00:
            raise RuntimeError("Couldn't cancel I2C")
        if resp[2] == 0x10:
            # bus release will need "a few hundred microseconds"
            time.sleep(0.001)

    def _i2c_write(self, cmd, address, buffer, start=0, end=None):
        if self._i2c_state() != 0x00:
            self._i2c_cancel()

        end = end if end else len(buffer)
        length = end - start
        retries = 0

        while (end - start) > 0:
            chunk = min(end - start, MCP2221_MAX_I2C_DATA_LEN)
            # write out current chunk
            resp = self._hid_xfer(bytes([cmd,
                                         length & 0xFF,
                                         (length >> 8) & 0xFF,
                                         address << 1]) +
                                         buffer[start:(start+chunk)])
            # check for success
            if resp[1] != 0x00:
                if resp[2] in (RESP_I2C_START_TOUT,
                               RESP_I2C_WRADDRL_TOUT,
                               RESP_I2C_WRADDRL_NACK,
                               RESP_I2C_WRDATA_TOUT,
                               RESP_I2C_STOP_TOUT):
                    raise RuntimeError("Unrecoverable I2C state failure")
                retries += 1
                if retries >= MCP2221_RETRY_MAX:
                    raise RuntimeError("I2C write error, max retries reached.")
                time.sleep(0.001)
                continue # try again
            # yay chunk sent!
            while self._i2c_state() == RESP_I2C_PARTIALDATA:
                time.sleep(0.001)
            start += chunk
            retries = 0

        # check status in another loop
        for _ in range(MCP2221_RETRY_MAX):
            status = self._i2c_status()
            if status[20] & MASK_ADDR_NACK:
                raise RuntimeError("I2C slave address was NACK'd")
            usb_cmd_status = status[8]
            if usb_cmd_status == 0:
                break
            if usb_cmd_status == RESP_I2C_WRITINGNOSTOP and cmd == 0x94:
                break   # this is OK too!
            if usb_cmd_status in (RESP_I2C_START_TOUT,
                                  RESP_I2C_WRADDRL_TOUT,
                                  RESP_I2C_WRADDRL_NACK,
                                  RESP_I2C_WRDATA_TOUT,
                                  RESP_I2C_STOP_TOUT):
                raise RuntimeError("Unrecoverable I2C state failure")
            time.sleep(0.001)
        else:
            raise RuntimeError("I2C write error: max retries reached.")
        # whew success!

    def _i2c_read(self, cmd, address, buffer, start=0, end=None):
        if self._i2c_state() not in (RESP_I2C_WRITINGNOSTOP, 0):
            self._i2c_cancel()

        end = end if end else len(buffer)
        length = end - start

        # tell it we want to read
        resp = self._hid_xfer(bytes([cmd,
                                     length & 0xFF,
                                     (length >> 8) & 0xFF,
                                     (address << 1) | 0x01]))

        # check for success
        if resp[1] != 0x00:
            raise RuntimeError("Unrecoverable I2C read failure")

        # and now the read part
        while (end - start) > 0:
            for retry in range(MCP2221_RETRY_MAX):
                # the actual read
                resp = self._hid_xfer(b'\x40')
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

    def i2c_configure(self, baudrate=100000):
        self._hid_xfer(bytes([0x10,  # set parameters
                              0x00,  # don't care
                              0x00,  # no effect
                              0x20,  # next byte is clock divider
                              12000000 // baudrate - 3]))

    def i2c_writeto(self, address, buffer, *, start=0, end=None):
        self._i2c_write(0x90, address, buffer, start, end)

    def i2c_readfrom_into(self, address, buffer, *, start=0, end=None):
        self._i2c_read(0x91, address, buffer, start, end)

  
mcp2221 = MCP2221()


class Pin:
    """A basic Pin class for use with MCP2221."""

    # pin modes
    OUT = 0
    IN = 1
    ADC = 2
    DAC = 3
    # pin values
    LOW = 0
    HIGH = 1

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None

    def init(self, mode=IN, pull=None):
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if mode in (Pin.IN, Pin.OUT):
            # All pins can do GPIO
            mcp2221.gp_set_mode(self.id, mcp2221.GP_GPIO)
            mcp2221.gpio_set_direction(self.id, mode)
        else:
            raise ValueError("Incorrect pin mode: {}".format(mode))
        self._mode = mode

    def value(self, val=None):
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return mcp2221.gpio_get_pin(self.id)
            # digital write
            elif val in (Pin.LOW, Pin.HIGH):
                mcp2221.gpio_set_pin(self.id, val)
            # nope
            else:
                raise ValueError("Invalid value for pin.")
        else:
            raise RuntimeError("No action for mode {} with value {}".format(self._mode, val))

# create pin instances for each pin
G0 = Pin(0)

class Enum():
    """
        Object supporting CircuitPython-style of static symbols
        as seen with Direction.OUTPUT, Pull.UP
    """

    def __repr__(self):
        """
        Assumes instance will be found as attribute of own class.
        Returns dot-subscripted path to instance
        (assuming absolute import of containing package)
        """
        cls = type(self)
        for key in dir(cls):
            if getattr(cls, key) is self:
                return "{}.{}.{}".format(cls.__module__, cls.__qualname__, key)
        return repr(self)

    @classmethod
    def iteritems(cls):
        """
            Inspects attributes of the class for instances of the class
            and returns as key,value pairs mirroring dict#iteritems
        """
        for key in dir(cls):
            val = getattr(cls, key)
            if isinstance(cls, val):
                yield (key, val)


class ContextManaged:
    """An object that automatically deinitializes hardware with a context manager."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    # pylint: disable=no-self-use
    def deinit(self):
        """Free any hardware used by the object."""
        return
    # pylint: enable=no-self-use


class DriveMode(Enum):
    PUSH_PULL = None
    OPEN_DRAIN = None
DriveMode.PUSH_PULL = DriveMode()
DriveMode.OPEN_DRAIN = DriveMode()

class Direction(Enum):
    INPUT = None
    OUTPUT = None
Direction.INPUT = Direction()
Direction.OUTPUT = Direction()

class Pull(Enum):
    UP = None
    DOWN = None
Pull.UP = Pull()
Pull.DOWN = Pull()

class DigitalInOut(ContextManaged):
    _pin = None

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self.direction = Direction.INPUT

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, dir):
        self.__direction = dir
        if dir is Direction.OUTPUT:
            self._pin.init(mode=Pin.OUT)
            self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif dir is Direction.INPUT:
            self._pin.init(mode=Pin.IN)
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self):
        return self._pin.value() == 1

    @value.setter
    def value(self, val):
        if self.direction is Direction.OUTPUT:
            self._pin.value(1 if val else 0)
        else:
            raise AttributeError("Not an output")

    @property
    def pull(self):
        if self.direction is Direction.INPUT:
            return self.__pull
        else:
            raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul):
        if self.direction is Direction.INPUT:
            self.__pull = pul
            if pul is Pull.UP:
                self._pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
            elif pul is Pull.DOWN:
                if hasattr(Pin, "PULL_DOWN"):
                    self._pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)
                else:
                    raise NotImplementedError("unsupported")
            elif pul is None:
                self._pin.init(mode=Pin.IN, pull=None)
            else:
                raise AttributeError("Not a Pull")
        else:
            raise AttributeError("Not an input")

    @property
    def drive_mode(self):
        if self.direction is Direction.OUTPUT:
            return self.__drive_mode  #
        else:
            raise AttributeError("Not an output")

    @drive_mode.setter
    def drive_mode(self, mod):
        self.__drive_mode = mod
        if mod is DriveMode.OPEN_DRAIN:
            self._pin.init(mode=Pin.OPEN_DRAIN)
        elif mod is DriveMode.PUSH_PULL:
            self._pin.init(mode=Pin.OUT)

class I2C():

    def __init__(self, *, frequency=400000):
        self._mcp2221 = mcp2221
        self._mcp2221.i2c_configure(frequency)

    def writeto(self, address, buffer):
        self._mcp2221.i2c_writeto(address, buffer, start=0, end=None)

    def readfrom_into(self, address, buffer):
        self._mcp2221.i2c_readfrom_into(address, buffer, start=0, end=None)

