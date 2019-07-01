import turing
import pygame
import sys
#curstate, observed, write, move, newstate)

pygame.init()

WIDTH, HEIGHT = 700, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
PINK  = [255,   0, 100]
tapeSeparation = [WIDTH/7, WIDTH/7*2, WIDTH/7*3, WIDTH/7*4, WIDTH/7*5, WIDTH/7*6, WIDTH] 
tapeFont = pygame.font.Font('freesansbold.ttf', 100)
headFont = pygame.font.Font('freesansbold.ttf', 50)
buttonFont = pygame.font.Font('freesansbold.ttf', 20)
running = True

def drawTape(tape, tapeIndex):
	#clear the current tape
	pygame.draw.rect(SCREEN, BLACK, (0, HEIGHT/4*2, WIDTH, 100))
	#Upper and lower line of the tape.
	pygame.draw.line(SCREEN, WHITE, (0, HEIGHT/4*2), (WIDTH, HEIGHT/4*2))
	pygame.draw.line(SCREEN, WHITE, (0, HEIGHT/4*3), (WIDTH, HEIGHT/4*3))
	#The seperating lines between each of the dataspaces
	for tapeSepI in range(6):
		pygame.draw.line(SCREEN, WHITE, (tapeSeparation[tapeSepI], HEIGHT/4*2), (tapeSeparation[tapeSepI], HEIGHT/4*3))
	#setting the font for the data
	tapeFont = pygame.font.Font('freesansbold.ttf', 100)
	#this is just to ensure that the following list indexing functions don't fail since the displayed tape needs at least three 
	if tapeIndex < 3 or len(tape) <= tapeIndex+3:
		tape = ['B', 'B', 'B', 'B', 'B'] + tape + ['B', 'B', 'B', 'B', 'B']
		tapeIndex += 5
	#Create a list of the symbols shown on screen so the left most symbol has index 0 and the current tapesymbol has index 3 and the right most symbol has index 6.
	tapeSymbols = tape[tapeIndex-3:tapeIndex+4]

	for symbol in range(7):
		SCREEN.blit(tapeFont.render(str(tapeSymbols[symbol]), True, WHITE), (tapeSeparation[symbol]-100, HEIGHT/4*2))

def drawHead(state):
	pygame.draw.polygon(SCREEN, WHITE, [(WIDTH/2, HEIGHT/4*2), (WIDTH/7*2, HEIGHT/8), (WIDTH/7*5, HEIGHT/8)])
	pygame.draw.polygon(SCREEN, BLACK, [(WIDTH/2, HEIGHT/4*2-20), (WIDTH/7*2+40, HEIGHT/8+20), (WIDTH/7*5-40, HEIGHT/8+20)])
	stateSurf = headFont.render(str(state), True, PINK)
	SCREEN.blit(stateSurf, (WIDTH/2 - stateSurf.get_width()/2,HEIGHT/4-20))

def drawNextStep():
	pygame.draw.rect(SCREEN, WHITE, (tapeSeparation[5], HEIGHT/4*3+50-20, 100, 40 ))
	SCREEN.blit(buttonFont.render("Next step", True, BLACK), (tapeSeparation[5]+5, HEIGHT/4*3+50-20+12))

def nextClicked(coord, TurMachine):
	if coord[0] <= tapeSeparation[5]+100 and coord[0] >= tapeSeparation[5] and coord[1] >= HEIGHT/4*3+30 and coord[1] <= HEIGHT/4*3+70 and running:
		Step(TurMachine)

def Step(TurMachine):
	previousTapeindex = TurMachine.tapeindex
	current_line = TurMachine.program.returnLine(TurMachine.programstate, TurMachine.tape[TurMachine.tapeindex])
	direction = current_line[1]
	if not TurMachine.executenextLine():
		drawHead(TurMachine.programstate)
		drawTape(TurMachine.tape, previousTapeindex)
		pygame.time.wait(200)
		drawTape(TurMachine.tape, TurMachine.tapeindex)
		pygame.display.flip()
	else:
		global running
		running = False
		SCREEN.fill(BLACK)
		drawHead(TurMachine.programstate)
		drawTape(TurMachine.tape, TurMachine.tapeindex)
		pygame.display.flip()

def main(TurMachine):

	SCREEN.fill(BLACK)
	drawNextStep()
	drawHead(TurMachine.programstate)
	drawTape(TurMachine.tape, TurMachine.tapeindex)
	pygame.display.flip()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				nextClicked(pygame.mouse.get_pos(), TurMachine)
	
	font = pygame.font.SysFont("Arial", 50)
	text = font.render("Use Left and Right Keys to move the tape", True, (255,255,255))
	SCREEN.blit(text, (WIDTH/2 - text.get_rect()[2]/2, text.get_rect()[3]/2))
	pygame.display.flip()

	while True:
		direction = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				elif event.key == pygame.K_LEFT:
					direction = 'l'
				elif event.key == pygame.K_RIGHT:
					direction = 'r'
		if direction != None:
			TurMachine.moveRead(direction)
			drawHead(TurMachine.programstate)
			drawTape(TurMachine.tape, TurMachine.tapeindex)
			pygame.display.flip()