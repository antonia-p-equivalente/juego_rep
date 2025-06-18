# juego1.py
import pygame
from control_usb import leer_boton

pygame.init()
pantalla = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Juego 2")

corriendo = True
while corriendo:
    pantalla.fill((0, 255, 0))  # Fondo azul
    pygame.display.flip()

    evento = leer_boton()
    if evento == "MENU":
        corriendo = False

    pygame.time.wait(100)

pygame.quit()