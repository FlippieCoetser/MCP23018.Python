# MCP2221

## Unmanaged DLL 
### Functions

#### Generic
1. Mcp2221_GetLibraryVersion  
  
Description: Returns the version number of the DLL  
Parameters:  
Inputs: None  
Outputs: (wchar_t*) version - variable that will store the library version. The library version is a 10 character wchar string.  
Returns: 0 for success or error code.  

2. Mcp2221_GetConnectedDevices  

Description: Gets the number of connected MCP2221s with the provided VID & PID.  
Parameters:  
Inputs:  
(unsigned int) vid - The vendor id of the MCP2221 devices to count  
(unsigned int) pid - The product id of the MCP2221 devices to count  
Outputs:
(unsigned int*) noOfDevs - The number of connected MCP2221s matching the provided VID and PID  
Returns: 0 if successful; error code otherwise  

#### Device Connection
1. Mcp2221_OpenByIndex  

Description: Attempt to open a connection with a MCP2221 with a specific index.  
Parameters:  
Inputs:  
(unsigned int) VID - The vendor ID of the MCP2221 to connect to(Microchip default = 0x4D8)  
(unsigned int) PID - The product ID of the MCP2221 to connect to(Microchip default = 0xDD)  
(unsigned int) index - The index of the MCP2221 to connect to. This value ranges from 0 to n-1, where n is the number of connected devices. This value can be obtained from "Mcp2221_GetConnectedDevices"  
Returns: (void*) - the handle value if the connection was successfully opened or INVALID_HANDLE_VALUE(-1) if not.  
NOTE: If the operation failed, call the Mcp2221_GetLastError method to get the error code  

2. Mcp2221_OpenBySN  

Description: Attempt to open a connection with a MCP2221 with a specific serial number.  
Parameters:  
Inputs:
(unsigned int) VID - The vendor ID of the MCP2221 to connect to.(Microchip default = 0x4D8)  
(unsigned int) PID - The product ID of the MCP2221 to connect to. Microchip default = 0xDD)  
(wchar_t*) serialNo - The serial number of the MCP2221 we want to connect to. Maximum 30 character value.  
Returns: (void*) - the handle value if the connection was successfully opened or INVALID_HANDLE_VALUE(-1) if not.  
NOTE: If the operation failed, call the Mcp2221_GetLastError method to get the error code.
If a connection to a matching device is already open, the function will fail with the "device not found" error.  

1. Mcp2221_Close  
Description: Attempt to close a connection to a MCP2221.  
Parameters:
(void*) handle - The handle for the device we'll close the connection to.  
Returns: (int) - 0 for success; error code otherwise.  

4. Mcp2221_CloseAll  
Description: Attempt to close all the currently opened MCP2221 connections.
If successful, all existing handles will be set to INVALID_HANDLE_VALUE  
Returns: (int) - 0 for success or the number of devices that failed to close.  

5. Mcp2221_Reset  
Description: Reset the MCP2221 and close its associated handle.  
Parameters:
(void*) handle - The handle for the device we'll reset. If successful, the handle will also be closed.  
Returns: (int) - 0 for success; error code otherwise.  

6. Mcp2221_GetLastError  
Description: Gets the last error value. Used only for the Open methods.  
Returns: (int) - The value for the last error code.  

#### I2C/SMBus
1. Mcp2221_SetSpeed  
Description: Set the communication speed for I2C/SMBus operations.  
Parameters:
(void*) handle - The handle for the device.  
(unsigned int) speed - the communication speed. Accepted values are between 46875 and 500000.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: The speed may fail to be set if an I2C/SMBus operation is already in progress or in a timeout situation. The "Mcp2221_I2cCancelCurrentTransfer" function can be used to free the bus before retrying to set the speed.  

2. Mcp2221_SetAdvancedCommParams  
Description: Set the time the MCP2221 will wait after sending the "read" command before trying to read back the data from the I2C/SMBus slave and the maximum number of retries if data couldn't be read back.  
Parameters:
(void*) handle - The handle for the device.  
(unsigned char) timeout - amount of time (in ms) to wait for the slave to send back data. Default 3ms.  
(unsigned char) maxRetries - the maximum amount of times we'll try to read data back from a slave. Default = 5  
Returns: (int) - 0 for success; error code otherwise.  

3. Mcp2221_I2cCancelCurrentTransfer  
Description: Cancel the current I2C/SMBus transfer  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
Returns: (int) - 0 for success; error code otherwise.  

4. Mcp2221_I2cRead  
Description: Read I2C data from a slave.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned int) bytesToRead - the number of bytes to read from the slave. Valid range is between 1 and 65535.  
(unsigned char) slaveAddress - 7bit or 8bit I2C slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0 - 7 bit address will be used for the slave. If 0 - 8 bit is used.  
Outputs:
(unsigned char*) i2cRxData - buffer that will contain the data bytes read from the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: if the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  

5. Mcp2221_I2cWrite  
Description: Write I2C data to a slave.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned int) bytesToWrite - the number of bytes to write to the slave. Valid range is between 0 and 65535.  
(unsigned char) slaveAddress - 7bit or 8bit I2C slave address, depending on the value of the "use7bitAddress" flag.For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char*) i2cTxData - buffer that will contain the data bytes to be sent to the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: if the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  

6. Mcp2221_I2cWriteNoStop  
Description: Write I2C data to a slave without sending the STOP bit.  
Parameters:  
Inputs: (void*) handle - the handle for the device.  
(unsigned int) bytesToWrite - the number of bytes to write to the slave. Valid range is between 0 and 65535.  
(unsigned char) slaveAddress - 7bit or 8bit I2C slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char*) i2cTxData - buffer that will contain the data bytes to be sent to the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: 1. The speed must be set via the "Mcp2221_SetSpeed" function before using this method. If the speed has not been set an error will be returned. 2. The SMBus Process Call command can be formed using Mcp2221_I2cWriteNoStop followed by Mcp2221_I2cReadRestart.  

7. Mcp2221_I2cReadRestart  
Description: Read I2C data from a slave starting with a Repeated START.  
Parameters:  
Inputs: (void*) handle - the handle for the device.  
(unsigned int) bytesToRead - the number of bytes to read from the slave. Valid range is between 1 and 65535.  
(unsigned char) slaveAddress - 7bit or 8bit I2C slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0 - 7 bit address will be used for the slave. If 0 - 8 bit is used.  
Outputs: (unsigned char*) i2cRxData - buffer that will contain the data bytes read from the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: 1. The speed must be set via the "Mcp2221_SetSpeed" function before using this method. If the speed has not been set an error will be returned. 2. The SMBus Process Call command can be formed using Mcp2221_I2cWriteNoStop followed by Mcp2221_I2cReadRestart.  

8. Mcp2221_I2cWriteRestart  
Description: Write I2C data to a slave without sending the STOP bit.  
Parameters:  
Inputs: (void*) handle - the handle for the device.  
(unsigned int) bytesToWrite - the number of bytes to write to the slave. Valid range is between 0 and 65535.  
(unsigned char) slaveAddress - 7bit or 8bit I2C slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char*) i2cTxData - buffer that will contain the data bytes to be sent to the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: The speed must be set via the "Mcp2221_SetSpeed" function before using this method. If the speed has not been set an error will be returned.  

9.  Mcp2221_SmbusSendByte  
Description: SMBus Send byte. Sends one data byte.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag.For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0 Packet Error Checking (PEC) will be used. A PEC byte containing the CRC8 value for the sent message is appended after the data byte.  
(unsigned char) data - The data byte.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  

10.  Mcp2221_SmbusReceiveByte  
Description: SMBus Receive Byte. Read one data byte back.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used.  
Outputs:
(unsigned char*) readByte - The data byte received from the slave  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used.Otherwise, the speed will not be reconfigured.  

11.  Mcp2221_SmbusReadByte  
Description: SMBus Read Byte. First Write the command byte to the slave, then read one data byte back.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used.  
(unsigned char) command - The command code byte.  
Outputs:
(unsigned char*) readByte - The data byte received from the slave  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used.Otherwise, the speed will not be reconfigured.
SMBus Read Byte. First Write the command byte to the slave, then read one data byte back.  

12.  Mcp2221_SmbusWriteWord 
Description: SMBus write word. The first byte of a Write Byte operation is the command code, followed by the data_byte_low then data_byte_high.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used. A PEC byte containing the CRC8 value for the sent message is appended after the data byte.  
(unsigned char) command - The command code byte.  
(unsigned char*) data - Array containing the low and high data bytes to be sent to the slave.  
data[0] will be considered the data_byte_low  
data[1] will be considered the data_byte_high    
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured. 
SMBus write word. The first byte of a Write Byte operation is the command code, followed by the data_byte_low then data_byte_high.  

13.  Mcp2221_SmbusReadWord
Description: SMBus Read Word. First Write the command byte to the slave, then read one data byte back.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag.For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0 Packet Error Checking (PEC) will be used.  
(unsigned char) command - The command code byte.  
Outputs:
(unsigned char*) readData - Buffer that will store the read data word.  
readData[0] - data_byte_low  
readData[1] - data_byte_high    
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  
SMBus Read Word. First Write the command byte to the slave, then read one data byte back.  

14.  Mcp2221_SmbusBlockWrite  
Description: SMBus Block Write. The first byte of a Block Write operation is the command code, followed by the number of data bytes, then data bytes.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used. A PEC byte containing the CRC8 value for the sent message is appended after the data byte.  
(unsigned char) command - The command code byte.  
(unsigned char) byteCount - the number of data bytes that will be sent to the slave. Valid range is between 0 and 255 bytes, conforming to the smbus v3 specification.  
(unsigned char*) data - Array containing the data bytes to be sent to the slave.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  

15.  Mcp2221_SmbusBlockRead  
Description: SMBus Block Read.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 1 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used. The CRC8 values is computed for the SMBus packet compared with the PEC byte sent by the slave. If the two values differ the function returns an error code.  
(unsigned char) command - The command code byte.  
(unsigned char) byteCount - (block size) the number of data bytes that the slave will send to the master.   Valid range is between 1 and 255 bytes. If there is a mismatch between this value and the byteCount the slave reports that it will send, an error will be returned.    
Outputs:
(unsigned char*) readData - Array containing the data bytes read from the slave. If PEC is used, the last data byte will be the PEC byte received from the slave so the array should have a length of n+1, where n is the block size.  
Returns: (int) - 0 for success; error code otherwise.  
NOTE: If the "Mcp2221_SetSpeed" function has not been called for the provided handle, the default speed of 100kbps will be configured and used. Otherwise, the speed will not be reconfigured.  

16.  Mcp2221_SmbusBlockWriteBlockReadProcessCall  
Description: SMBus Block Write Block Read Process Call.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(unsigned char) slaveAddress - 7bit or 8bit SMBus slave address, depending on the value of the "use7bitAddress" flag. For 8 bit addresses, the R/W LSB of the address is set to 0 inside the function.  
(unsigned char) use7bitAddress - if >0, 7 bit address will be used for the slave. If 0, 8 bit is used.  
(unsigned char) usePec - if >0, Packet Error Checking (PEC) will be used. The CRC8 values is computed for the SMBus packet and compared with the PEC byte sent by the slave. If the two values differ the function returns an error code.  
(unsigned char) command - The command code byte.  
(unsigned char) writeByteCount - the number of data bytes that will be sent to the slave. The total data payload must not exceed 255 bytes (writeByteCount + readByteCound <= 255) and writeByteCount > 0  
(unsigned char*) writeData - array containing the data bytes to be sent to the slave.  
(unsigned char) readByteCount - the number of data bytes that the slave will send to the master. If there is a mismatch between this value and the readByteCount the slave reports that it will send, an error will be returned. The total data payload must not exceed 255 bytes (writeByteCount + readByteCound <= 255) and readByteCount > 0  
Outputs:
(unsigned char*) readData - Array containing the data bytes read from the slave. If PEC is used, the last data byte will be the PEC byte received from the slave so the array should have a length of n+1, where n is the readByteCount size.  
Returns: (int) - 0 for success; error code otherwise.  

#### USB settings adn Device Information
1. Mcp2221_GetManufacturerDescriptor  
Description: Read USB Manufacturer Descriptor string from device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
Outputs:
(wchar_t*) manufacturerString - will contain the value of the USB Manufacturer Descriptor String.  
Note: the output string can contain up to 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

2. Mcp2221_SetManufacturerDescriptor 
Description: Write USB Manufacturer Descriptor string to the device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(wchar_t*) manufacturerString - will contain the value of the USB Manufacturer Descriptor String.  
Note: the input string can contain a maximum of 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

3. Mcp2221_GetProductDescriptor  
Description: Read USB Product Descriptor string from device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
Outputs:
(wchar_t*) productString - will contain the value of the USB Product Descriptor String. Note: the output string can contain up to 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

4. Mcp2221_SetProductDescriptor  
Description: Write USB Product Descriptor string to the device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(wchar_t*) productString - will contain the value of the USB Product Descriptor String.  
Note: the input string can contain a maximum of 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

5. Mcp2221_GetSerialNumberDescriptor  
Description: Read USB Serial Number Descriptor string from device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
Outputs:
(wchar_t*) serialNumber - will contain the value of the USB Serial Number Descriptor String.  
Note: the output string can contain up to 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

6. Mcp2221_SetSerialNumberDescriptor  
Description: Write USB Serial Number Descriptor string to the device.  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
(wchar_t*) serialNumber - will contain the value of the USB Serial Number Descriptor String.  
Note: the input string can contain a maximum of 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

7. Mcp2221_GetFactorySerialNumber  
Description: Read the factory serial number of the device  
Parameters:  
Inputs:
(void*) handle - The handle for the device.  
Outputs:
(wchar_t*) serialNumber - will contain the value of the factory serial number of the device  
Note: the output string can contain a maximum of 30 characters  
Returns: (int) - 0 for success; error code otherwise.  

8. Mcp2221_GetVidPid  
Description: Gets the VID and PID for the selected device.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned int*) vid - The vendor id of the MCP2221 device  
(unsigned int*) pid - The product id of the MCP2221 device    
Returns: 0 if successful; error code otherwise  

9.  Mcp2221_SetVidPid  
Description: Sets the VID and PID for the selected device.  
Parameters:  
Inputs: (void*) handle - the handle for the device  
(unsigned int) vid - The vendor id to be set  
(unsigned int) pid - The product id to be set  
Returns: 0 if successful; error code otherwise  
NOTE: the new VID/PID values will take effect after a device reset.  

10.  Mcp2221_GetUsbPowerAttributes  
Description: Gets the USB power attribute values.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) powerAttributes - the power attributes value from the USB descriptor.
Bit meanings, based on the USB 2.0 spec:  
bit 7 - Reserved (Set to 1) (equivalent to Bus Powered)  
bit 6 - Self Powered  
bit 5 - Remote Wakeup  
bits 4..0 Reserved (reset to 0)  
(unsigned int*) currentReq - the requested current value (mA); This value is expressed in multiples of 2mA.  
Returns: 0 if successful; error code otherwise  

11.  Mcp2221_SetUsbPowerAttributes  
Description: Sets the USB power attribute values.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) powerAttributes - the power attributes value from the USB descriptor.  
Bit meanings, based on the USB 2.0 spec:  
bit 7 - Reserved (Set to 1) (equivalent to Bus Powered)  
bit 6 - Self Powered  
bit 5 - Remote Wakeup  
bits 4..0 Reserved (reset to 0)  
The following constants can be OR'd to set this value: MCP2221_USB_SELF, MCP2221_USB_REMOTE, MCP2221_USB_BUS
(unsigned int) currentReq - the requested current value (mA); This value is expressed in multiples of 2mA. Valid range is between 0 and 500mA. If an odd value is used, it will be rounded down to the closest even value (ex currentReq = 201mA will result in a 200mA current request).  
Returns: 0 if successful; error code otherwise  
NOTE: For the PowerAttributes parameter, bits 7 and 0-4 are automatically set to the correct reserved" value.  

12.  Mcp2221_GetSerialNumberEnumerationEnable  
Description: Gets the status of the Serial number enumeration bit.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) snEnumEnabled - determines if the serial number descriptor will be used during the USB enumeration of the CDC interface. If 1 - the serial number descriptor is used; if 0 - no serial number descriptor will be present during enumeration.  
Returns: 0 if successful; error code otherwise  

13.  Mcp2221_SetSerialNumberEnumerationEnable  
Description: Sets the status of the Serial number enumeration bit.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) snEnumEnabled - determines if the serial number descriptor will be used during the USB enumeration of the CDC interface. If 1 - the serial number descriptor is used; if 0 - no serial number descriptor will be present during enumeration.  
Returns: 0 if successful; error code otherwise  

14.  Mcp2221_GetHwFwRevisions  
Description: Reads the hardware and firmware revision values from the device.  
Parameters:  
Inputs:
(void*) handle - the handle for the device.  
Outputs:
(wchar_t*) hardwareRevision - will contain the hardware revision string.  
(wchar_t*) firmwareRevision - will contain the firmware revision string.  
Returns: 0 if successful; error code otherwise  
NOTE: the output strings must have a minimum length of 2.
Reads the hardware and firmware revision values from the device.  

#### Pin Functions
1. Mcp2221_GetInitialPinValues  
Description: Gets the initial values for the special function pins: LEDUARTRX, LEDUARTTX, LEDI2C, SSPND and USBCFG  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) ledUrxInitVal - this value represents the logic level signaled when no Uart Rx activity takes place (inactive level)  
(unsigned char*) ledUtxInitVal - this value represents the logic level signaled when no Uart Tx activity takes place (inactive level)  
(unsigned char*) ledI2cInitVal - this value represents the logic level signaled when no I2C traffic occurs (inactive level)  
(unsigned char*) sspndInitVal - this value represents the logic level signaled when the device is not in suspend mode (inactive level)  
(unsigned char*) usbCfgInitVal - this value represents the logic level signaled when the device is not usb configured (inactive level)Returns: 0 if successful; error code otherwise  
Returns: 0 if successful; error code otherwise  

2. Mcp2221_SetInitialPinValues  
Description: Sets the initial values for the special function pins: LEDUARTRX, LEDUARTTX, LEDI2C, SSPND and USBCFG. The settings are saved to flash and take effect after a device reset.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) ledUrxInitVal - this value represents the logic level signaled when no Uart Rx activity takes place (inactive level)  
(unsigned char) ledUtxInitVal - this value represents the logic level signaled when no Uart Tx activity takes place (inactive level)  
(unsigned char) ledI2cInitVal - this value represents the logic level signaled when no I2C traffic occurs (inactive level)  
(unsigned char) sspndInitVal - this value represents the logic level signaled when the device is not in suspend mode (inactive level)  
(unsigned char) usbCfgInitVal - this value represents the logic level signaled when the device is not usb configured (inactive level)  
Returns: 0 if successful; error code otherwise  
NOTE: Accepted values for the logic levels are 0(low) and 1(high), 0xff (leave unchanged)  

3. Mcp2221_GetInterruptEdgeSetting  
Description: Gets the interrupt pin trigger configuration.  
Parameters:  
Inputs:
(void*) handle - the handle for the device
(unsigned char) whichToGet - 0 to read Flash settings, >0 to read SRAM (runtime) settings  
Outputs:
(unsigned char*) interruptPinMode - value representing which edge will trigger the interrupt  
0 - none  
1 - positive edge  
2 - negative edge  
3 – both    
Returns: 0 if successful; error code otherwise  

4. Mcp2221_SetInterruptEdgeSetting  
Description: Sets the interrupt pin trigger configuration.  
Parameters:  
Inputs:
(void*) handle - the handle for the device
(unsigned char) whichToSet - 0 to write Flash settings, >0 to write SRAM (runtime) settings  
(unsigned char) interruptPinMode - value representing which edge will trigger the interrupt  
0 - none  
1 - positive edge  
2 - negative edge  
3 – both  
Returns: 0 if successful; error code otherwise  

5. Mcp2221_ClearInterruptPinFlag  
Description: Clears the interrupt pin flag of a device.  
Parameters:  
Inputs:
(void*) handle - the handle for the device for which the flag will be cleared.  
Returns: 0 if successful; error code otherwise  

6. Mcp2221_GetClockSettings  
Description: Gets the duty cycle and clock divider values for the clock out pin (if configured for this operation).  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToGet - 0 to read Flash settings, >0 to read SRAM (runtime) settings  
Outputs:
(unsigned char*) dutyCycle - value of the duty cycle of the waveform on the clock pin  
0 - 0 %  
1 - 25 %  
2 - 50 %  
3 - 75 %  
(unsigned char*) clockDivider - value of the clock divider. The value provided is a power of 2. The 48Mhz internal clock is divided by 2^value to obtain the output waveform frequency. The correspondence between the divider values and output frequencies are as follows:  
1 - 24 MHz  
2 - 12 MHz  
3 - 6 MHz  
4 - 3 MHz  
5 - 1.5 MHz  
6 - 750 kHz  
7 - 375 kHz  
Returns: 0 if successful; error code otherwise)  

7. Mcp2221_SetClockSettings  
Description: Sets the duty cycle and clock divider values for the clock out pin (if configured for this operation).  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToSet - 0 to write Flash settings, >0 to write SRAM (runtime) settings  
(unsigned char) dutyCycle - value of the duty cycle of the waveform on the clock pin  
0 - 0 %  
1 - 25 %  
2 - 50 %  
3 - 75 %  
(unsigned char) clockDivider - value of the clock divider. The value provided is a power of 2. The 48Mhz internal clock is divided by 2^value to obtain the output waveform frequency. The correspondence between the divider values and output frequencies are as follows:  
1 - 24 MHz  
2 - 12 MHz  
3 - 6 MHz  
4 - 3 MHz  
5 - 1.5 MHz  
6 - 750 kHz  
7 - 375 kHz  
Returns: 0 if successful; error code otherwise  

8. Mcp2221_GetDacVref  
Description: Gets the DAC voltage reference.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToGet - 0 to read Flash settings, >0 to read SRAM (runtime) settings  
Outputs:
(unsigned char*) dacVref - The voltage reference for the DAC:  
0 - Vdd  
1 - 1.024 V  
2 - 2.048 V  
3 - 4.096 V  
Returns: 0 if successful; error code otherwise  

9.  Mcp2221_SetDacVref  
Description: Sets the DAC voltage reference.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToSet - 0 to write Flash settings, >0 to write SRAM (runtime) settings  
(unsigned char) dacVref - The voltage reference for the DAC:  
0 - Vdd  
1 - 1.024 V  
2 - 2.048 V  
3 - 4.096 V  
Returns: 0 if successful; error code otherwise  

10.  Mcp2221_GetAdcData  
Description: Reads the ADC data for all 3 analog pins.  
Parameters:  
Inputs:
(void*) handle - the handle for the device.  
(unsigned int*) adcDataArray - Array containing the ADC values. Entry 0 will contain the value for ADC1, entry 1 - ADC2, entry 2 - ADC3  
Returns: 0 if successful; error code otherwise  
NOTE: the array must have a minimum length of 3.  

11.  Mcp2221_SetAdcVref  
Description: Sets the ADC voltage reference.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToSet - 0 to write Flash settings, >0 to write SRAM (runtime) settings  
(unsigned char) dacVref - The voltage reference for the ADC:  
0 - Vdd  
1 - 1.024 V  
2 - 2.048 V  
3 - 4.096 V  
Returns: 0 if successful; error code otherwise  

12.  Mcp2221_GetDacValue  
Description: Gets the DAC value.  
Parameters:  
Inputs:
(void*) handle - the handle for the device
(unsigned char) whichToGet - 0 to read Flash settings, >0 to read SRAM (runtime) settings  
Outputs:
(unsigned char*) dacValue - The DAC output value. Valid range is between 0 and 31.  
Returns: 0 if successful; error code otherwise  

13.  Mcp2221_SetDacValue  
Description: Sets the DAC value.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) whichToSet - 0 to write Flash settings, >0 to write SRAM (runtime) settings  
(unsigned char) dacValue - The DAC output value. Valid range is between 0 and 31.  
Returns: 0 if successful; error code otherwise  

14.  Mcp2221_GetGpioSettings  
Description: Gets the GPIO settings.  
Parameters:  
Inputs:
(void*) handle - the handle for the device
(unsigned char) whichToGet - 0 to read Flash settings, >0 to read SRAM (runtime) settings  
Outputs:
(unsigned char*) pinFunctions - Array containing the values for the pin functions. pinFunction[i] will contain the value for pin GP"i. Possible values: 0 to 3. 0 - GPIO, 1 - Dedicated function, 2 - alternate function 0, 3 - alternate function 1, 4 - alternate function 2.
GP0: 0 – GPIO GP1: 0 – GPIO GP2: 0 – GPIO GP3: 0 - GPIO  
1 – SSPND 1 - Clock Out 1 - USBCFG 1 - LED I2C  
2 - LED UART RX 2 - ADC1 2 - ADC2 2 - ADC3  
3 - LED UART TX 3 - DAC1 3 - DAC2  
4 - Interrupt detection  
(unsigned char*) pinDirections - Array containing the pin direction of the IO pins.  
0 - output  
1 - input  
(unsigned char*) outputValues - Array containing the value present on the output pins.  
0 - logic low  
1 - logic high    
Returns: 0 if successful; error code otherwise  
NOTE: all output arrays must have a minimum length of 4.  

15.  Mcp2221_SetGpioSettings  
Description: Sets the GPIO settings.  
Parameters:  
Inputs:
(void*) handle - the handle for the device
(unsigned char) whichToSet - 0 to write Flash settings, >0 to read SRAM (runtime) settings  
(unsigned char*) pinFunctions - Array containing the values for the pin functions. pinFunction[i] will contain the value for pin GP"i". Possible values: 0 to 3. 0 - GPIO, 1 - Dedicated function, 2 - alternate function 0, 3 - alternate function 1, 4 - alternate function 2, 0xFF - leave the pin unchanged.
GP0: 0 – GPIO GP1: 0 – GPIO GP2: 0 - GPIO GP3: 0 - GPIO  
1 - SSPND 1 - Clock Out 1 - USBCFG 1 - LED I2C  
2 - LED UART RX 2 - ADC1 2 - ADC2 2 - ADC3  
3 - LED UART TX 3 - DAC1 3 - DAC2  
4 - Interrupt detection  
(unsigned char*) pinDirections - Array containing the pin direction of the IO pins.  
0 - output  
1 - input  
0xff - leave unchanged  
(unsigned char*) outputValues - Array containing the value present on the output pins.  
0 - logic low  
1 - logic high  
0xff - leave unchanged    
Returns: 0 if successful; error code otherwise  
NOTE: all arrays must have a minimum length of 4.  

16.  Mcp2221_GetGpioValues  
Description: Gets the GPIO pin values.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) gpioValues - Array containing the value present on the IO pins.  
0 - logic low  
1 - logic high  
0xEE - GPx not set for GPIO operation  
Returns: 0 if successful; error code otherwise  
NOTE: the output array must have a minimum length of 4.  

17.  Mcp2221_SetGpioValues  
Description: Sets the runtime GPIO pin values. Sets the runtime GPIO pin directions; flash values are not changed.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char*) gpioValues - Array containing the value of the output IO pins.  
0 - logic low  
1 - logic high  
0xFF - no change  
Returns: 0 if successful; error code otherwise  
NOTE: the output array must have a minimum length of 4.  

18.  Mcp2221_GetGpioDirection  
Description: Gets the GPIO pin directions.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) gpioDir - Array containing the direction of an IO pin.  
0 - output  
1 - input  
0xEF - GPx not set for GPIO operation  
Returns: 0 if successful; error code otherwise  
NOTE: the output array must have a minimum length of 4.  

19.  Mcp2221_SetGpioDirection  
Description: Sets the runtime GPIO pin directions; flash values are not changed.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char*) gpioDir - Array containing the direction of an IO pin. gpioDir[i] will set pin "i"  
0 - output  
1 - input  
0xff - no change  
Returns: 0 if successful; error code otherwise  
NOTE: the output array must have a minimum length of 4.  

#### Security
1. Mcp2221_GetSecuritySetting  
Description: Gets the state of flash protection for the device  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
Outputs:
(unsigned char*) securitySetting - the value of the chip security option  
0 - unsecured  
1 - password protected  
2 - permanently locked  
Returns: 0 if successful; error code otherwise    
Gets the state of flash protection for the device  

2. Mcp2221_SetSecuritySettings  
Description: Sets the state of flash protection for the device  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(unsigned char) securitySetting - the value of the chip security option. If any other values are used, the E_ERR_INVALID_PARAMETER (-4) error is returned.  
0 - disable password protection  
1 - enable password protection  
0xff - change current password  
(char*) currentPassword - the value for the currently set password. This is used for when the password "disable" or "change" operations are taking place.  
(char*) newPassword - the value for the new password. Must be an 8 character string. This is only for the "enable" or "change" operations.  
Returns: 0 if successful; error code otherwise  

3. Mcp2221_SetPermanentLock  
Description: Permanently lock the device flash settings -- this action CAN'T be undone.  
Parameters:  
Inputs:
(void*) handle - the handle for the device to be locked  
Returns: 0 if successful; error code otherwise  
!!! WARNING !!! -- USE THIS FUNCTION WITH GREAT CAUTION. THE CHIP FLASH SETTINGS (boot-up defaults) CANNOT BE CONFIGURED AFTER THIS FUNCTION HAS BEEN INVOKED!!  

4. Mcp2221_SendPassword  
Description: Sends the access password to the device.  
Parameters:  
Inputs:
(void*) handle - the handle for the device  
(char*) password - the password that will be sent to the device to unlock writing to flash. Must be an 8 character string.  
Returns: 0 if successful; error code otherwise  
NOTE: If 3 flash writes are attempted with an incorrect password, the chip won't accept any more passwords. This function doesn't validate the password, it just sends it to the device. The password is checked only during a flash write.  

### Error Codes
| Value | Code | Description | Suggestion |  
|-------|------|-------------|------------|  
| 0 | E_NO_ERR | operation was successfull | |
| -1 | E_ERR_UNKOWN_ERROR | Unknown error. This can happen in the getconnecteddevices, openbyindex or openbytes if searching through the connected hid devices fails. | Try again |
| -2 | E_ERR_CMD_FAILED | The library indicates an unexpected device replay after being given a command: neither successful operation nor specific error code. | This is a command failure indication. Depending on the application strategy, the next step can be a device status check followed by command retry. |
| -3 | E_ERR_INVALID_HANDLE | Invalid device handle usage attempt. The device is already closed or there is an issue with the device handles management in the application | Re-open the device, or exit the application |
| -4 | E_ERR_INVALID_PARAMETER | At least one api parameter is not valid | Check the parameter validity and try again |
| -5 | E_ERR_INVALID_PASS | Invalid Password (length <8) | Check the password string and try again |
| -6 | E_ERR_PASSWORD_LIMIT_REACHE | An Incorrect password was sent 3 time | Reset the device, check password and try again | 
| -7 | E_ERR_FLASH_WRITE_PROTECTED | The command cannot be executed because the device is password protected or locked | Check the security settings (GetSecuritySetting) and if the device is not permanently locked, send the current password before retrying the operation | 
| -10 | E_ERR_NULL | Null pointer received | Validate the input parameters | 
| -11 | E_ERR_DESTINATION_TOO_SMALL | Destination string to small | | 
| -12 | E_ERR_INPUT_TOO_LARGE | The input string exceeds teh maximum allowed size | Check that the string length is within the range provided in teh function documentation | 
| -13 | E_ERR_FLASH_WRITE_FAILED | Flash write failed due to an unkown error | | 
| -14 | E_ERR_MALLOC | Memory allocation error | | 
| -101 | E_ERR_NO_SUCH_INDEX | An attempt was made to open a connection to an non existing index (usually >= the number of connect devices) | Check the number of connected devices (with getconnecteddevices); the index must be smaller | 
| -103 | E_ERR_DEVICE_NOT_FOUND | No device with the provided vid/pid or SN has been found. This error can also occur during the i2c/smbus operations if the device is disconnected from the usb before the operation is compelete. The OpenBySn method will also return tis code if a connectio to an matching device is already open. | | 
| -104 | E_ERR_INTERNAL_BUFFER_TOO_SMALL | One of the internal buffers of teh function was to small | | 
| -105 | E_ERR_OPEN_DEVICE_ERROR | An error occurred when trying to get the device handle | Retry operation | 
| -106 | E_ERR_CONNECTION_ALREADY_OPEN | Connection already open | Sharing mode is not allowed. Please read the paragraph "device parallel access /  multithreading | 
| -107 | E_ERR_CLOSE_FAILED | File close operation failed due to unkown reasons | Tray again or exit the applicatoin | 
| -301 | E_ERR_RAW_TX_TOO_LARGE | Low level communication error, shouldn't appear during nomral operation | Restart application | 
| -302 | E_ERR_RAW_TX_COPYFAILED | Low level communication error, shouldn't appear during normal operation | Restart application | 
| -303 | E_ERR_RAW_RX_COPYFAILED | Low level communication error, shouldn't appear during normal operation | Restart Application | 
| -401 | E_ERR_INVALID_SPEED | I2c/smbus speed is not within accepted range of 46875 - 500000 | |
| -402 | E_ERR_SPEED_NOT_SET | The speed may fail to be set if an i2c/smbus operation is already in progress or in a timeout situation. The "mcp2221_i2ccancelcurrenttransfer" function can be used to free the bus before retrying to set the speed. | | 
| -403 | E_ERR_INVALID_BYTE_NUMBER | The byte count is outside the accepted range for the attempted operation | Check the valid range for the desired operation and retry | 
| -405 | E_ERR_I2C_BUSY | The mcp2221 i2c/smbus engine is currently busy. | Retry operation or call cancelcurrenti2ctransfer before another retry. | 
| -406 | E_ERR_I2C_READ_ERROR | Mcp2221 signaled an error during the i2c read operation | Retry or reset device before retrying | 
| -407 | E_ERR_ADDRESS_NACK | Nack received for the slave address used | Check that the slave address is correct. | 
| -408 | E_ERR_TIMEOUT | Either the "timeout" or "retries" value has been exceeded and no reply was received from the slave. | I2c/smbus transfer is not working properly. Check the communication settings and try again. The retries and timeout values can also be updated in the SetAdvancedCommParams |
| -409 |  E_ERR_TOO_MANY_RX_BYTES | The number of received data bytes is greater than requested | | 
| -410 | E_ERR_COPY_RX_DATA_FAILED | Could not copy the data received from the slave into the provided buffer; | Check buffer size and retry operation | 
| -411 |  E_ERR_NO_EFFECT | The i2c engine (inside mcp2221) was already idle. The cancellation command had no effect. | | 
| -412 | M_E_ERR_COPY_TX_DATA_FAILED | Failed to copy the data into the hid buffer | Retry operation | 
| -413 | M_E_ERR_INVALID_PEC | The slave replied with a pec value different than the expected one. | Check that the smbus parameters used are supported by the slave. | 
| -414 | M_E_ERR_BLOCK_SIZE_MISMATCH | The slave sent a different value for the block size(byte count) than we expected | Check that the SMBus parameters used are supported by the slave. | 

### Constants

| Constant | Value | Description | 
| -------- | ----- | ----------- | 
| FLASH_SETTINGS | 0 |  read/write chip flash settings |
| RUNTIME_SETTINGS | 1 | read/write chip runtime settings | 
| NO_CHANGE | 0xff | Do not change the existing value. For example you can alter a pin's function and mark the rest as "no_change" to maintain their existing configuration. | 
| MCP2221_GPFUNC_IO | 0 | Pin configured as input/output | 
| MCP2221_GP_SSPND | 1 | Pin configured as SSPND | 
| MCP2221_GP_CLOCK_OUT | 1 | pin configured as ClockOut |  
| MCP2221_GP_USBCFG | 1 | pin configured for USBCFG | 
| MCP2221_GP_LED_I2C | 1 | pin configured for I2C LED | 
| MCP2221_GP_LED_UART_RX | 2 | pin configured for UART RX LED |
| MCP2221_GP_ADC | 2 | pin configured for ADC | 
| MCP2221_GP_LED_UART_TX | 3 | pin configured for UART TX LED |
| MCP2221_GP_DAC | 3 | Pin configured for DAC function |
| MCP2221_GP_IOC | 4 | Pin configured for Interrupt On Change |
| MCP2221_GPDIR_INPUT | 1 | GPIO pin configured as input | 
| MCP2221_GPDIR_OUTPUT | 0 | GPIO pin configured as output | 
| MCP2221_GPVAL_HIGH | 1 | Logic high value for I/O pins |
| MCP2221_GPVAL_LOW | 0| Logic low value for I/O pins |
| INTERRUPT_NONE | 0 | Interrupt on change trigger = none |
| INTERRUPT_POSITIVE_EDGE | 1 | interrupt on change trigger = positive edge |
| INTERRUPT_NEGATIVE_EDGE | 2 | interrupt on change trigger = negative edge |
| INTERRUPT_BOTH_EDGES | 3 | interrupt on change trigger = both edges |
| VREF_VDD | 0 | ADC/DAC voltage reference = Vdd | 
| VREF_1024V | 1 | ADC/DAC voltage reference = 1.024V |
| VREF_2048V | 2 | ADC/DAC voltage reference = 2.048V | 
| VREF_4096V | 3 | ADC/DAC voltage reference = 4.096V |
| MCP2221_USB_BUS | 0x80 | USB bus powered |
| MCP2221_USB_SELF | 0x40 | USB self powered |
| MCP2221_USB_REMOTE | 0x20 | USB remote wakeup enable | 
| MCP2221_PASS_ENABLE | 1 | Enable password protection |
| MCP2221_PASS_DISABLE | 0 | Disable password protection | 
| MCP2221_PASS_CHANGE | 0xff | Change current password | 