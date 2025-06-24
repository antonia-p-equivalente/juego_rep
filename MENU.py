import pygame
import os
import sys
import subprocess
import leerBoton   # <-- nuevo

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Menú de Juegos")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    games = [
        ("Anathema",      os.path.join("anathema", "anathema_adaptado_botones.py")),
        ("Juego2",        "juego2.py"),
        ("Shooter",       os.path.join("Shooter", "JUEGO DISEÑO.py")),
        ("MiNuevoJuego",  "mi_nuevo_juego.py")
    ]

    current = 0
    running = True

    while running:
        clock.tick(30)

        # 1) Cerrar ventana si toca
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # 2) Leer botón de hardware (bloquea hasta soltar y luego devuelve None)
        btn = leerBoton.leer_boton()
        if btn:
            b = btn.strip().upper()
            print("DEBUG → botón leído:", b)

            # 3) Navegación con botones
            if b == 'DOWN':
                current = (current + 1) % len(games)
            elif b == 'UP':
                current = (current - 1) % len(games)
            elif b == 'A':
                label, path = games[current]
                print(f"Lanzando «{label}» → {path}")
                subprocess.Popen(["python3", path])
                running = False

        # 4) Dibujar menú con selección en amarillo
        screen.fill((0, 0, 0))
        for idx, (label, _) in enumerate(games):
            color = (255, 255, 0) if idx == current else (255, 255, 255)
            txt_surf = font.render(label, True, color)
            screen.blit(txt_surf, (50, 50 + idx * 40))

        pygame.display.flip()

    # 5) Limpiar GPIO y salir
    leerBoton.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
