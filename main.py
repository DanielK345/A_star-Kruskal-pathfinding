import pygame
import button
import _tkinter as Tk
from tkinter import *
import Constants
from Runscreen import RunScreen 


root = Tk()


pygame.font.init()

screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
pygame.display.set_caption('Welcome To The Neighborhood game')

#load button images
button_surface = pygame.image.load("button.png")
button_surface = pygame.transform.scale(button_surface, (180, 80))
bg = pygame.image.load("a-star.png")
bg = pygame.transform.scale(bg, (800, 500))

#create button instances
start_button = button.Button(400, 230, text_input = "START", image=button_surface)
about_button = button.Button(400, 400, text_input = "ABOUT", image = button_surface)

try:
	with open("Intro.txt", 'r') as file:
		text = file.read()
		intro_text = text.strip()  # Remove leading/trailing whitespace
except FileNotFoundError:
	print(f"Error: Could not find intro text file")
	intro_text = ""
except Exception as e:  # Catch other potential errors
	print(f"Error reading intro text file: {e}")
	intro_text = ""

#game loop
run = True
while run:

	screen.blit(bg, (0,0))

	if start_button.draw(screen):
		WIDTH_RUNSCREEN = 810 
		WIN = pygame.display.set_mode((WIDTH_RUNSCREEN, WIDTH_RUNSCREEN))
		runscreen = RunScreen(WIN, WIDTH_RUNSCREEN)
		runscreen.run()
		print("")
	if about_button.draw(screen):
		myLabel = Label(root, text=intro_text, justify=LEFT, font=("Arial", 12))
		myLabel.pack(padx = 10, pady=10)
		root.mainloop()

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()