# modbus_fake_server.py
import asyncio
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.server import StartAsyncTcpServer

# Memorias simuladas
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0,1,0,1,0,0,1,0] + [0]*92),   # 8 coils
    hr=ModbusSequentialDataBlock(0, [10,20,30,40,50,60,70,80,90,100] + [0]*90),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)

context = ModbusServerContext(slaves=store, single=True)

async def run():
    print("🚀 Simulador Modbus TCP corriendo en 127.0.0.1:1502 ...")
    await StartAsyncTcpServer(context, address=("127.0.0.1", 1502))

if __name__ == "__main__":
    asyncio.run(run())
