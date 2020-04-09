from enum import Enum, IntEnum

NAME = "Name"
BAUDRATE = "Baudrate"
STOP_BIT = "Stop Bit"
PARITY_BIT = "Parity Bit"
PASSWORD = "Password"
ADDRESS = "Address"
VERSION = "Version"
ROLE = "Role"
CONNECTION_MODE = "Connection Mode"
BIND_ADDRESS = "Bind Address"

AVAILABLE_GET_INFO = [NAME, BAUDRATE, STOP_BIT, PARITY_BIT, PASSWORD, ADDRESS, VERSION, ROLE, CONNECTION_MODE, BIND_ADDRESS]
AVAILABLE_SET_INFO = [NAME, BAUDRATE, STOP_BIT, PARITY_BIT, PASSWORD, ROLE, CONNECTION_MODE, BIND_ADDRESS]
AVAILABLE_BAUDRATE = [4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1382400]

class ATState(Enum):
	SUCCESS = 0          # There is response and the response is valid
	FAIL = 1             # There is no response but AT mode is active
	ERROR = 2            # There is response but the response is error
	NOT_IN_AT_MODE = 3   # There is no response and AT mode is inactive


class StopBit(IntEnum):
	ONE_BIT = 0
	TWO_BIT = 1

class ParityBit(IntEnum):
	NONE_PARITY = 0
	ODD_PARITY = 1
	EVEN_PARITY = 2

class Role(IntEnum):
	SLAVE_ROLE = 0
	MASTER_ROLE = 1
	SLAVE_LOOP_ROLE = 2

class ConnectionMode(IntEnum):
	SPECIFIED_ADDRESS = 0
	ANY_ADDRESS = 1
	SLAVE_LOOP = 2
