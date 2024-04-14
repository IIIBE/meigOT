import os
import sys
import signal
from datetime import datetime
from scapy.all import sniff, IP, TCP
from utilidades import print_status, solicitar_input
from config import COLORS, PROTOCOLOS

def crear_directorio_traffic():
    dir_traffic = "traffic"
    if not os.path.exists(dir_traffic):
        os.makedirs(dir_traffic)
    return dir_traffic

def generar_nombre_archivo(dir_traffic, ip_objetivo):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archivo_nombre = f"{dir_traffic}/trafico_scada_{ip_objetivo}_{timestamp}.txt"
    return archivo_nombre

def manejar_output(mensaje, es_correcto=True, protocolo="", archivo_nombre=""):
    prefijo = COLORS["verde"] + "[+]" if es_correcto else COLORS["rojo"] + "[!]"
    mensaje_con_protocolo = mensaje.replace(protocolo, COLORS["verde"] + protocolo + COLORS['fin'])
    mensaje_completo = f"{prefijo} {mensaje_con_protocolo}{COLORS['fin']}"
    print(mensaje_completo)
    with open(archivo_nombre, "a") as archivo:
        archivo.write(mensaje + "\n")

def identificar_protocolo(packet, ip_objetivo, archivo_nombre):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        if packet[IP].src == ip_objetivo or packet[IP].dst == ip_objetivo:
            puerto_destino = packet[TCP].dport
            protocolo = PROTOCOLOS.get(puerto_destino, "Protocolo Desconocido")
            manejar_output(f"IP Origen: {packet[IP].src}, IP Destino: {packet[IP].dst}, Protocolo: {protocolo}, Puerto: {puerto_destino}",
                           es_correcto=(protocolo != "Protocolo Desconocido"), protocolo=protocolo, archivo_nombre=archivo_nombre)

def signal_handler(sig, frame):
    print_status(f"[+] Monitoreo interrumpido por el usuario. Los datos capturados se han guardado en {archivo_nombre}", "info")
    sys.exit(0)

def monitoreo_pasivo(ip_objetivo):
    global archivo_nombre
    dir_traffic = crear_directorio_traffic()
    archivo_nombre = generar_nombre_archivo(dir_traffic, ip_objetivo)
    print_status(f"[+] Iniciando el monitoreo pasivo del tráfico SCADA hacia/desde {ip_objetivo}...", "success")
    signal.signal(signal.SIGINT, signal_handler)
    sniff(prn=lambda packet: identificar_protocolo(packet, ip_objetivo, archivo_nombre), store=False, filter=f"ip host {ip_objetivo}")

if __name__ == "__main__":
    ip_objetivo = solicitar_input("Ingrese la dirección IP a monitorear: ", tipo="str",
                                  validacion=lambda x: re.match(r'^\d{1,3}(\.\d{1,3}){3}$', x))
    monitoreo_pasivo(ip_objetivo)
