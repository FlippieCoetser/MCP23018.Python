# MCP23018.Python
Python Library for Microchip MCP23018 16-bit I/O Expander with Open-Drain Outputs

### Dependencies
Boards: USB I2C Click  
Libraries: 
1. hidapi
```
pip install hidapi
```
2. blinka
```
pip install adafruit-blinka
```

Note: click [here](https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/overview) for instructions how to setup your environment to use the USB I2C Click with circuitpython

**This library is work in progress**  

The test.py file contains example code which has been tested on windows 10


To use library, instantiate MCP23018 as follows
```python
mcp23018 = MCP23018(RESET_Pin = pin, I2C_Interface=I2C)
```
### MCP23018 API
#### General
1. Reset Device
```python
mcp23018.reset()
```
2. Wait x seconds
```python
mcp23018.wait(x)
```
#### Debugging
Debugging on all modules are by default switched off
1. Switch External RESET_PIN debugging on
```python
mcp23018.RESET.debug = True
```
2. Switch External I2C Interface debugging on
```python
mcp23018.I2C = True
```
3. Switch Configuration Module debugging on
```python
mcp23018.Configuration.debug = True
```
4. Switch specific GPIO PIN debugging on
```python
mcp23018.GPIO.port[PORT.B].pin[PIN.GP5].debug = True
```
#### Device Configuration
1. Set Configuration Parameter
```python
mcp23018.Configuration.bank = PARAMETERS[PARAMETER.BANK].SEPARATE
```
2. Get Configuration Parameter
```python
configuration = mcp23018.Configuration.bank
```
#### All GPIO PINS 
1. Set all GPIO Pins value
```python
mcp23018.GPIO.value = STATE.LOW
```
2. Get all GPIO Pins value
```python
 state = mcp23018.GPIO.value
```
3. Set all GPIO Pins direction
```python
mcp23018.GPIO.direction = DIRECTION.OUT
```
4. Get all GPIO Pins direction
```python
direction = mcp23018.GPIO.direction
```
#### Specific PORT's GPIO PINS 
1. Set specific PORT GPIO Pins value
```python
mcp23018.GPIO.port[PORT.A].value = STATE.LOW
```
2. Get specific PORT GPIO Pins value
```python
state = mcp23018.GPIO.port[PORT.A].value
```
3. Set specific PORT GPIO Pins direction
```python
mcp23018.GPIO.port[PORT.A].direction = DIRECTION.OUT
```
4. Get specific PORT GPIO Pins direction
```python
mcp23018.GPIO.port[PORT.A].direction = DIRECTION.OUT
```
#### Specific GPIO PIN
1. Set specific GPIO Pins value
```python
mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].value = STATE.LOW
```
2. Get specific GPIO Pins value
```python
state = mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].value
```
3. Set specific GPIO Pins direction
```python
mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].direction = DIRECTION.OUT
```
4. Get specific GPIO Pins direction
```python
direction = mcp23018.GPIO.port[PORT.A].pin[PIN.GP0].direction
```

