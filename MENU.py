


#!/usr/bin/env python3
import pygame
import sys
import subprocess
import os
from leerBoton import leer_boton

# ——— Configuración básica ———
SCREEN_WIDTH  = 480
SCREEN_HEIGHT = 320
FPS           = 30

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú de Juegos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Lista de juegos: (Etiqueta, comando como lista de args)
    games = [
        ("Anathema", ["python3", os.path.join("anathema","anathema_adaptado_botones.py")]),
        ("Shooter",  ["python3", os.path.join("Shooter","JUEGO DISEÑO.py")]),
        ("Doom",     ["chocolate-doom", "-iwad", "/home/pi/doom-wad/DOOM1.WAD"]),
        ("Juego2",        "juego2.py"),
    ]

    current = 0
    running = True

    while running:
        clock.tick(FPS)

        # Cerrar ventana
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Leer botón de hardware
        btn = leer_boton()  # devuelve cadenas como 'UP','DOWN','A',...
        if btn:
            b = btn.strip().upper()
            if b == 'DOWN':
                current = (current + 1) % len(games)
            elif b == 'UP':
                current = (current - 1) % len(games)
            elif b == 'A':
                label, cmd = games[current]
                # Lanza el juego (sea .py o binario de sistema)
                subprocess.Popen(cmd)
                running = False

        # Dibujar opciones
        screen.fill((0,0,0))
        for idx, (label, _) in enumerate(games):
            color = (255,255,0) if idx == current else (255,255,255)
            txt = font.render(label, True, color)
            screen.blit(txt, (50, 50 + idx*40))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
