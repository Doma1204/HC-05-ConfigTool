INVALID_MESSAGE = "Invalid input, Please enter again"

def get_input(type, input_msg, wrong_msg="", correct=[]):
	while True:
		ans = input(input_msg)

		if type == int:
			try:
				ans = int(ans)
			except:
				print(wrong_msg)
				continue

		if ans in correct or not correct:
			return ans

		if wrong_msg:
			print(wrong_msg)
