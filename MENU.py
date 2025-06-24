# menu.py
import pygame
import subprocess
import os
from leerBoton import leer_boton


def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Menú de Juegos")
    font = pygame.font.Font(None, 50)

    # Lista de juegos: (etiqueta, ruta_relativa_al_script)
    games = [
        ("Anathema", os.path.join("anathema", "anathema_adaptado_botones.py", "setup.py")),
        ("juego2", "juego2.py"),
        ("Shooter", os.path.join("Shooter", "button.py", "JUEGO DISEÑO.py"))
    ]
    current = 0

    def draw_menu():
        screen.fill((0, 0, 0))
        for idx, (name, _) in enumerate(games):
            color = (255, 255, 0) if idx == current else (150, 150, 150)
            text_surf = font.render(name, True, color)
            x = 100 + idx * 240
            y = 160
            screen.blit(text_surf, (x, y))
        pygame.display.flip()

    while True:
        # Bucle del menú
        in_menu = True
        while in_menu:
            draw_menu()
            evt = leer_boton()
            if evt == "LEFT":
                current = (current - 1) % len(games)
            elif evt == "RIGHT":
                current = (current + 1) % len(games)
            elif evt == "A":
                in_menu = False
            pygame.time.wait(100)

        # Preparar ruta y carpeta de trabajo
        game_relpath = games[current][1]
        game_folder = os.path.dirname(game_relpath) or "."
        game_script = os.path.basename(game_relpath)

        full_script_path = os.path.join(game_folder, game_script)
        if not os.path.exists(full_script_path):
            print(f"No se encontró el archivo del juego: {full_script_path}")
            continue

        # Lanzar el juego con el directorio de trabajo adecuado
        proc = subprocess.Popen(["python3", game_script], cwd=game_folder)

        # Bucle de ejecución del juego
        running = True
        while running:
            evt = leer_boton()
            retcode = proc.poll()
            if evt == "MENU":
                proc.terminate()
                proc.wait()
                running = False
            elif retcode is not None:
                running = False
            pygame.time.wait(100)

if __name__ == "__main__":
    main()

