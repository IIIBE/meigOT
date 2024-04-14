
# MeigOT “Mapping and Enumeration Tool for Industrial Governance in Operational Technology’’​
​

La herramienta MeigOT está diseñada para proporcionar capacidades de análisis y monitoreo en redes de tecnología operativa (OT). Facilita la identificación de dispositivos y protocolos, ofreciendo una valiosa perspectiva de la infraestructura de red.

## Características

- Reconocimiento pasivo y activo de redes.
- Chequeo y evaluación de DNSSEC.
- Monitoreo del tráfico de red con capacidad de reconocimiento de protocolos.
- Descubrimiento de hosts con resolución ARP.
- Análisis de firmware en dispositivos Modbus y S7comm.

## Configuración del Proyecto

Este proyecto requiere Python 3.10 y el uso de un entorno virtual para una gestión de dependencias adecuada.

### Instalación de Python 3.10

Si aún no tienes Python 3.10, descárgalo e instálalo desde [python.org](https://www.python.org/downloads/release/python-3100/).

### Creación y Activación del Entorno Virtual

Abre una terminal en el directorio del proyecto y ejecuta:

```bash
python3.10 -m venv venv
```

Esto creará un nuevo entorno virtual llamado `venv` dentro de tu proyecto. Para activarlo:

```bash
source venv/bin/activate
```

Una vez activado, tu prompt de la terminal debería cambiar para indicar que el entorno virtual está en uso.

### Instalación de Dependencias

Con el entorno virtual activado, instala todas las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

Esto garantizará que todas las bibliotecas externas necesarias estarán disponibles para tu proyecto.

## Ejecución

Con las dependencias instaladas, puedes ejecutar el programa principal con:

```bash
sudo python main.py
```

Sigue las instrucciones en pantalla para navegar a través de las distintas funciones de la herramienta.

## Desactivación del Entorno Virtual

Para salir del entorno virtual después de trabajar con la aplicación, simplemente ejecuta:

```bash
deactivate
```

Esto retornará tu terminal a su configuración normal.
