import pygame 

# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.selected = False  # marca si el botón está enfocado

    def draw(self, surface):
        # Dibujar borde si está seleccionado
        if self.selected:
            pygame.draw.rect(
                surface, (255, 255, 0),
                self.rect.inflate(10, 10), 4
            )
        # Dibujar imagen
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def handle_press(self, press):
        """
        press: cadena retornada por leerBoton.leer_boton()
        Devuelve True si:
          - Se presionó 'A'
          - Este botón está seleccionado
          - Aún no estaba marcado como 'clicked'
        """
        if press == 'A' and self.selected and not self.clicked:
            self.clicked = True
            return True
        # Resetear clicked cuando no hay presión
        if press is None:
            self.clicked = False
        return False
