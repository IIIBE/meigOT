import asyncio
import ipaddress
import requests
import logging
import re
from scapy.all import Ether, ARP, srp
from config import COLORS  

# Configuración de logging para reducir la verbosidad de Scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def os_from_ttl(ttl):
    """Determina el posible sistema operativo basado en el valor TTL."""
    if ttl <= 64:
        return "Linux/Unix"
    elif ttl <= 128:
        return "Windows"
    else:
        return "Posiblemente otro sistema operativo"

async def ping_host(host):
    """Utiliza el comando ping del sistema para verificar si un host está activo y retorna el TTL."""
    proc = await asyncio.create_subprocess_shell(
        f"ping -c 1 -W 1 {host}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    stdout, _ = await proc.communicate()
    if proc.returncode == 0:
        # Busca el valor TTL en la salida de ping
        match = re.search(r'ttl=(\d+)', stdout.decode())
        ttl = int(match.group(1)) if match else None
        return (host, ttl)
    return (host, None)

async def arp_query(host):
    """Realiza una consulta ARP para obtener la dirección MAC de un host activo."""
    def perform_arp():
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host), timeout=2, verbose=0)
        return (host, ans[0][1].hwsrc) if ans else (host, None)
    
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, perform_arp)

def get_vendor(mac):
    """Obtiene el fabricante de una dirección MAC utilizando una API web."""
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.ok:
            return response.text
    except requests.RequestException:
        pass
    return "Desconocido"

async def scan_subnet(subnet):
    """Escanea una subred, descubre hosts activos, sus direcciones MAC y posible sistema operativo."""
    subnet = ipaddress.ip_network(subnet)
    hosts = [str(host) for host in subnet.hosts()]

    print(f"{COLORS['azul']}Realizando descubrimiento ICMP...{COLORS['fin']}")
    tasks = [ping_host(host) for host in hosts]
    results = await asyncio.gather(*tasks)
    active_hosts = [result for result in results if result[1]]

    if not active_hosts:
        print(f"{COLORS['rojo']}No se encontraron hosts activos.{COLORS['fin']}")
        return

    print(f"{COLORS['verde']}Hosts activos encontrados con sus posibles sistemas operativos:{COLORS['fin']}")
    for host, ttl in active_hosts:
        os_guess = os_from_ttl(ttl)
        print(f"{COLORS['verde']}{host} - {os_guess}{COLORS['fin']}")

    print(f"\n{COLORS['azul']}Realizando consultas ARP...{COLORS['fin']}")
    arp_tasks = [arp_query(host) for host, _ in active_hosts]
    arp_results = await asyncio.gather(*arp_tasks)

    print(f"\n{COLORS['amarillo']}Información de los hosts activos:{COLORS['fin']}")
    for (host, ttl), (host_arp, mac) in zip(active_hosts, arp_results):
        os_guess = os_from_ttl(ttl)
        if mac:
            vendor = get_vendor(mac)
            print(f"IP: {host}, MAC: {mac}, Fabricante: {vendor}, SO: {os_guess}")
        else:
            print(f"IP: {host}, MAC: No encontrada, SO: {os_guess}")

async def main():
    while True:
        try:
            subnet_input = input(f"{COLORS['azul']}Introduce el rango IP (ej. 192.168.1.0/24): {COLORS['fin']}")
            ipaddress.ip_network(subnet_input)  # Valida la entrada
            await scan_subnet(subnet_input)
            break  # Si la entrada es válida y el escaneo se completa, salir del bucle
        except ValueError:
            print(f"{COLORS['rojo']}Por favor, introduce bien los datos de la IP/rango. Ejemplo: 192.168.1.0/24{COLORS['fin']}")

if __name__ == "__main__":
    asyncio.run(main())
