from .port_select import getPort

def get_basic_info(port=None, is_print=True):
	if not port:
		port = getPort("Please select the port of your HC-05: ")

	port.checkATMode()

	print("Getting Basic Information")
	
	info = port.getAllInfo()
	if is_print:
		print_basic_info("\nInformation of the HC-05 bluetooth module", info)

	return info

def print_basic_info(title, info):
	print(title)
	print("-----------------------------------------")
	print("Name: {}".format(      info["Name"]       if info["Name"]                     else "[No Information]"))
	print("Baud rate: {}".format( info["Baud Rate"]  if info["Baud Rate"] is not False   else "[No Information]"))
	print("Stop bit: {}".format(  info["Stop Bit"]   if info["Stop Bit"] is not False    else "[No Information]"))
	print("Parity bit: {}".format(info["Parity Bit"] if info["Parity Bit"] is not False  else "[No Information]"))
	print("Password: {}".format(  info["Password"]   if info["Password"]                 else "[No Information]"))
	print("Address: {}".format(   info["Address"]    if info["Address"]                  else "[No Information]"))
	print("Version: {}".format(   info["Version"]    if info["Version"]                  else "[No Information]"))

	if info["Connection Mode"] is not False:
		if info["Role"] == 0:
			print("Role: Slave(0)")
		elif info["Role"] == 1:
			print("Role: Master(1)")
		elif info["Role"] == 2:
			print("Role: Slave-Loop(2)")
	else:
		print("Role: [No Information]")

	print("Connection mode: {}".format(info["Connection Mode"] if info["Connection Mode"] is not False else "[No Information]"))
	print("Bind address: {}".format(info["Bind Address"] if info["Bind Address"] else "[No Information]"))
	print("-----------------------------------------\n")
