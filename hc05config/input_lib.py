import re

INVALID_MESSAGE = "Invalid input, Please enter again"

AVAILABLE_BAUD_RATE = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

NAME_VALIDATE = lambda: get_input(str, "Name: ", "Invalid name, please enter again", NAME_VALIDATOR, allow_empty=True)
BAUD_RATE_VALIDATE = lambda: get_input(int, "Baud rate: ", "Invalid baud rate, please enter again", AVAILABLE_BAUD_RATE)
STOP_BIT_VALIDATE = lambda: get_input(int, "Stop bit: ", "Invalid stop bit, please enter again", [0, 1])
PARITY_BIT_VALIDATE = lambda: get_input(int, "Parity bit: ", "Invalid parity bit, please enter again", [0, 1, 2])
PASSWORD_VALIDATE = lambda: get_input(str, "Password: ", "Invalid password, please enter again", PASSWORD_VALIDATOR, allow_empty=True)
ROLE_VALIDATE = lambda: get_input(int, "Role (Slave[0], Master[1], Slave-Loop[2]): ", "Invalid role, please enter again", [0, 1, 2])
CONNECTION_MODE_VALIDATE = lambda: get_input(int, "Connection Mode [0, 1, 2]: ", "Invalid connection mode, please enter again", [0, 1, 2])
ADDRESS_VALIDATE = lambda: get_input(str, "Bind address: ", "Invalid address, please enter again", ADDRESS_VALIDATOR)

def match_pattern(pattern, string):
	match = re.match(pattern, string)
	return match is not None and match.start() == 0 and match.end() == len(string)

NAME_VALIDATOR = lambda name: match_pattern("([ -~]{0,32})", name)
BAUD_RATE_VALIDATOR = lambda baud_rate: baud_rate in AVAILABLE_BAUD_RATE
STOP_BIT_VALIDATOR = lambda stop_bit: stop_bit in [0, 1]
PARITY_BIT_VALIDATOR = lambda parity_bit: parity_bit in [0, 1, 2]
PASSWORD_VALIDATOR = lambda password: match_pattern("([ -~]{0,16})", password)
ROLE_VALIDATOR = lambda role: role in [0, 1, 2]
CONNECTION_MODE_VALIDATOR = lambda cmode: cmode in [0, 1, 2]
ADDRESS_VALIDATOR = lambda addr: match_pattern("([0-9A-F]{1,4}):([0-9A-F]{1,2}):([0-9A-F]{1,6})", addr)

BLUETOOTH_CONFIG_VALIDATE = {
	"Name": NAME_VALIDATE,
	"Baud Rate": BAUD_RATE_VALIDATE,
	"Stop Bit": STOP_BIT_VALIDATE,
	"Parity Bit": PARITY_BIT_VALIDATE,
	"Password": PASSWORD_VALIDATE,
	"Role": ROLE_VALIDATE,
	"Connection Mode": CONNECTION_MODE_VALIDATE,
	"Bind Address": ADDRESS_VALIDATE
}

MASTER_AND_SLAVE_VALIDATE = {
	""
	"Baud Rate": BAUD_RATE_VALIDATE,
	"Stop Bit": STOP_BIT_VALIDATE,
	"Parity Bit": PARITY_BIT_VALIDATE
}

def isInt(integer):
	try:
		int(integer)
		return True
	except:
		return False

def get_input(type, input_msg, wrong_msg="", correct=[], allow_empty=False):
	while True:
		ans = input(input_msg)

		if not ans:
			if allow_empty:
				return ans
			else:
				print(wrong_msg)
				continue

		if type == int:
			if not isInt(ans):
				if wrong_msg:
					print(wrong_msg)
				continue
			ans = int(ans)

		if not correct or ((callable(correct) and correct(ans)) or (not callable(correct) and ans in correct)):
			return ans

		if wrong_msg:
			print(wrong_msg)
