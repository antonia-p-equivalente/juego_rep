pip3 install clock
import pygame
from pygame import mixer
import os, random, csv
import button
from leerBoton import leer_boton  # <-- nuevo

# ... (toda la configuración e inicialización previa queda igual)

run = True
while run:
    clock.tick(FPS)

    # 1) Leer botón de hardware (bloquea hasta soltar, luego devuelve None)
    button_press = leerBoton.leer_boton()

    # 2) Reset flags de control en cada frame
    moving_left = moving_right = shoot = grenade = False

    if not start_game:
        # Navegación de menú
        if button_press == 'DOWN':
            selected_button_index = (selected_button_index + 1) % len(menu_buttons)
        elif button_press == 'UP':
            selected_button_index = (selected_button_index - 1) % len(menu_buttons)

        # Actualizar foco
        for i, btn in enumerate(menu_buttons):
            btn.selected = (i == selected_button_index)

        # Confirmar selección con 'A'
        if menu_buttons[selected_button_index].handle_press(button_press):
            if menu_buttons[selected_button_index] == start_button:
                start_game = True
                start_intro = True
            else:  # exit_button
                run = False

        # Dibujar menú
        screen.fill(BG)
        for btn in menu_buttons:
            btn.draw(screen)

    else:
        # === Lógica de juego (dibujar fondo, world, sprites, etc.) ===
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        # ... resto del renderizado del juego ...

        # === Mapeo de botones a acciones IN-GAME ===
        if button_press == 'LEFT':
            moving_left = True
        elif button_press == 'RIGHT':
            moving_right = True
        elif button_press == 'B':
            shoot = True
        elif button_press == 'A':
            grenade = True
        elif button_press == 'MENU':
            run = False

        # Usar estos flags en el update del player:
        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and not grenade_thrown and player.grenades > 0:
                # lanzar granada...
                grenade_thrown = True
            # animaciones y movimiento:
            if player.in_air:
                player.update_action(2)  # jump
            elif moving_left or moving_right:
                player.update_action(1)  # run
            else:
                player.update_action(0)  # idle

            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # ... resto de lógica de cambio de nivel, muerte, reinicio, etc. ...

    pygame.display.update()

# Al salir, limpiar GPIO y cerrar pygame
leerBoton.cleanup()
pygame.quit()
