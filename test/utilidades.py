# utilidades.py
from config import COLORS
import re

def print_status(message, status_type="info"):
    """Imprime mensajes de estado con colores específicos."""
    colors = {
        "info": COLORS["azul"],
        "success": COLORS["verde"],
        "error": COLORS["rojo"],
        "warning": COLORS["amarillo"]
    }
    print(f"{colors.get(status_type, COLORS['fin'])}{message}{COLORS['fin']}")

def solicitar_input(mensaje, tipo="str", validacion=None):
    """
    Solicita input al usuario y valida según el tipo y la función de validación proporcionada.
    """
    while True:
        input_usuario = input(f"{COLORS['azul']}{mensaje}{COLORS['fin']}")
        if tipo == "int":
            try:
                input_usuario = int(input_usuario)
            except ValueError:
                print_status("Por favor, introduce un número válido.", "error")
                continue

        if validacion and not validacion(input_usuario):
            print_status("La entrada no cumple con los requisitos de validación.", "error")
            continue

        return input_usuario
