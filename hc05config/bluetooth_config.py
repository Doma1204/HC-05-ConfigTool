from .port_select import getPort
from .input_lib import get_input, INVALID_MESSAGE, BLUETOOTH_CONFIG_VALIDATE
from .basic_info import get_basic_info
from .preset import selectPreset, adjustPreset, savePreset

from copy import deepcopy

def bt_config():
	port = getPort("Please select the port of your HC-05: ")

	isUsePreset = get_input(str, "Do you want to use preset to set up the pair? (Y/N) ", INVALID_MESSAGE, correct=["Y", "N", "y", "n"]).upper()

	presetReady = False
	if isUsePreset == "Y":
		config = selectPreset("Bluetooth Config")
		if config:
			presetReady = True

	if not presetReady:
		config = get_basic_info(port=port, is_print=False)
		config["UART"] = [config["Baud Rate"], config["Stop Bit"], config["Parity Bit"]]
		old_config = deepcopy(config)
		del config["UART"]
		del config["Address"]
		del config["Version"]

	print("\n----------------------------------------------------\n")
	adjustPreset(config, inputFunc=BLUETOOTH_CONFIG_VALIDATE)

	config["UART"] = [config["Baud Rate"], config["Stop Bit"], config["Parity Bit"]]
	if not presetReady:
		new_config = {}
		for key in config.keys():
			if old_config[key] != config[key]:
				new_config[key] = config[key]		

	print("Setting HC-05 bluetooth module")
	success, fail = port.set(config if presetReady else new_config)

	for item in fail:
		print("Fail to set {}".format(item))
	
	print("Setting completed")

	del config["UART"]
	savePreset("Bluetooth Config", config)