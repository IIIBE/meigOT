import socket
import time
import random

# Lista de puertos basados en los protocolos a simular
PUERTOS_PROTOCOLOS = [502, 20000, 4840, 47808, 102, 1883, 8883, 2404, 161, 162, 21, 22, 23, 80, 443, 44818, 34962]

def cliente_protocolos(servidor_ip='11.12.13.131'):
    while True:
        port = random.choice(PUERTOS_PROTOCOLOS)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((servidor_ip, port))
                solicitud = b'Solicitud de protocolo'
                print(f"Conectando al puerto {port}")
                s.sendall(solicitud)
                respuesta = s.recv(1024)
                print(f"Respuesta desde puerto {port}: {respuesta}")
            except Exception as e:
                print(f"Error en puerto {port}: {e}")
            time.sleep(10)

if __name__ == "__main__":
    cliente_protocolos()
