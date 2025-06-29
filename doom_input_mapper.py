#!/usr/bin/env python3
import time
import uinput
from leerBoton import leer_boton

# 1) Defino el dispositivo virtual con las teclas que Doom usa
events = [
    uinput.KEY_UP,
    uinput.KEY_DOWN,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_SPACE,
    uinput.KEY_ESC,
]
dev = uinput.Device(events)

# 2) Mapeo nombres de leer_boton() → evento uinput
MAP = {
    'UP':    uinput.KEY_UP,
    'DOWN':  uinput.KEY_DOWN,
    'LEFT':  uinput.KEY_LEFT,
    'RIGHT': uinput.KEY_RIGHT,
    'B':     uinput.KEY_LEFTCTRL,
    'A':     uinput.KEY_SPACE,
    'MENU':  uinput.KEY_ESC,
}

print("Mapper arrancado. Lee botones y envía keys…")

try:
    while True:
        btn = leer_boton()      # bloquea hasta soltar, luego None
        if btn:
            key = MAP.get(btn.strip().upper())
            if key:
                dev.emit_click(key)
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
