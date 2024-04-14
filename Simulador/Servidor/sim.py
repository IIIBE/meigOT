
import socket
from threading import Thread
import random
import time

# Diccionario de respuestas simuladas para cada protocolo
RESPUESTAS_PROTOCOLOS = {
    502: b'\x00\x01\x00\x00\x00\x06\x01\x03\x02\x00\x01',  # Modbus TCP
    20000: b'DNP3 Response',  # DNP3
    4840: b'OPC UA Response',  # OPC UA
    47808: b'BACnet/IP Response',  # BACnet/IP
    102: b'S7comm Response',  # S7comm (Siemens)
    1883: b'MQTT Response',  # MQTT
    8883: b'MQTT TLS Response',  # MQTT over TLS
    2404: b'IEC 60870-5-104 Response',  # IEC 60870-5-104
    161: b'SNMP Response',  # SNMP
    162: b'SNMP Trap Response',  # SNMP trap
    21: b'FTP Response',  # FTP
    22: b'SSH Response',  # SSH
    23: b'Telnet Response',  # Telnet
    80: b'HTTP Response',  # HTTP
    443: b'HTTPS Response',  # HTTPS
    44818: b'EtherNet/IP Response',  # EtherNet/IP
    34962: b'EtherCAT Response',  # EtherCAT
    # Continúa agregando más protocolos y respuestas según sea necesario
}

def simular_firmware_modbus():
    """ Simula la respuesta de firmware para Modbus """
    # Simulación más compleja puede ir aquí
    firmware_version = random.randint(1, 100)
    return f"Firmware Modbus v{firmware_version}".encode()

def simular_firmware_s7():
    """ Simula la respuesta de firmware para S7 """
    firmware_version = f"1.{random.randint(0, 9)}"
    return f"Firmware S7 v{firmware_version}".encode()

def manejar_cliente(conn, puerto):
    if puerto == 502:
        respuesta = simular_firmware_modbus()
    elif puerto == 102:
        respuesta = simular_firmware_s7()
    else:
        respuesta = RESPUESTAS_PROTOCOLOS.get(puerto, b'Protocolo no soportado')
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(respuesta)  # Enviar la respuesta simulada correspondiente al protocolo
    finally:
        conn.close()

def servidor_por_puerto(host, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, puerto))
        s.listen()
        print(f"Servidor escuchando en {host}:{puerto}...")
        while True:
            conn, addr = s.accept()
            Thread(target=manejar_cliente, args=(conn, puerto)).start()

