from .basic_info import get_basic_info
from .bluetooth_config import bt_config
from .master_and_slave import masterAndSlave
from .preset import viewPreset
from .input_lib import get_input

def main():
	while True:
		print("Please select the following job:")
		print("1. Get basic Information of the HC-05")
		print("2. Config a HC-05")
		print("3. Set up a pair of master and slave HC-05")
		print("4. View preset")
		print("5. Exit")

		selection = get_input(int, "Please enter 1-5: ", correct=range(1, 6))

		print("")

		if selection == 1:
			get_basic_info()
		elif selection == 2:
			bt_config()
		elif selection == 3:
			masterAndSlave()
		elif selection == 4:
			viewPreset()
		elif selection == 5:
			print("See you")
			break

		input("Press enter to exit")
		print("")

if __name__ == "__main__":
	main()