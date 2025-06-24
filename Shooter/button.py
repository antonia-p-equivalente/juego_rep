import pygame 

#button class
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.selected = False  # <<----- agrega esta línea

	def draw(self, surface):
		action = False

		# Dibujar borde si está seleccionado
		if self.selected:
			pygame.draw.rect(surface, (255, 255, 0), self.rect.inflate(10, 10), 4)  # borde amarillo

		# Dibujar botón
		surface.blit(self.image, (self.rect.x, self.rect.y))

		# Interacción con mouse (solo si tienes mouse)
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action
	
