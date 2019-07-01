import turing
import turingGUI
import sys

exampleProgram = turing.Program()
exampleProgram.addLine(1, 1, 1, 'r', 1)
exampleProgram.addLine(1, 0, 1, 'r', 2)
exampleProgram.addLine(2, 0, 1, 'r', 0)

exampleTapeInput = [1,1]

examplemachine = turing.TuringMachine(exampleTapeInput, exampleProgram)

program = None
tapeinput = None
def handleInput(cur_input, program, newTapeinput):
	try:
		inputs[cur_input](program)
	#is the input a valid command(does it precisely correspond to a key string in inputs)
	except KeyError:
		print("Invalid input")
	#does the valid command not take program as a parameter
	except TypeError:
		try:
			inputs[cur_input]()
		except TypeError:
			inputs[cur_input](program, newTapeinput)

def help():
	print("""Welcome to Simon's turing machine EXTRAVAGANZA.\n Before you can run a program both the program and the tape have to be declared.""")
	print("Available commands:")
	for available_input in inputs:
		print(available_input)

def newProgram():
	global program
	program = turing.Program()
	print("new program created")

def newTapeinput():
	global tapeinput
	print("Input should either be 1 or 0, write the input should be put like this, 1 0 1...")
	tapeinput = input()
	temp_list = []
	for char in tapeinput:
		if char == "0":
			temp_list.append(int(char))
		elif char == "1":
			temp_list.append(int(char))
		elif char == "B":
			temp_list.append(char)
	if len(temp_list) != 0:
		tapeinput = temp_list

def getProgramLine(program):
	#Current state or escape
	try:
		curstate = input("Current state: ")
		if curstate != "exit":
			curstate = int(curstate)
			if curstate < 0:
				raise ValueError
		else:
			return
	except ValueError:
		print("To escape enter exit or enter a positive integer.")
		while True:
			try:
				curstate = input("Current state: ")
				if curstate != "exit":
					curstate = int(curstate)
					if curstate < 0:
						raise ValueError
					else:
						break
				else:
					return
			except ValueError:
				print("To escape enter exit or enter a positive integer.")
	
	#Observed state or escape
	try:
		observed = input("Observed state: ")
		if observed != "exit":
			if observed != 'B':
				observed = int(observed)
				if observed != 1 and observed != 0:
					raise ValueError
		else:
			return
	except ValueError:
		print("To escape enter exit else please enter either 0, 1 or B.")
		while True:
			try:
				observed = input("Observed state: ")
				if observed != "exit":
					if observed != 'B':
						observed = int(observed)
						if observed != 1 and observed != 0:
							raise ValueError
						else:
							break
				else:
					return
			except ValueError:
				print("To escape enter exit else please enter either 0, 1 or B.")

	#Write state or escape
	try:
		writestate = input("Write state: ")
		if writestate != "exit":
			if writestate != 'B':
				writestate = int(writestate)
				if writestate != 1 and writestate != 0:
					raise ValueError
		else:
			return
	except ValueError:
		print("To escape enter exit else please enter either 0, 1 or B.")
		while True:
			try:
				writestate = input("Write state: ")
				if writestate != "exit":
					if writestate != 'B':
						writestate = int(writestate)
						if writestate != 1 and writestate != 0:
							raise ValueError
						else:
							break
				else:
					return
			except ValueError:
				print("To escape enter exit else please enter either 0, 1 or B.")

	#Move or escape
	try:
		move = input("Move l or r: ")
		if move == "exit":
			return
		elif move != "l" and move != "r":
			raise ValueError
	except ValueError:
		print("To escape enter exit or enter either l or r.")
		while True:
			try:
				move = input("Move l or r: ")
				if move == "exit":
					return
				elif move != 'l' and move != 'r':
					raise ValueError
				break
			except ValueError:
				print("To escape enter exit or enter either l or r.")

	#New state or escape
	try:
		newstate = input("New state: ")
		if newstate != "exit":
			newstate = int(newstate)
			if newstate < 0:
				raise ValueError
		else:
			return
	except ValueError:
		print("To escape enter exit or enter a positive integer.")
		while True:
			try:
				newstate = input("Current state: ")
				if newstate != "exit":
					newstate = int(curstate)
					if newstate < 0:
						raise ValueError
					else:
						break
				else:
					return
			except ValueError:
				print("To escape enter exit or enter a positive integer.")

	#Add the line information gathered to the program
	program.addLine(curstate, observed, writestate, move, newstate)
	return True

def getProgramLines(program):
	programUnchanged = False
	while not programUnchanged:
		if getProgramLine(program) == None:
			programUnchanged = True
		else:
			print(program)

def runProgram(program, tape):
	turMachine = turing.TuringMachine(tape, program)
	while True:	
		current_line = turMachine.program.returnLine(turMachine.programstate, turMachine.tape[turMachine.tapeindex])
		print(current_line)
		direction = current_line[1]
		if not turMachine.executenextLine():
			print(turMachine.tape)
		else:
			break

def runProgramGUI(program, tape):
	turMachine = turing.TuringMachine(tape, program)
	turingGUI.main(turMachine)
x = lambda program  : a + 10
inputs = {"help": help, "new program" : newProgram, "tapeinput" : lambda program, tapeinput: print(tapeinput), "new tapeinput" : newTapeinput, "add line" : getProgramLine, "add lines": getProgramLines, "program" : print, "run program" : runProgram, "run program GUI" : runProgramGUI, "exit" : sys.exit}

if __name__ == '__main__':
	help()

	while True:
		cur_input = input("$ ")
		handleInput(cur_input, program, tapeinput)

