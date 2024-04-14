import asyncio
from utilidades import print_status, solicitar_input
from config import COLORS
import re
from reconocimiento import monitoreo_pasivo
from arpscan import scan_subnet
from escaneo_activo import realizar_escaneo_activo
from dnssec import chequear_dnssec, evaluar_transferencia_zona

def print_encabezado_y_pie():
    encabezado = "*" * 30 + " MeigOT " + "*" * 30
    pie = "Creado por Liibe"
    print('')
    print(COLORS['azul'] + encabezado + COLORS['fin'])
    print(COLORS['verde'] + pie.center(len(encabezado)) + COLORS['fin'])
    print(COLORS['azul'] + "*" * len(encabezado) + COLORS['fin'])

def print_menu():
    print(f"{COLORS['azul']}Menu Principal{COLORS['fin']}")
    print("1. Reconocimiento Pasivo de Red")
    print("2. Descubrimiento Host + ARP")
    print("3. Escaneo Activo de Red")
    print("4. Chequeos de DNS")
    print("5. Salir")
    print('')

async def main_async():
    try:
        while True: 
            print_encabezado_y_pie() 
            print_menu()
            opcion = solicitar_input("Seleccione una opción: ", tipo="int")

            if opcion == 1:
                ip_objetivo = solicitar_input("Ingrese la dirección IP a monitorear: ", tipo="str", validacion=lambda x: re.match(r'^\d{1,3}(\.\d{1,3}){3}$', x))
                monitoreo_pasivo(ip_objetivo)
            elif opcion == 2:
                subnet_input = solicitar_input("Introduce la IP o el rango IP (ej. 192.168.1.0/24): ", tipo="str")
                await scan_subnet(subnet_input)  # Ejecución asíncrona
            elif opcion == 3:
                await realizar_escaneo_activo()  # Ejecución asíncrona
            elif opcion == 4:
                dominio = solicitar_input("Ingrese el dominio a chequear: ", tipo="str")
                chequear_dnssec(dominio)
                evaluar_transferencia_zona(dominio)
            elif opcion == 5:
                print_status("Saliendo...", "error")
                break
            else:
                print_status("Opción no válida. Por favor, intente de nuevo.", "error")
    except KeyboardInterrupt:
        print_status("\nInterrupción detectada, cerrando el programa...", "error")

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print_status("\nInterrupción detectada, cerrando el programa desde main...", "error")

if __name__ == "__main__":
    main()
