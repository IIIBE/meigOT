import dns.resolver
import dns.query
import dns.zone
import dns.exception
from utilidades import print_status  

def chequear_dnssec(dominio):
    """Chequea si DNSSEC está habilitado para el dominio proporcionado."""
    print_status(f"Chequeando DNSSEC para {dominio}...", "info")
    try:
        respuesta = dns.resolver.resolve(dominio, 'DNSKEY')
        if respuesta:
            print_status(f"DNSSEC encontrado para {dominio}.", "success")
        else:
            print_status(f"DNSSEC no está habilitado para {dominio}.", "warning")
    except dns.resolver.NoAnswer:
        print_status(f"No se encontraron registros DNSKEY para {dominio}.", "warning")
    except dns.resolver.NXDOMAIN:
        print_status(f"El dominio {dominio} no existe.", "error")
    except dns.exception.Timeout:
        print_status(f"Tiempo de espera agotado al consultar DNSKEY para {dominio}.", "error")
    except Exception as e:
        print_status(f"Error al chequear DNSSEC para {dominio}: {e}", "error")

def evaluar_transferencia_zona(dominio):
    """Evalúa la configuración de transferencia de zona para el dominio proporcionado."""
    print_status(f"Evaluando transferencia de zona para {dominio}...", "info")
    try:
        ns_records = dns.resolver.resolve(dominio, 'NS')
        for ns_record in ns_records:
            nameserver = str(ns_record.target)
            try:
                ns_ip = dns.resolver.resolve(nameserver, 'A')[0].to_text()
                xfr = dns.query.xfr(ns_ip, dominio)
                zone = dns.zone.from_xfr(xfr)
                if zone:
                    print_status(f"Transferencia de zona posible para {dominio} desde {nameserver}.", "warning")
            except dns.exception.DNSException as e:
                print_status(f"No se pudo realizar la transferencia de zona desde {nameserver}: {e}", "info")
    except dns.resolver.NoNameservers:
        print_status(f"No se encontraron servidores NS para {dominio}.", "error")
    except dns.exception.DNSException as e:
        print_status(f"Error al resolver NS para {dominio}: {e}", "error")
