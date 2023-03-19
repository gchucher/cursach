from OPCUAServerManager import OPCUAServerManager
from OPCUAServerManager import PredefinedAttributes as pa
import asyncio
from asyncua import ua
from aquarium import temperature, water_level, pollution

server_manager = OPCUAServerManager()
DOUBLE = ua.VariantType.Double
BOOLEAN = ua.VariantType.Double
INT64 = ua.VariantType.Int64


async def main():
    global server_manager
    if server_manager is None:
        server_manager = OPCUAServerManager()
    await server_manager.create_server("opc.tcp://0.0.0.0:1234/", "SRV NAME")
    node = await server_manager.add_node("ROOM #1")
    # Control flags

    await server_manager.server.start()
    await server_manager.activate_historizing_for_variables(
        [temperature, water_level, pollution])
    asyncio.get_event_loop().create_task(temperature())
    asyncio.get_event_loop().create_task(water_level())
    asyncio.get_event_loop().create_task(pollution())
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)
    loop.run_until_complete(main())
    server_manager.server.stop()
