from port_select import *
from AT_command import *
from input_lib import *
from basic_info import *
from preset import *

availableBaudRate = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

profile = {
	"Name": "",
	"baudRate": "",
	"stopBit",
	"parityBit",
}

def bt_config():
	port_name = getPort("Please select the port of your HC-05: ")
	port = SerialATMode(port_name, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

	while True:
		if port.isATMode():
			break
		input("The bluetooth module have not entered AT mode yet, please fix your module and then press enter")

	isUsePreset = get_input(str, "Do you want to use preset to set up the pair? (Y/N) ", INVALID_MESSAGE, correct=["Y", "N", "y", "n"]).upper()

	configReady = False
	if isUsePreset == "Y":
		preset = selectPreset("Master_and_Slave")
		if preset:
			adjustPreset(preset, inputFunc={
				"baudRate": lambda: get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availibleBaudRate),
				"stopBit": lambda: get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1]),
				"parityBit": lambda: get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])
			})
			configReady = True
	if not configReady:
		config = get_basic_info()
		print("\n----------------------------------------------------\n")
		adjustPreset(config, inputFunc={
			
		})

		print("Please enter the following value to set up the pair\n")

		profile["Name"] = input("Master module's name: ")
		profile["baudRate"] = get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availibleBaudRate)
		profile["stopBit"] = get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1])
		profile["parityBit"] = get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])
	
