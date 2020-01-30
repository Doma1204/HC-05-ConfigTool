from serial.tools.list_ports import comports as listPorts
from serial.serialutil import SerialException
from .AT_command import *
from .input_lib import get_input

def getPortName(info_msg):
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

def getPort(info_msg):
	while True:
		port_name = getPortName(info_msg)
		try:
			return SerialATMode(port_name, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
		except SerialException:
			print("\"{}\" is currently busy, please select other port\n".format(port_name))
