import serial
from time import sleep

DELAY = 0.01
MAX_DELAY_TIME = 50

class SerialATMode(serial.Serial):
	def sendATCommand(self, cmd, raw=False):
		if not self.is_open:
			self.open()
		self.reset_input_buffer()

		cmd += "\r\n"
		self.write(cmd.encode())

		time = 0
		while not self.in_waiting:
			time += 1
			sleep(DELAY)
			if time > MAX_DELAY_TIME:
				return None

		text = self.readlines()
		return text if raw else text[0].decode("UTF-8")[:-2]

	def sendATCommandWithChecking(self, cmd, raw=False):
		while True:
			respond = self.sendATCommand(cmd, raw)
			if not respond:
				self.checkATMode()
			else:
				return respond

	def sendSettingATCommand(self, cmd):
		if self.sendATCommandWithChecking(cmd) == "OK":
			return True

	def isATMode(self):
		if self.sendATCommand("AT") == "OK":
			return True
		return False

	def checkATMode(self):
		while True:
			if self.isATMode():
				break
			input("The bluetooth module have not entered AT mode yet, please fix your module and then press enter")

	def getName(self):
		name = self.sendATCommandWithChecking("AT+NAME?")
		return name[name.find(":") + 1:] if name else False

	def getVersion(self):
		version = self.sendATCommandWithChecking("AT+VERSION?")
		return version[version.find(":") + 1:] if version else False

	def getAddress(self):
		address = self.sendATCommandWithChecking("AT+ADDR?")
		return address[address.find(":") + 1:] if address else False

	def getRole(self):
		role = self.sendATCommandWithChecking("AT+ROLE?")
		return int(role[role.find(":") + 1]) if role else False

	def getPassword(self):
		password = self.sendATCommandWithChecking("AT+PSWD?")
		return password[password.find(":") + 1:].replace("\"", "") if password else False

	def getUartInfo(self):
		uartInfo = self.sendATCommandWithChecking("AT+UART?")
		if uartInfo:
			parse_uartInfo = list(map(lambda x: int(x), uartInfo[uartInfo.find(":") + 1:].split(",")))
			return {"Baud Rate": parse_uartInfo[0], "Stop Bit": parse_uartInfo[1], "Parity Bit": parse_uartInfo[2]}
		else:
			return False

	def getConnectionMode(self):
		cmode = self.sendATCommandWithChecking("AT+CMODE?")
		return int(cmode[cmode.find(":") + 1:]) if cmode else False

	def getBindAddress(self):
		bind = self.sendATCommandWithChecking("AT+BIND?")
		return bind[bind.find(":") + 1:] if bind else False

	def getAllInfo(self):
		name = self.getName()
		uartInfo = self.getUartInfo()
		password = self.getPassword()
		address = self.getAddress()
		version = self.getVersion()
		role = self.getRole()
		cmode = self.getConnectionMode()
		bind = self.getBindAddress()

		return {"Name":            name if name else "",
		        "Baud Rate":       uartInfo["Baud Rate"] if uartInfo else False,
		        "Stop Bit":        uartInfo["Stop Bit"] if uartInfo else False,
		        "Parity Bit":      uartInfo["Parity Bit"] if uartInfo else False,
		        "Password":        password if password else "",
		        "Address":         address if address else "",
		        "Version":         version if version else "",
		        "Role":            role,
		        "Connection Mode": cmode,
		        "Bind Address":    bind if bind else ""}

	def set(self, settings):
		success = []
		fail = []

		isSet = False

		for setting, value in settings.items():
			if setting == "Name":
				isSet = self.setName(value)
			elif setting == "UART":
				isSet = self.setUart(value)
			elif setting == "Password":
				isSet = self.setPassword(value)
			elif setting == "Role":
				isSet = self.setRole(value)
			elif setting == "Connection Mode":
				isSet = self.setConnectionMode(value)
			elif setting == "Bind Address":
				isSet = self.setBindAddress(value)

			if isSet:
				success.append(setting)
			else:
				fail.append(setting)

		return success, fail

	def setName(self, name):
		return self.sendSettingATCommand("AT+NAME={}".format(name))

	def setUart(self, uart):
		return self.sendSettingATCommand("AT+UART={},{},{}".format(uart[0], uart[1], uart[2]))

	def setPassword(self, password):
		if not self.sendSettingATCommand("AT+PSWD={}".format(password)):
			if not self.sendSettingATCommand("AT+PSWD=\"{}\"".format(password)):
				return False
		return True

	def setRole(self, role):
		return self.sendSettingATCommand("AT+ROLE={}".format(role))

	def setConnectionMode(self, cmode):
		return self.sendSettingATCommand("AT+CMODE={}".format(cmode))

	def setBindAddress(self, address):
		addr = address.split(":")
		return self.sendSettingATCommand("AT+BIND={},{},{}".format(addr[0].zfill(4), addr[1], addr[2].zfill(6)))
