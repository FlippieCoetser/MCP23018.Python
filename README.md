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

The test.py file contains some example code which has been tested on windows 10

### Standard API
#### Device Level
1. Reset Device
```python
mcp23018.reset()
```
2. Wait
```python
mcp23018.wait(duration)
```
#### GPIO Level
1. Set Direction of all GPIO Pins
```python
mcp23018.GPIO.direction = Direction.OUT
```
2. Set State of all GPIO Pins
```python
mcp23018.GPIO.value = State.LOW
```
#### Port Level
1. Set Direction of all GPIO Pins on specific Port (A or B)
```python
mcp23018.GPIO.Ports["A"].direction = Direction.OUT
```
2. Set State of all GPIO Pins on specific Port (A or B)
```python
mcp23018.GPIO.Ports["A"].value = State.LOW
```

### Fluent API
Using the Fluent API it is possible to chain different oprations.
See the below example, which should speak for itself:

```python
(mcp23018
    .reset()
    .wait(1)
    .GPIO.set_value(State.HIGH)
    .GPIO.set_direction(Direction.OUT)
    .wait(1)
    .GPIO.Ports["A"].set_value(State.LOW)
    .wait(1)
    .GPIO.Ports["B"].set_value(State.LOW)
    .wait(1)
    .GPIO.Ports["A"].set_value(State.HIGH)
    .wait(1)
    .GPIO.Ports["B"].set_value(State.HIGH))
```
