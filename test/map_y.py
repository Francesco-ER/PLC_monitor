# map_y.py
# Script para descubrir en qué dirección Modbus están las salidas Y
# Activa Y0, Y1, Y2... desde HMI y observa qué coil cambia aquí.

from pymodbus.client import ModbusTcpClient
import time

PLC_IP   = "192.168.1.10"  # IP del PLC
PLC_PORT = 502             # Puerto Modbus TCP
UNIT_ID  = 1
N_COILS  = 256             # Rango de coils a explorar (ajusta si necesitas más)

def main():
    c = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    if not c.connect():
        print("❌ No conecta al PLC")
        return

    print(f"Conectado a {PLC_IP}:{PLC_PORT}, escaneando {N_COILS} coils...")
    last = [None]*N_COILS

    try:
        while True:
            r = c.read_coils(0, N_COILS, unit=UNIT_ID)
            if r.isError():
                print("Error leyendo coils")
                time.sleep(1)
                continue

            bits = r.bits[:N_COILS]

            # Detecta cambios respecto a la lectura anterior
            for i, val in enumerate(bits):
                if last[i] is None:
                    last[i] = val
                elif last[i] != val:
                    estado = "ON " if val else "OFF"
                    print(f"Coil {i:03d} cambió → {estado}")
                    last[i] = val

            time.sleep(0.5)  # ajusta velocidad de refresco
    finally:
        c.close()

if __name__ == "__main__":
    main()
