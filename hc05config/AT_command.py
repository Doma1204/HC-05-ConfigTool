import serial
from time import sleep

delay = 0.01
delayTime = 50
settingMaxTime = 5

class SerialATMode(serial.Serial):
	def sendATCommand(self, cmd, raw=False):
		if not self.is_open:
			self.open()

		cmd += "\r\n"
		self.write(cmd.encode())

		time = 0
		while True:
			while self.in_waiting:
				text = self.readlines()
				try:
					return text if raw else text[0].decode("UTF-8")[:-2]
				except:
					return False

			if (time >= delayTime):
				return False
			time += 1
			sleep(delay)

	def sendSettingATCommand(self, cmd):
		tryTime = 0
		while True:
			tryTime += 1
			if self.sendATCommand(cmd) == "OK":
				return True
			elif tryTime >= settingMaxTime:
				return False

	def isATMode(self):
		if self.sendATCommand("AT") == "OK":
			return True
		if self.sendATCommand("AT") == "OK":
			return True
		return False

	def checkATMode(self):
		while True:
			if self.isATMode():
				break
			input("The bluetooth module have not entered AT mode yet, please fix your module and then press enter")

	def getName(self):
		name = self.sendATCommand("AT+NAME?")
		return name[name.find(":") + 1:] if name else False

	def getVersion(self):
		version = self.sendATCommand("AT+VERSION?")
		return version[version.find(":") + 1:] if version else False

	def getAddress(self):
		address = self.sendATCommand("AT+ADDR?")
		return address[address.find(":") + 1:] if address else False

	def getRole(self):
		role = self.sendATCommand("AT+ROLE?")
		return int(role[role.find(":") + 1]) if role else False

	def getPassword(self):
		password = self.sendATCommand("AT+PSWD?")
		return password[password.find(":") + 1:].replace("\"", "") if password else False

	def getUartInfo(self):
		uartInfo = self.sendATCommand("AT+UART?")
		if uartInfo:
			parse_uartInfo = list(map(lambda x: int(x), uartInfo[uartInfo.find(":") + 1:].split(",")))
			return {"baud_rate": parse_uartInfo[0], "stop_bit": parse_uartInfo[1], "parity_bit": parse_uartInfo[2]}
		else:
			return False

	def getConnectionMode(self):
		cmode = self.sendATCommand("AT+CMODE?")
		return cmode[cmode.find(":") + 1:] if cmode else False

	def getBindAddress(self):
		bind = self.sendATCommand("AT+BIND?")
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

		return {"name":            name if name else "",
		        "baud_rate":       uartInfo["baud_rate"] if uartInfo else False,
		        "stop_bit":        uartInfo["stop_bit"] if uartInfo else False,
		        "parity_bit":      uartInfo["parity_bit"] if uartInfo else False,
		        "password":        password if password else "",
		        "address":         address if address else "",
		        "version":         version if version else "",
		        "role":            role,
		        "connection_mode": cmode,
		        "bind_address":    bind if bind else ""}

	def set(self, settings):
		success = []
		fail = []

		isSet = False

		for setting, value in settings.items():
			if setting == "name":
				isSet = self.setName(value)
			elif setting == "uart":
				isSet = self.setUart(value)
			elif setting == "password":
				isSet = self.setPassword(value)
			elif setting == "role":
				isSet = self.setRole(value)
			elif setting == "connection_mode":
				isSet = self.setConnectionMode(value)
			elif setting == "bind_address":
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
