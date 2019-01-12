from port_select import *
from AT_command import *
from input_lib import get_input
from basic_info import print_basic_info

availibleBaudRate = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

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

	print("Getting Basic Information")

	print_basic_info("\nInformation of the HC-05 bluetooth module", port.getAllInfo())




	isUsePreset = get_input(str, "Do you want to use preset to set up the pair? (Y/N) ", "Invalid input, please enter again", correct=["Y", "N", "y", "n"]).upper()

	if isUsePreset == "Y":
		print("In development stage, please visit it later")
		return
	else:
		print("\n----------------------------------------------------\n")
		print("Please enter the following value to set up the pair\n")

		profile["Name"] = input("Master module's name: ")
		profile["baudRate"] = get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availibleBaudRate)
		profile["stopBit"] = get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1])
		profile["parityBit"] = get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])
