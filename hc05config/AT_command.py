import serial
from serial.tools.list_ports import comports
from time import sleep
import warning

from .enum_const import *
from .validation import *

def getSerialPorts():
	"""Get a list of available serial ports
	
	:return: a list of available serial ports
	:rtype: list[str]
	"""
	return list(map(lambda x: x.device, comports()))

class SerialATConfig(serial.Serial):

	def __init__(self, port_name, delay=0.01, baudrate=38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, *args, **kwargs):
		"""The class of a AT mode serial port, inherit from serial.Serial
		
		:param port_name: The name of the designated serial port for AT mode configuration
		:type port_name: str
		:param delay: The period (in second) to check if there is any response from the serial port, defaults to 0.01
		:type delay: float, optional
		:param baudrate: The baudrate to enter AT mode, defaults to 38400
		:type baudrate: int, optional
		:param timeout: Timeout to parity waiting for response, defaults to 0.5
		:type timeout: float, optional
		:param parity: Parity bit for the serial port, defaults to serial.PARITY_NONE
		:type parity: str, optional
		:param stopbits: Stop bit for the serial port, defaults to serial.STOPBITS_ONE
		:type stopbits: int or float, optional
		"""
		super(serial.Serial, self).__init__(port_name, *args, baudrate=baudrate, timeout=timeout, parity=parity, stopbits=stopbits, **kwargs)
		self.delay = delay
		self.max_delay_time = int(timeout / delay)

	def sendATCommand(self, cmd, raw=False):
		"""Send a AT command to the serial port
		Example: sendATCommand("AT+NAME?")

		If there is no response from the serial port, it will first check if the device still in AT mode.
		If yes, ATState.NOT_IN_AT_MODE is returned, otherwise ATState.FAIL is returned.
		If there is response from the serial port, it will first check if the response is an error message.
		If yes, ATState.ERROR is return, otherwise ATState.SUCCESS is returned.
		
		:param cmd: The AT comaand to be sent, "\r\n" is not required in the end of the command
		:type cmd: str
		:param raw: Choose to return raw string or not, defaults to False
		:type raw: bool, optional
		:return: Return ATState and the list of raw binary string if raw = True,
		or the list of decode string without "\r\n" at the end if raw = False.
		None is returned if no response .
		:rtype: enum 'ATState', list[str]
		"""
		# open the port and reset the input buffer to prevent left over response from previous command
		if not self.is_open:
			self.open()
		self.reset_input_buffer()

		cmd += "\r\n"
		self.write(cmd.encode())

		# wait for response
		time = 0
		while not self.in_waiting:
			time += 1
			sleep(self.delay)
			if time > self.max_delay_time:
				# if no response, check if it is in AT mode or not
				if self.isATMode():
					return ATState.FAIL, None
				else:
					return ATState.NOT_IN_AT_MODE, None

		raw_text = self.readlines()
		return ATState.ERROR if b"ERROR" in raw_text[0] else ATState.SUCCESS, raw_text if raw else list(map(lambda line: line.decode("UTF-8")[:-2], raw_text))

	def sendSettingATCommand(self, cmd):
		"""Send a AT setting command to the serial port
		
		:param cmd: The AT comaand to be sent, "\r\n" is not required in the end of the command
		:type cmd: str
		:return: Return the state of response
		:rtype: enum 'ATState'
		"""
		state, _ = self.sendATCommand(cmd)
		return state

	def isATMode(self):
		"""Check if the HC-05 module is in AT mode or not
		
		:return: Return True if the module is in AT mode, otherwise False
		:rtype: bool
		"""
		# open the port and reset the input buffer to prevent left over response from previous command
		if not self.is_open:
			self.open()
		self.reset_input_buffer()

		cmd = "AT\r\n"
		self.write(cmd.encode())

		# wait for response
		time = 0
		while not self.in_waiting:
			time += 1
			sleep(self.delay)
			if time > self.max_delay_time:
				return False

		raw_text = self.readlines()
		return b"OK" in raw_text[0]

	def reset(self):
		"""Exit the AT mode of the HC-05 module
		
		:return: Return True if the response is "OK", False otherwise
		:rtype: bool
		"""
		return self.sendSettingATCommand("AT+RESET")

	def restoreDefault(self):
		"""Restore the HC-05 module to default status
		
		:return: Return True if the response is "OK", False otherwise
		:rtype: bool
		"""
		return self.sendSettingATCommand("AT+ORGL")

	def getName(self):
		"""Get the name of the HC-05 module
		
		:return: Return the name of the module if respond successfully, the error string received if response has error, None otherwise
		:rtype: enum 'ATState', str
		"""
		state, name = self.sendATCommand("AT+NAME?")

		if state == ATState.SUCCESS:
			name = name[0]
			return state, name[name.find(":") + 1:]
		elif state == ATState.ERROR:
			return state, name[0]
		else:
			return state, None

	def getUartInfo(self):
		"""Get all the uart info of the HC-05 module
		The dictionary format:
		{
			"Baud Rate": int,
			"Stop Bit": enum 'StopBit',
			"Parity Bit": enum 'ParityBit'
		}
		
		:return: Return a dictionary of info if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', dict/str
		"""
		state, uartInfo = self.sendATCommand("AT+UART?")
		if state == ATState.SUCCESS:
			uartInfo = uartInfo[0]
			parse_uartInfo = list(map(lambda x: int(x), uartInfo[uartInfo.find(":") + 1:].split(",")))
			return state, {BAUDRATE: parse_uartInfo[0], STOP_BIT: StopBit(parse_uartInfo[1]), PARITY_BIT: ParityBit(parse_uartInfo[2])}
		elif state == ATState.ERROR:
			return state, uartInfo[0]
		else:
			return state, None

	def getBaudrate(self):
		"""Get the baudrate of the HC-05 module
		
		:return: Return the baudrate if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', int/str
		"""
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return state, uartInfo[BAUDRATE]
		elif state == ATState.ERROR:
			return state, uartInfo
		else:
			return state, None

	def getStopBit(self):
		"""Get the stop bit of the HC-05 module
		
		:return: Return the stop bit if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', enum 'StopBit'/str
		"""
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return state, uartInfo[STOP_BIT]
		elif state == ATState.ERROR:
			return state, uartInfo
		else:
			return state, None

	def getParityBit(self):
		"""Get the parity bit of the HC-05 module
		
		:return: Return the parity bit if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', enum 'ParityBit'/str
		"""
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return state, uartInfo[PARITY_BIT]
		elif state == ATState.ERROR:
			return state, uartInfo
		else:
			return state, None

	def getPassword(self):
		"""Get the password of the HC-05 module
		
		:return: Return the password if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', str
		"""
		state, password = self.sendATCommand("AT+PSWD?")
		if state == ATState.SUCCESS:
			password = password[0]
			return state, password[password.find(":") + 1:].replace("\"", "")
		elif state == ATState.ERROR:
			return state, password[0]
		else:
			return state, None

	def getRole(self):
		"""Get the role of the HC-05 module
		
		:return: Return the role if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', enum 'Role'/str
		"""
		state, role = self.sendATCommand("AT+ROLE?")
		if state == ATState.SUCCESS:
			role = role[0]
			return state, Role(int(role[role.find(":") + 1:]))
		elif state == ATState.ERROR:
			return state, role[0]
		else:
			return state, None

	def getConnectionMode(self):
		"""Get the connection mode of the HC-05 module
		
		:return: Return the connection mode if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', enum 'ConnectionMode'/str
		"""
		state, cmode = self.sendATCommand("AT+CMODE?")
		if state == ATState.SUCCESS:
			cmode = cmode[0]
			return state, ConnectionMode(int(cmode[cmode.find(":") + 1:]))
		elif state == ATState.ERROR:
			return state, cmode[0]
		else:
			return state, None

	def getAddress(self):
		"""Get the standard bluetooth MAC address of the HC-05 module
		
		:return: Return the standard bluetooth MAC address if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', str
		"""
		state, addr = self.sendATCommand("AT+ADDR?")
		if state == ATState.SUCCESS:
			addr = addr[0]
			return state, formatBluetoothAddress(addr[addr.find(":") + 1:])
		elif state == ATState.ERROR:
			return state, addr[0]
		else:
			return state, None

	def getBindAddress(self):
		"""Get the standard bind address of the HC-05 module
		
		:return: Return the standard bind address if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', str
		"""
		state, addr = self.sendATCommand("AT+BIND?")
		if state == ATState.SUCCESS:
			addr = addr[0]
			return state, formatBluetoothAddress(addr[addr.find(":") + 1:])
		elif state == ATState.ERROR:
			return state, addr[0]
		else:
			return state, None

	def getVersion(self):
		"""Get the firmware version of the HC-05 module
		
		:return: Return the firmware version if response successfully, the error string receive if response has error, None otherwise
		:rtype: enum 'ATState', str
		"""
		state, version = self.sendATCommand("AT+VERSION?")
		if state == ATState.SUCCESS:
			version = version[0]
			return state, version[version.find(":") + 1:]
		elif state == ATState.ERROR:
			return state, version[0]
		else:
			return state, None

	def get(self, info_title):
		"""Get multiple info at a time
		
		:param info_title: A list of info's title
		:type info_title: list[str]
		:return: A dictionary with the state of getting info and a dictionary of actual returned info
		:rtype: dict, dict
		"""
		uartInfo_state = None
		uartInfo = None
		state = {}
		info = {}

		for i in info_title:
			print(i)
			if i not in AVAILABLE_GET_INFO:
				warnings.warn(f"Unknown Info Title, skip \"{i}\"")
				continue

			if i == NAME:
				state[i], info[i] = self.getName()
			elif i == BAUDRATE or i == STOP_BIT or i == PARITY_BIT:
				if uartInfo_state == None:
					uartInfo_state, uartInfo = self.getUartInfo()
				state[i], info[i] = uartInfo_state, uartInfo[i] if uartInfo else None
			elif i == PASSWORD:
				state[i], info[i] = self.getPassword()
			elif i == ADDRESS:
				state[i], info[i] = self.getAddress()
			elif i == VERSION:
				state[i], info[i] = self.getVersion()
			elif i == ROLE:
				state[i], info[i] = self.getRole()
			elif i == CONNECTION_MODE:
				state[i], info[i] = self.getConnectionMode()
			elif i == BIND_ADDRESS:
				state[i], info[i] = self.getBindAddress()

		return state, info

	def setName(self, name):
		"""Set the name of the HC-05 module
		
		:param name: The name that is going to be set
		:type name: str
		:raises ValueError: If the name is invalid, i.e. the length of name exceeds the limit of 32 characters, a ValueError will be raised
		:return: The state of response
		:rtype: enum 'ATState'
		"""
		if not isNameValid(name):
			raise ValueError("The name is invalid, the length of name exceeds the limit of 32 characters")
		return self.sendSettingATCommand(f"AT+NAME={name}")

	def setUart(self, baudrate, stopBit, parityBit):
		"""Set the UART configuration (Baudrate, Stop Bit and Parity Bit) of the HC-05 module
		
		:param baudrate: The baudrate to be set
		:type baudrate: int
		:param stopBit: The stop bit to be set
		:type stopBit: enum 'StopBit'
		:param parityBit: The parity bit to be set
		:type parityBit: enum 'ParityBit'
		:raises ValueError: If the baudrate is invalid, a ValueError will be raised
		:raises ValueError: If the stop bit is invalid, a ValueError will be raised
		:raises ValueError: If the parity bit is invalid, a ValueError will be raised
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		if not isBaudrateValid(baudrate):
			raise ValueError("Invalid baudrate. The valid baudrate are as follow: 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1382400")
		if not isStopBitValid(stopBit):
			raise ValueError("Invalid stop bit. The valid stop bit are as follow: 0, 1")
		if not isParityBitValid(parityBit):
			raise ValueError("Invalid parity bit. The valid parity are as follow: 0, 1, 2")
		return self.sendSettingATCommand(f"AT+UART={baudrate},{int(stopBit)},{int(parityBit)}")

	def setBaudrate(self, baudrate):
		"""Set the baudrate of the HC-05 module
		
		:param baudrate: The baudrate to be set
		:type baudrate: int
		:raises ValueError: If the baudrate is invalid, a ValueError will be raised
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		if not isBaudrateValid(baudrate):
			raise ValueError("Invalid baudrate. The valid baudrate are as follow: 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1382400")
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return self.sendSettingATCommand(f"AT+UART={baudrate},{int(uartInfo[STOP_BIT])},{int(uartInfo[PARITY_BIT])}")
		else:
			return False

	def setStopBit(self, stopBit):
		"""Set the stop bit of the HC-05 module
		
		:param stopBit: The stop bit to be set
		:type stopBit: int
		:raises ValueError: If the stop bit is invalid, a ValueError will be raised
		:return: The state of response 
		:rtype: enum 'ATState'
		"""

		if not isStopBitValid(stopBit):
			raise ValueError("Invalid stop bit. The valid stop bit are as follow: 0, 1")
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return self.sendSettingATCommand(f"AT+UART={uartInfo[BAUDRATE]},{int(stopBit)},{int(uartInfo[PARITY_BIT])}")
		else:
			return False

	def setParityBit(self, parityBit):
		"""Set the parity bit of the HC-05 module
		
		:param parityBit: The parity bit to be set
		:type parityBit: int
		:raises ValueError: If the parity bit is invalid, a ValueError will be raised
		:return: The state of response 
		:rtype: enum 'ATState'
		"""

		if not isParityBitValid(parityBit):
			raise ValueError("Invalid parity bit. The valid parity are as follow: 0, 1, 2")
		state, uartInfo = self.getUartInfo()
		if state == ATState.SUCCESS:
			return self.sendSettingATCommand(f"AT+UART={uartInfo[BAUDRATE]},{int(uartInfo[STOP_BIT])},{int(parityBit)}")
		else:
			return False

	def setPassword(self, password):
		"""Set the password of the HC-05 module
		
		:param password: The password to be set
		:type password: str
		:raises ValueError: If the password is invalid, i.e. the length of password exceeds the limit of 16 characters, a ValueError will be raised
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		if not isPasswordValid(password):
			raise ValueError("Invalid password. the length of password exceeds the limit of 16 characters")
		return self.sendSettingATCommand(f"AT+PSWD=\"{password}\"")

	def setRole(self, role):
		"""Set the role of the HC-05 module
		
		:param role: The role to be set
		:type role: enum 'Role'
		:raises ValueError: If the role is invalid, a ValueError will be raised 
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		if not isRoleValid(role):
			raise ValueError("Invalid role. The valid role are as follow: 0, 1, 2")
		return self.sendSettingATCommand(f"AT+ROLE={int(role)}")

	def setConnectionMode(self, cmode):
		"""Set the conncetion mode of the HC-05 module
		
		:param cmode: The conncetion mode to be set
		:type cmode: enum 'ConnectionMode'
		:raises ValueError: If the conncetion mode is invalid, a ValueError will be raised 
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		if not isConnectionModeValid(cmode):
			raise ValueError("Invalid connection mode. The valid connection mode are as follow: 0, 1, 2")
		return self.sendSettingATCommand(f"AT+CMODE={int(cmode)}")

	def setBindAddress(self, addr):
		"""Set the bind address of the HC-05 module
		
		:param addr: The bind address of the HC-05 module
		:type addr: str
		:return: The state of response 
		:rtype: enum 'ATState'
		"""
		addr = formatBluetoothAddress(addr)
		return self.sendSettingATCommand("AT+BIND=" + addr.replace(":", ","))

	def set(self, settings):
		"""Set a list of settings
		
		:param settings: A dictionary will all the settings to be set, e.g. {NAME: "HC-05", PASSWORD: "1234"}
		:type settings: dict
		"""
		baudrate = None
		stopBit = None
		parityBit = None
		success = {}

		for setting, value in settings.items():
			if i not in AVAILABLE_SET_INFO:
				warnings.warn(f"Unknown setting, skip \"{i}\"")
				continue

			if setting == NAME:
				success[setting] = self.setName(value)
			elif setting == BAUDRATE:
				baudrate = value
			elif setting == STOP_BIT:
				stopBit = value
			elif setting == PARITY_BIT:
				parityBit = value
			elif setting == PASSWORD:
				success[setting] = self.setPassword(value)
			elif setting == ROLE:
				success[setting] = self.setRole(value)
			elif setting == CONNECTION_MODE:
				success[setting] = self.setConnectionMode(value)
			elif setting == BIND_ADDRESS:
				success[setting] = self.setBindAddress(value)
			
			if baudrate or stopBit or parityBit:
				if not(baudrate and stopBit and parityBit):
					state, moduleUart = self.getUartInfo()
					if state == ATState.SUCCESS:
						if not baudrate: baudrate = moduleUart[BAUDRATE]
						if not stopBit: stopBit = moduleUart[STOP_BIT]
						if not parityBit: parityBit = moduleUart[PARITY_BIT]

						successUart = self.setUart(baudrate, stopBit, parityBit)
						success[BAUDRATE] = success[STOP_BIT] = success[PARITY_BIT] = successUart
					else:
						success[BAUDRATE] = success[STOP_BIT] = success[PARITY_BIT] = False
