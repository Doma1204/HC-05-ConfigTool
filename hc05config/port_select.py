from serial.tools.list_ports import comports as listPorts
from .input_lib import get_input

def getPort(info_msg):
	while True:
		print("Available Ports:")
		ports = list(map(lambda x: x.device, listPorts()))
		for i, port in enumerate(ports):
			print("{}: {}".format(i + 1, port))

		print("{}: Rescan serial port\n".format(i + 2))

		selection = get_input(int, info_msg, "The input is invalid, please enter again", range(1, len(ports) + 2)) - 1

		if selection in range(len(ports)):
			return ports[selection]

		print()
