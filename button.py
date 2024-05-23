import pygame
import sys

pygame.init()
main_font = pygame.font.SysFont("cambria", 50)

#button class
class Button():
	def __init__(self, x, y, text_input, image = None):
               

		self.x = x
		self.y = y
		self.text_input = text_input
		self.text = main_font.render(self.text_input, True, "white")
		self.image = image
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.text_rect = self.text.get_rect(center = (self.x, self.y))
	

	def draw(self, screen):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

		return action
	

			
            
	