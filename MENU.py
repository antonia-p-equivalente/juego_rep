import pygame
import subprocess
import sys

pygame.init()
screen = pygame.display.set_mode((480, 240))
pygame.display.set_caption("Menú de Juegos")

font = pygame.font.SysFont("Arial", 50)
clock = pygame.time.Clock()

juegos = [
    {"nombre": "juego1", "path": "anathema/anathema_adaptado_botones.py"},
    {"nombre": "juego2", "path": "juego2/juego2.py"},
]

seleccionado = 0

def dibujar_menu():
    screen.fill((0, 0, 0))
    for i, juego in enumerate(juegos):
        color = (255, 255, 0) if i == seleccionado else (200, 200, 200)
        texto = font.render(juego["nombre"], True, color)
        rect = texto.get_rect(center=(240 + (i - 0.5) * 200, 120))
        screen.blit(texto, rect)
    pygame.display.flip()

def ejecutar_juego(path):
    try:
        subprocess.run(["python3", path])
    except FileNotFoundError:
        print(f"No se encontró el archivo del juego: {path}")

running = True
while running:
    dibujar_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                seleccionado = (seleccionado + 1) % len(juegos)
            elif event.key == pygame.K_LEFT:
                seleccionado = (seleccionado - 1) % len(juegos)
            elif event.key == pygame.K_RETURN:
                ejecutar_juego(juegos[seleccionado]["path"])

    clock.tick(30)

pygame.quit()
sys.exit()

