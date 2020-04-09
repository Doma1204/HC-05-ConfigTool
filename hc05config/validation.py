import re
from .enum_const import AVAILABLE_BAUDRATE

def _match_pattern(pattern, string):
	match = re.match(pattern, string)
	return match is not None and match.start() == 0 and match.end() == len(string)

def isNameValid(name):
	return _match_pattern("([ -~]{0,32})", name)

def isBaudrateValid(baudrate):
	return baudrate in AVAILABLE_BAUDRATE

def isStopBitValid(stopBit):
	return stopBit == 0 or stopBit == 1

def isParityBitValid(parityBit):
	return parityBit in [0, 1, 2]

def isPasswordValid(password):
	return _match_pattern("([ -~]{0,16})", password)

def isRoleValid(role):
	return role in [0, 1, 2]

def isConnectionModeValid(cmode):
	return cmode in [0, 1, 2]

def isBlutoothAddressValid(addr):
	return _match_pattern("([0-9a-fA-F]{1,4}):([0-9a-fA-F]{1,2}):([0-9a-fA-F]{1,6})", addr)

def formatBluetoothAddress(addr):
	if not isBlutoothAddressValid(addr):
		raise ValueError("Invalid Bluetooth address")
	split_addr = addr.split(":")
	return f"{split_addr[0].zfill(4)}:{split_addr[1].zfill(2)}:{split_addr[2].zfill(6)}"
