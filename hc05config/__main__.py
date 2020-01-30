from .basic_info import get_basic_info
from .bluetooth_config import bt_config
from .master_and_slave import masterAndSlave
from .preset import managePreset
from .input_lib import get_input

def main():
	while True:
		print("Please select the following job:")
		print("1. Get basic Information of the HC-05")
		print("2. Config a HC-05")
		print("3. Set up a pair of master and slave HC-05")
		print("4. Manage preset")

		selection = get_input(int, "Please enter 1-4, or press enter to exit: ", correct=range(1, 5), allow_empty=True)

		print()

		if selection == 1:
			get_basic_info()
		elif selection == 2:
			bt_config()
		elif selection == 3:
			masterAndSlave()
		elif selection == 4:
			managePreset()
		else:
			print("See you")
			break

		if selection != 4:
			input("Press enter to exit")
		print()

if __name__ == "__main__":
	main()