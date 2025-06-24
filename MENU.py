import pygame
import os
import sys
import subprocess
from leerBoton import leer_boton

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Menú de Juegos")
    font = pygame.font.Font(None, 36)  # Tamaño de letra más legible
    clock = pygame.time.Clock()

    # 1) Definimos la lista de juegos:
    #    ("Etiqueta visible", "ruta/al/script.py")
    games = [
        ("Anathema", os.path.join("anathema", "anathema_adaptado_botones.py")),
        ("Juego2", "juego2.py"),
        ("Shooter", os.path.join("Shooter", "JUEGO DISEÑO.py"))
       
    ]

    current = 0   # Índice de la opción resaltada
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    current = (current + 1) % len(games)
                elif e.key == pygame.K_UP:
                    current = (current - 1) % len(games)
                elif e.key == pygame.K_RETURN:
                    # Al presionar Enter lanzamos el script
                    _, path = games[current]
                    subprocess.Popen(["python3", path])
                    running = False

        # 2) Dibujamos fondo negro
        screen.fill((0, 0, 0))

        # 3) Recorremos todas las opciones y pintamos el texto
        for idx, (label, _) in enumerate(games):
            color = (255, 255, 255)                  # Blanco por defecto
            if idx == current:
                color = (200, 200, 200)              # Gris claro para seleccionado
            txt_surf = font.render(label, True, color)
            screen.blit(txt_surf, (50, 50 + idx * 40))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
