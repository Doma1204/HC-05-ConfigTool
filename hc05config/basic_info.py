from .port_select import getPort
from .AT_command import *

def get_basic_info(port=None, is_print=True):
	if not port:
		port_name = getPort("Please select the port of your HC-05: ")
		port = SerialATMode(port_name, 38400, timeout=0.5, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

	port.checkATMode()

	print("Getting Basic Information")
	
	info = port.getAllInfo()
	if is_print:
		print_basic_info("\nInformation of the HC-05 bluetooth module", info)

	return info

def print_basic_info(title, info):
	print(title)
	print("-----------------------------------------")
	print("Name: {}".format(      info["name"]       if info["name"]                     else "[No Information]"))
	print("Baud rate: {}".format( info["baud_rate"]  if info["baud_rate"] is not False   else "[No Information]"))
	print("Stop bit: {}".format(  info["stop_bit"]   if info["stop_bit"] is not False    else "[No Information]"))
	print("Parity bit: {}".format(info["parity_bit"] if info["parity_bit"] is not False  else "[No Information]"))
	print("Password: {}".format(  info["password"]   if info["password"]                 else "[No Information]"))
	print("Address: {}".format(   info["address"]    if info["address"]                  else "[No Information]"))
	print("Version: {}".format(   info["version"]    if info["version"]                  else "[No Information]"))

	if info["connection_mode"] is not False:
		if info["role"] == 0:
			print("Role: Slave(0)")
		elif info["role"] == 1:
			print("Role: Master(1)")
		elif info["role"] == 2:
			print("Role: Slave-Loop(2)")
	else:
		print("Role: [No Information]")

	print("Connection mode: {}".format(info["connection_mode"] if info["connection_mode"] is not False else "[No Information]"))
	print("Bind address: {}".format(info["bind_address"] if info["bind_address"] else "[No Information]"))
	print("-----------------------------------------\n")
