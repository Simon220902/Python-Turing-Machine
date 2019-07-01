#Program: Currentstate, observed number, write number, move, new state
class Program:
	def __init__(self):
		self.program = {}

	def addLine(self, curstate, observed, write, move, newstate):
		#see if the state exists.
		try:
			if observed == 'B':
				self.program[curstate][2] = (write, move, newstate)
			else:
				self.program[curstate][observed] = (write, move, newstate)
		except KeyError:
			if observed == 1:
				self.program[curstate] = [None, (write, move, newstate), None]
			elif observed == 0:
				self.program[curstate] = [(write, move, newstate), None, None]
			elif observed == 'B':
				self.program[curstate] = [None, None, (write, move, newstate)]

	def returnLine(self, curstate, observed):
		#see if the state exists and if it can handle the current input else terminate.
		try:
			if observed != 'B':
				return self.program[curstate][observed]
			else:
				return self.program[curstate][2]
		except IndexError:
			try:
				self.program[curstate]
				#Print which state does not ex
				raise IndexError("The input you get for the current state is not handled.\nState: %i Input: %i"%(curstate, observed))
				#Terminate the program by writing what is currently on the tape and going right and to state 0
				return (curstate, 'r', 0)
			except IndexError:
				raise IndexError("The state you are calling does not exist.\n State: %i"%(curstate))
				#Terminate the program by writing what is currently on the tape and going right and to state 0
				return (curstate, 'r', 0)

	def __str__ (self):
		lines = "| Curstate |  ObsNum  |  Write   |   Move   | NewState |\n"
		def center10(s):
			lenspaces= 10-len(s)
			if lenspaces > 0:
				if lenspaces%2 == 0:
					spaces = ""
					for i in range(int(lenspaces/2)):
						spaces += (" ")
					return spaces + s + spaces
				else:
					spaces1 = ""
					spaces2 = ""
					for i in range(int((lenspaces/2)-0.5)):
						spaces1 += " "
					for i in range(int((lenspaces/2)+0.5)):
						spaces2 += " "
					return spaces1 + s + spaces2
			else:
				return s
		for curstate, program_list in self.program.items():
			#set the curstate data under the curstate column
			current_line = "|"+center10(str(curstate))+"|"
			#the reason for the explicit list, is that 
			for program_tuple in range(len(program_list)):
				if program_list[program_tuple] == None:
					pass
				else:
					lines += current_line + center10(str(program_tuple))+"|"+center10(str(program_list[program_tuple][0]))+"|"+center10(str(program_list[program_tuple][1]))+"|"+center10(str(program_list[program_tuple][2]))+"|\n"
		return lines


class TuringMachine:
	def __init__(self, tapeinput, program):
		self.program = program #this shall be an object of the Program class
		self.programstate = 1 #The state always starts at one and terminates at zero.
		self.tape = tapeinput #the tape input needs to be at least a list with one element which is a one, the first element of the inputtape shall always be a one.
		self.tapeindex = 0 #shall start at the tapeinput

	def moveRead(self, direction):
		#Add a blank space to the tape if it hits the right most border of the tape
		if direction == "r" and self.tapeindex == len(self.tape)-1:
			self.tape = self.tape + ['B']
			self.tapeindex += 1
		#Add a blank space to the left of tape when it hits the left most border of the tape
		elif direction == "l" and self.tapeindex == 0:
			self.tape = ['B'] + self.tape
		elif direction == "r":
			self.tapeindex += 1
		else:
			self.tapeindex -= 1

	def executenextLine(self):
		line = self.program.returnLine(self.programstate, self.tape[self.tapeindex])
		self.tape[self.tapeindex] = line[0]
		self.moveRead(line[1])
		if line[2] != 0:
			self.programstate = line[2]
		else:
			self.programstate = 0
			return self.tape