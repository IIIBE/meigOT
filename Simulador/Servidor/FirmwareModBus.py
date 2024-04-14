from pyModbusTCP.server import ModbusServer, DataBank
import time

def run_server():
    server = ModbusServer(host="0.0.0.0", port=502, no_block=True)
    server.start()
    print("Servidor Modbus TCP iniciado en 0.0.0.0:502")

    # Crea una instancia de DataBank
    db = server.data_bank

    try:
        while True:
            # Establece el valor del firmware a 122 (que representa 1.22) usando métodos de instancia
            db.set_holding_registers(0, [3])  # El índice 0 corresponde al registro 1

            # Imprime el valor actual en el registro 0 para confirmar usando métodos de instancia
            current_value = db.get_holding_registers(0, 1)
            print(f"Estableciendo firmware a {current_value} en el registro 0")

            time.sleep(10)  # Actualiza el registro cada 10 segundos
    except KeyboardInterrupt:
        print("Servidor detenido.")
        server.stop()

if __name__ == "__main__":
    run_server()
