INVALID_MESSAGE = "Invalid input, Please enter again"

def isInt(integer):
	try:
		int(integer)
		return True
	except:
		return False

def get_input(type, input_msg, wrong_msg="", correct=[]):
	while True:
		ans = input(input_msg)

		if type == int:
			if not isInt(ans):
				if wrong_msg:
					print(wrong_msg)
				continue
			ans = int(ans)
		# print(not correct)
		# print(((callable(correct) and correct(ans)) or ans in correct))
		# print((callable(correct) and correct(ans)))
		# print(ans in correct)
		if not correct or ((callable(correct) and correct(ans)) or (not callable(correct) and ans in correct)):
			return ans

		if wrong_msg:
			print(wrong_msg)
