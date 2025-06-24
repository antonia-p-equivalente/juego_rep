import time
import leerBoton

try:
    print("== Test de botones ==\nPresiona UP, DOWN, A, B o MENU")
    while True:
        btn = leerBoton.leer_boton()
        if btn:
            print("Botón detectado:", btn)
        time.sleep(0.05)
except KeyboardInterrupt:
    pass
finally:
    leerBoton.cleanup()
    print("GPIO limpio, saliendo.")
