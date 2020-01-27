from .port_select import *
from .AT_command import *
from .input_lib import *
from .basic_info import *
from .preset import *

availableBaudRate = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

def bt_config():
	port_name = getPort("Please select the port of your HC-05: ")
	port = SerialATMode(port_name, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

	isUsePreset = get_input(str, "Do you want to use preset to set up the pair? (Y/N) ", INVALID_MESSAGE, correct=["Y", "N", "y", "n"]).upper()

	configReady = False
	if isUsePreset == "Y":
		config = selectPreset("BT_Config")
		if config:
			configReady = True

	if not configReady:
		config = get_basic_info(port=port, is_print=False)
		del config["address"]
		del config["version"]
	
	print("\n----------------------------------------------------\n")
	adjustPreset(config, inputFunc={
		"baud_rate": lambda: get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", availableBaudRate),
		"stop_bit": lambda: get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1]),
		"parity_bit": lambda: get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2]),
		"password": lambda: get_input(str, "Password: ", "Invalid password, please enter again", lambda x: isInt(x) and len(x) == 4),
		"role": lambda: get_input(int, "Role (Slave[0], Master[1], Slave-Loop[2]): ", "Invalid role, please enter again", [0, 1, 2]),
		"connection_mode": lambda: get_input(int, "Connection Mode [0, 1, 2]: ", "Invalid connection mode, please enter again", [0, 1, 2]),
		"bind_address": lambda: get_input(str, "Bind address: ", "Invalid address, please enter again", lambda x: len(x.split(":")) == 3)
	})

	print("Setting HC-05 bluetooth module")

	config["uart"] = [config["baud_rate"], config["stop_bit"], config["parity_bit"]]
	success, fail = port.set(config)

	for item in fail:
		print("Fail to set {}".format(item))
	
	print("Setting completed")

	del config["uart"]
	savePreset("BT_Config", config)