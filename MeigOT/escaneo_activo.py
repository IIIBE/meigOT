import asyncio
from scapy.all import ICMP, IP, TCP, sr1, UDP
from utilidades import print_status, solicitar_input
from config import COMMON_OT_PORTS, PROTOCOLOS
import snap7
from snap7.client import Client
from pymodbus.client import ModbusTcpClient as ModbusClient

# Función para detectar el sistema operativo basado en TTL
def detectar_sistema_operativo(host):
    try:
        packet = IP(dst=host) / ICMP()
        resp = sr1(packet, timeout=1, verbose=0)
        if resp:
            ttl = resp[IP].ttl
            if ttl <= 64:
                return "Linux/Unix"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Posiblemente otro sistema operativo"
    except Exception as e:
        print(f"No se pudo determinar el sistema operativo: {str(e)}")
    return "Desconocido"

# Funciones para leer el firmware

def leer_firmware_modbus(ip, port):
    client = ModbusClient(ip, port=port)
    try:
        client.connect()
        response = client.read_holding_registers(0, 1)
        if response.isError():
            print("Error al leer el registro de firmware de Modbus")
            return False
        else:
            firmware = response.registers[0]
            print(f"Firmware version (Modbus): {firmware}")
            return True
    except Exception as e:
        print(f"No se pudo conectar o leer del dispositivo Modbus en {ip}:{port}, error: {str(e)}")
        return False
    finally:
        client.close()



def leer_firmware_s7(ip):
    client = snap7.client.Client()
    try:
        client.connect(ip, 0, 1, 102)
        szl_id = 0x001C  # Asegúrate de que este ID coincide con lo que el servidor está configurado para manejar
        szl_index = 0x0000  # Este índice también debe coincidir
        szl_data = client.read_szl(szl_id, szl_index)
        # Suponiendo que los datos del firmware están en los primeros dos bytes
        firmware_version_major = szl_data.data[0]
        firmware_version_minor = szl_data.data[1]
        firmware = f"{firmware_version_major}.{firmware_version_minor}"
        print(f"Firmware version (S7): {firmware}")
        return True
    except Exception as e:
        print(f"No se pudo conectar o leer del PLC S7 en {ip}, error: {str(e)}")
        return False
    finally:
        client.disconnect()



async def ask_and_scan_plc(host, port, protocol_name):
    if protocol_name in ["ModBus", "S7comm"]:
        respuesta = solicitar_input(f"Hemos detectado {protocol_name} en puerto {port} abierto, ¿deseas ver la versión del firmware? (s/n): ", tipo="str")
        if respuesta.lower() == 's':
            success = False
            if protocol_name == "ModBus":
                success = leer_firmware_modbus(host, port)
            elif protocol_name == "S7comm":
                success = leer_firmware_s7(host)
            if not success:
                print("No se pudo obtener la versión de firmware para el dispositivo en el puerto especificado.")

async def port_scan(host, ports, scan_type):
    detected_protocols = {}
    for port in ports:
        packet = None
        if scan_type == "TCP":
            packet = IP(dst=host) / TCP(dport=port, flags="S")
        elif scan_type == "UDP":
            packet = IP(dst=host) / UDP(dport=port)
        elif scan_type == "ACK":
            packet = IP(dst=host) / TCP(dport=port, flags="A")
        
        resp = await asyncio.get_event_loop().run_in_executor(None, lambda: sr1(packet, timeout=1, verbose=False))
        if resp and ((scan_type == "TCP" and resp.haslayer(TCP) and (resp.getlayer(TCP).flags & 0x12)) or
                     (scan_type == "UDP") or
                     (scan_type == "ACK" and resp.haslayer(TCP) and (resp.getlayer(TCP).flags & 0x4))):
            protocol_name = PROTOCOLOS.get(port, "Desconocido")
            print_status(f"{host}: Puerto {scan_type} {port} abierto ({protocol_name}).", "success")
            detected_protocols[port] = protocol_name
            await ask_and_scan_plc(host, port, protocol_name)

    return detected_protocols

# Implementación del flujo principal de escaneo activo
async def realizar_escaneo_activo():
    host_input = solicitar_input("Ingrese la dirección IP a escanear (ej. 192.168.1.1): ", tipo="str")
    os_detectado = detectar_sistema_operativo(host_input)
    print(f"Sistema operativo detectado: {os_detectado}")
    print("Tipo de escaneo:")
    print("1. TCP")
    print("2. UDP")
    print("3. ACK")
    
    tipo_escaneo = solicitar_input("Seleccione el tipo de escaneo: ", tipo="int")
    scan_type = "TCP" if tipo_escaneo == 1 else "UDP" if tipo_escaneo == 2 else "ACK" if tipo_escaneo == 3 else "TCP"
    detected_protocols = await port_scan(host_input, COMMON_OT_PORTS, scan_type)

# Ejecutar el escaneo activo
if __name__ == "__main__":
    asyncio.run(realizar_escaneo_activo())
