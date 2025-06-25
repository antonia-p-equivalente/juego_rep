#!/usr/bin/env python3
import pygame
from pygame import mixer
import os
import sys
import random
import csv
import subprocess
import button                         # tu clase Button
from leerBoton import leer_boton     # función para leer los botones

# ——— Configuración general ———
SCREEN_WIDTH  = 480
SCREEN_HEIGHT = 320
BG_COLOR      = (0, 0, 0)
FPS           = 60

def load_background():
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surf.fill((30, 30, 30))
    return surf

def setup_world():
    class DummyWorld:
        def draw(self): pass
    return DummyWorld()

def setup_player():
    class DummyPlayer:
        def __init__(self):
            self.health   = 100
            self.grenades = 3
            self.in_air   = False
            self.alive    = True
        def move(self, left, right): return 0, False
        def shoot(self): pass
        def update_action(self, action_id): pass
    return DummyPlayer()

def setup_health_bar():
    class DummyHB:
        def draw(self, h): pass
    return DummyHB()

def setup_menu_buttons():
    surf = pygame.Surface((200, 50))
    surf.fill((200,200,200))
    start_button = button.Button(300, 200, surf, 1)
    exit_button  = button.Button(300, 300, surf, 1)
    return [start_button, exit_button], start_button, exit_button

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()

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
        clock.tick(FPS)

        # 1) Cierre de ventana
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        # 2) Leer pulsaciones de hardware
        btn = leer_boton()  # bloquea hasta soltar, luego devuelve None
        if btn:
            b = btn.strip().upper()

            # — Navegación de menú —
            if not start_game:
                if b == 'DOWN':
                    selected_button_index = (selected_button_index + 1) % len(menu_buttons)
                elif b == 'UP':
                    selected_button_index = (selected_button_index - 1) % len(menu_buttons)

                for i, mb in enumerate(menu_buttons):
                    mb.selected = (i == selected_button_index)

                if b == 'A' and menu_buttons[selected_button_index].handle_press('A'):
                    if menu_buttons[selected_button_index] is start_button:
                        start_game  = True
                        start_intro = True
                    else:
                        run = False

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
                    # Lanza de nuevo el menú principal y sale de este juego
                    menu_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MENU.py'))
                    subprocess.Popen(["python3", menu_script])
                    run = False

                # Render básico del juego
                screen.blit(bg, (0,0))
                world.draw()
                health_bar.draw(player.health)

                if player.alive:
                    if shoot:
                        player.shoot()
                    elif grenade and player.grenades > 0:
                        player.grenades -= 1
                        # lógica de granada

                    if player.in_air:
                        player.update_action(2)
                    elif moving_left or moving_right:
                        player.update_action(1)
                    else:
                        player.update_action(0)

                    scroll, level_complete = player.move(moving_left, moving_right)
                    # lógica de scroll / cambio de nivel...

        # 3) Actualizar pantalla
        pygame.display.update()

    # 4) Limpieza de GPIO y cierre
    leer_boton.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
