# config.py

# Definición de colores ANSI para la salida en la terminal
COLORS = {
    "verde": "\033[92m",
    "rojo": "\033[91m",
    "azul": "\033[94m",
    "amarillo": "\033[93m",
    "fin": "\033[0m"
}

# Puertos OT comunes y sus protocolos correspondientes
COMMON_OT_PORTS = [
    21, 22, 23, 25, 69, 80, 102, 110, 137, 139, 443, 502, 789, 955, 9600,
    1883, 1911, 1962, 2222, 2404, 2455, 47808, 4840, 5006, 5007, 8883,
    161, 162, 20000, 20547, 34962, 44818
]

# Nombres de protocolos para puertos comunes
PROTOCOLOS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 69: "TFTP", 80: "HTTP", 102: "S7comm", 110: "POP3",
    137: "NetBIOS", 139: "SMB", 161: "SNMP", 162: "SNMP Trap", 443: "HTTPS", 502: "ModBus", 789: "Red Lion",
    955: "OMRON", 9600: "OMRON FINS", 1883: "MQTT", 1911: "Niagara Fox", 1962: "PCWorx", 20547: "Profinet",
    2222: "EtherNet/IP", 2404: "IEC 60870-5-104", 2455: "CODESYS", 34962: "EtherCAT", 44818: "Ethernet/IP",
    47808: "BACnet", 4840: "OPC UA", 5006: "Profibus", 5007: "Profibus", 8883: "Secure MQTT", 20000: "DNP3"
}

# Definición de los valores de TTL para cada sistema operativo
OT_OS_VALORES_TTL = {
    "Linux": {"TTL": [64, 255]},
    "macOS": {"TTL": [60, 64]},
    "Stratus": {"TTL": [30, 60, 64, 255]},
    "HP-UX": {"TTL": [30, 64, 255]},
    "AIX": {"TTL": [30, 60, 255]},
    "SunOS": {"TTL": [60, 255]},
    "FreeBSD": {"TTL": [64, 255]},
    "VMS/Wollongong": {"TTL": [30, 128]},
    "VMS/UCX": {"TTL": [128]},
    "Windows": {"TTL": [32, 128]},
    "NetBSD": {"TTL": [255]},
    "OpenBSD": {"TTL": [255]},
    "OpenVMS": {"TTL": [255]},
    "Cisco": {"TTL": [254]},
    "Compa": {"TTL": [64]},
    "Foundry": {"TTL": [64]},
    "HP MPE/iX": {"TTL": [200]},
    "Irix": {"TTL": [60, 255]},
    "Juniper": {"TTL": [64]},
    "DEC Pathworks": {"TTL": [30]},
    "Netgear": {"TTL": [64]},
    "OS/2": {"TTL": [64]},
    "OSF/1": {"TTL": [30, 60]},
    "Solaris": {"TTL": [255]},
    "DEC Ultrix": {"TTL": [30, 60, 255]},
    "VMS/Multinet": {"TTL": [64]},
    "VMS/TCPware": {"TTL": [60, 64]},
}
