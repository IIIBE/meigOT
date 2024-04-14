# Simulador de Protocolos

Simulación de servidor y cliente que manejan diversos protocolos de comunicaciones industriales.

## Estructura del Proyecto

- `Cliente`: Contiene el código del cliente que realiza solicitudes a los servidores de protocolo.
- `Servidor`: Contiene el código del servidor que simula respuestas para varios protocolos.

## Requisitos Previos

- Python 3.10
- Ubuntu VM para servidor
- Ubuntu VM para cliente

## Configuración del Entorno de Desarrollo

### Primeros Pasos

1. Abre una terminal en tu máquina Ubuntu Server VM.
2. Clona el repositorio del proyecto:
`git clone https://github.com/IIIBE/meigOT`
3. Navega al directorio del servidor:
`cd meigOT/Simulador/Servidor`

### Creación del Entorno Virtual

Un entorno virtual en Python es un entorno aislado que permite instalar paquetes y ejecutar software sin afectar el resto de tu sistema. Aquí te mostramos cómo configurarlo:

4. Crea un entorno virtual para Python 3.10:
  `python3.10 -m venv venv`
5. Activa el entorno virtual:
  `source venv/bin/activate`

Una vez activado, tu prompt debería cambiar para reflejar que estás ahora dentro de un entorno virtual.

6. Instala las dependencias necesarias:
 ` pip install -r requirements.txt`


### Iniciar el Servidor

7. Con el entorno virtual activo, ejecuta el servidor con:
   `sudo python sim.py` o `FirmwareModBus.py`


### Iniciar el Servidor

Una vez activado el entorno virtual, inicia el servidor ejecutando el script de Python correspondiente, por ejemplo:
`sudo python sim.py` Para el escaneo pasivo
`sudo python FirmwareModBus.py` Para el escaneo activo 


Esto iniciará el proceso del servidor en la dirección y puerto configurados.

### Configuración e Inicio del Cliente

Para configurar y ejecutar el cliente, simplemente repite los pasos 1 al 3, cambiando el directorio a `Cliente`, y luego sigue los pasos 4 al 7 para activar el entorno virtual y ejecutar el script del cliente.

- `cd meigOT/Simulador/Cliente`
- `python3.10 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `sudo python client.py`

