# leerBoton.py
# Módulo para leer botones conectados a la Raspberry Pi usando RPi.GPIO

import RPi.GPIO as GPIO
import time

# Asignación de pines BCM para cada botón
BUTTON_PINS = {
    'UP': 9,
    'DOWN': 10,
    'LEFT': 11,
    'RIGHT': 12,
    'A': 13,
    'B': 14,
    'MENU': 15
}

# Configuración inicial de GPIO
GPIO.setmode(GPIO.BCM)
for name, pin in BUTTON_PINS.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Tiempo de rebote en segundos
_DEBOUNCE_TIME = 0.02


def leer_boton():
    """
    Revisa el estado de los botones y retorna el nombre del primer botón presionado.
    Si no hay ningún botón presionado, retorna None.
    """
    for name, pin in BUTTON_PINS.items():
        # Botón conectado a GND, nivel bajo indica presión
        if GPIO.input(pin) == GPIO.LOW:
            # Debounce: esperar un corto periodo y verificar nuevamente
            time.sleep(_DEBOUNCE_TIME)
            if GPIO.input(pin) == GPIO.LOW:
                # Esperar hasta que el usuario suelte el botón
                while GPIO.input(pin) == GPIO.LOW:
                    time.sleep(0.01)
                return name
    return None


def cleanup():
    """
    Limpia la configuración de GPIO. Usar al finalizar el programa si se desea.
    """
    GPIO.cleanup()
