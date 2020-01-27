from .port_select import *
from .AT_command import *
from .bluetooth_config import availableBaudRate
from .input_lib import *
from .basic_info import print_basic_info
from .preset import *

# Setting up master and slave bluetooth module:
# 1. Check if the firmware version of the two module are the same, otherwise they cannot pair up
# 2. Set the name of master and slave module
# 3. Set the corresponding baud rate, stop bit and parity bit
# 4. Set the password of the two bluetooth to be the same
# 5. Set the role of the two bluetooth to corresponding role
# 6. Set the cmode to 0
# 7. Get the address of the two bluetooth
# 8. Set the bind address of the two bluetooth to the opposite one
# 9. Reset the two bluetooth

def masterAndSlave():
	print("1. Set up master and slave pair with one serial port")
	print("2. Set up master and slave pair with two serial port")

	setupMethod = get_input(int, "Please select your desire set up method(1-2): ", INVALID_MESSAGE, [1, 2])
	isUsePreset = get_input(str, "Do you want to use preset to set up the pair? (Y/N) ", INVALID_MESSAGE, correct=["Y", "N", "y", "n"]).upper()

	configReady = False
	if isUsePreset == "Y":
		profile = selectPreset("Master_and_Slave")
		if profile:
			adjustPreset(profile, inputFunc={
				"baud_rate": lambda: get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availableBaudRate),
				"stop_bit": lambda: get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1]),
				"parity_bit": lambda: get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])
			})
			configReady = True

	if not configReady:
		print("\n----------------------------------------------------\n")
		print("Please enter the following value to set up the pair\n")

		profile = {}
		profile["masterName"] = input("Master module name: ")
		profile["slaveName"] = input("Slave module Name: ")
		profile["baud_rate"] = get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availableBaudRate)
		profile["stop_bit"] = get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1])
		profile["parity_bit"] = get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])

	if setupMethod == 1:
		masterAndSlave_oneSerial(profile)
	else:
		masterAndSlave_twoSerial(profile)

	savePreset("Master_and_Slave", profile)

def masterAndSlave_oneSerial(profile):
	print("\n----------------------------------------------------\n")
	portName = getPort("Please select your port: ")
	port = SerialATMode(portName, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

	print("\nPlease connect your master module to the port and make sure it is in AT mode")
	input("When you have done, Please press enter to continue")
	port.checkATMode()

	masterAddress = port.getAddress()

	print("\nPlease connect your slave module to the port and make sure it is in AT mode")
	input("When you have done, Please press enter to continue")
	port.checkATMode()

	slaveAddress = port.getAddress()

	slave_profile = {
		"name": profile["slaveName"],
		"uart": [profile["baud_rate"], profile["stop_bit"], profile["parity_bit"]],
		"password": "0000",
		"connection_mode": 0,
		"bind_address": masterAddress,
		"role": 0
	}

	print("Setting slave bluetooth module")
	slaveSuccess, slaveFail = port.set(slave_profile)

	for fail in slaveFail:
		print("Fail to set slave {}".format(fail))

	print_basic_info("Infomation of slave bluetooth module", port.getAllInfo())

	print("\nPlease connect your master module to the port and make sure it is in AT mode")
	input("When you have done, Please press enter to continue")

	while True:
		if port.isATMode():
			break
		input("The bluetooth module have not entered AT mode yet, please fix your module and then press enter")

	master_profile = {
		"name": profile["masterName"],
		"uart": [profile["baud_rate"], profile["stop_bit"], profile["parity_bit"]],
		"password": "0000",
		"connection_mode": 0,
		"bind_address": slaveAddress,
		"role": 1
	}

	print("Setting master bluetooth module")
	masterSuccess, masterFail = port.set(master_profile)

	for fail in masterFail:
		print("Fail to set master {}".format(fail))
	
	print_basic_info("Infomation of slave bluetooth module", port.getAllInfo())

	if masterFail or slaveFail:
		print("Fail to pair up the two bluetooth module as master and slave")
	else:
		print("Master and slave bluetooth module pair up successfully")

	port.sendATCommand("AT+RESET")

def masterAndSlave_twoSerial(profile):
	while True:
		print("\n----------------------------------------------------\n")
		masterPortName = getPort("Please select your master bluetooth port: ")
		print("\n----------------------------------------------------\n")
		slavePortName = getPort("Please select your slave bluetooth port: ")
		print()

		if masterPortName == slavePortName:
			print("Master and slave bluetooth port cannot be the same, please select again\n")
		else:
			break

	print("\nMaster: {}".format(masterPortName))
	print("Slave: {}\n".format(slavePortName))

	masterPort = SerialATMode(masterPortName, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
	slavePort = SerialATMode(slavePortName, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

	masterPort.checkATMode()
	slavePort.checkATMode()

	masterAddress = masterPort.getAddress()
	slaveAddress = slavePort.getAddress()

	master_profile = {
		"name": profile["masterName"],
		"uart": [profile["baud_rate"], profile["stop_bit"], profile["parity_bit"]],
		"password": "0000",
		"role": 1,
		"connection_mode": 0,
		"bind_address": slaveAddress
	}

	slave_profile = {
		"name": profile["slaveName"],
		"uart": [profile["baud_rate"], profile["stop_bit"], profile["parity_bit"]],
		"password": "0000",
		"role": 0,
		"connection_mode": 0,
		"bind_address": masterAddress
	}

	print("Setting master bluetooth module")
	masterSuccess, masterFail = masterPort.set(master_profile)

	for fail in masterFail:
		print("Fail to set master {}".format(fail))

	print("Setting slave bluetooth module")
	slaveSuccess, slaveFail = slavePort.set(slave_profile)

	for fail in slaveFail:
		print("Fail to set slave {}".format(fail))

	if masterFail or slaveFail:
		print("Fail to pair up the two bluetooth module as master and slave")
	else:
		print("Master and slave bluetooth module pair up successfully")

	print("The following are the information of the two module:\n")

	print_basic_info("Infomation of master bluetooth module", masterPort.getAllInfo())
	print_basic_info("Information of slave bluetooth module", slavePort.getAllInfo())

	masterPort.sendATCommand("AT+RESET")
	slavePort.sendATCommand("AT+RESET")