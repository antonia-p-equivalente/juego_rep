#!/usr/bin/env python3
import pygame
from pygame import mixer
import os
import random
import csv
import button                         # importas tu clase Button :contentReference[oaicite:0]{index=0}
from leerBoton import leer_boton     # función para leer los botones

# ——— Configuración general ———
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
BG_COLOR      = (0, 0, 0)
FPS           = 60

def load_background():
    """Carga y devuelve la superficie de fondo."""
    # Ejemplo: fondo negro simple
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surf.fill((30, 30, 30))
    return surf

def setup_world():
    """Inicializa y devuelve tu mundo (tiles, plataformas, etc.)."""
    class DummyWorld:
        def draw(self):
            pass
    return DummyWorld()

def setup_player():
    """Inicializa y devuelve tu objeto jugador."""
    class DummyPlayer:
        def __init__(self):
            self.health   = 100
            self.grenades = 3
            self.in_air   = False
            self.alive    = True

        def move(self, left, right):
            return 0, False

        def shoot(self):
            pass

        def update_action(self, action_id):
            pass

    return DummyPlayer()

def setup_health_bar():
    """Inicializa y devuelve tu barra de vida."""
    class DummyHB:
        def draw(self, h):
            pass
    return DummyHB()

def setup_menu_buttons():
    """
    Crea y devuelve:
      - lista de botones [start_button, exit_button, ...]
      - start_button, exit_button (para comparar)
    Ajusta posiciones, imágenes y escala según tu diseño.
    """
    # Ejemplo genérico: botones blancos
    surf = pygame.Surface((200, 50))
    surf.fill((200,200,200))
    start_button = button.Button(300, 200, surf, 1)
    exit_button  = button.Button(300, 300, surf, 1)
    return [start_button, exit_button], start_button, exit_button

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()    # ← define el reloj antes de usarlo

    # ——— Carga de recursos y objetos ———
    bg            = load_background()
    world         = setup_world()
    player        = setup_player()
    health_bar    = setup_health_bar()
    menu_buttons, start_button, exit_button = setup_menu_buttons()
    selected_button_index = 0

    start_game  = False
    start_intro = False
    run         = True

    while run:
        # 1) Control de FPS
        clock.tick(FPS)

        # 2) Cierre de ventana
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        # 3) Leer pulsaciones de hardware
        btn = leer_boton()  # bloquea hasta soltar, luego devuelve None
        if btn:
            b = btn.strip().upper()

            # — Navegación de menú —
            if not start_game:
                if b == 'DOWN':
                    selected_button_index = (selected_button_index + 1) % len(menu_buttons)
                elif b == 'UP':
                    selected_button_index = (selected_button_index - 1) % len(menu_buttons)

                # Resaltar el botón seleccionado
                for i, mb in enumerate(menu_buttons):
                    mb.selected = (i == selected_button_index)

                # Confirmar con A
                if b == 'A' and menu_buttons[selected_button_index].handle_press('A'):
                    if menu_buttons[selected_button_index] is start_button:
                        start_game  = True
                        start_intro = True
                    else:
                        run = False

                # Dibujar menú
                screen.fill(BG_COLOR)
                for mb in menu_buttons:
                    mb.draw(screen)

            # — Dentro del juego —
            else:
                moving_left  = False
                moving_right = False
                shoot        = False
                grenade      = False

                if b == 'LEFT':
                    moving_left = True
                elif b == 'RIGHT':
                    moving_right = True
                elif b == 'B':
                    shoot = True
                elif b == 'A':
                    grenade = True
                elif b == 'MENU':
                    run = False

                # Render básico del juego
                screen.blit(bg, (0,0))
                world.draw()
                health_bar.draw(player.health)

                # Lógica de acciones del jugador
                if player.alive:
                    if shoot:
                        player.shoot()
                    elif grenade and player.grenades > 0:
                        player.grenades -= 1
                        # aquí tu lógica de lanzar granada

                    if player.in_air:
                        player.update_action(2)  # salto
                    elif moving_left or moving_right:
                        player.update_action(1)  # correr
                    else:
                        player.update_action(0)  # idle

                    scroll, level_complete = player.move(moving_left, moving_right)
                    # aquí tu lógica de scroll de pantalla, cambio de nivel, etc.

        # 4) Actualizar pantalla
        pygame.display.update()

    # 5) Limpieza de GPIO y salida limpia
    leer_boton.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

