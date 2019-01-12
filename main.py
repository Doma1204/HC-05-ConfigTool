from basic_info import *
from Master_and_Slave import *
from input_lib import get_input

while True:
	print("Please select the following job:")
	print("1. Get basic Information of the HC-05")
	print("2. Config a HC-05")
	print("3. Set up a pair of master and slave HC-05")
	print("4. Exit")

	selection = get_input(int, "Please enter 1-4: ", correct=range(1, 5))

	print("")

	if selection == 1:
		get_basic_info()
	elif selection == 2:
		print("In development stage, please visit it later")
	elif selection == 3:
		masterAndSlave()
	elif selection == 4:
		print("GoodBye")
		break

	input("Press enter to exit")
	print("")
