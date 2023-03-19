import asyncio

from asyncua import ua
from OPCUAServerManager import PredefinedAttributes as pa
from OPCUAServerManager import OPCUAServerManager
from aquarium import *

server_manager = OPCUAServerManager()
DOUBLE = ua.VariantType.Double
BOOLEAN = ua.VariantType.Boolean
INT64 = ua.VariantType.Int64


async def main():
    global server_manager
    if server_manager is None:
        server_manager = OPCUAServerManager()
    await server_manager.create_server("opc.tcp://0.0.0.0:1234/", "AQUARIUM")
    aqua = await server_manager.add_node("AQUARIUM #1")
    # Control flags
    inner_temperature = await server_manager.add_variable_to_object(aqua, "Inner temperature", 40, INT64,
                                                                    pa.read_attributes + pa.history_attributes)
    CurrentTemp = await server_manager.add_variable_to_object(aqua, "Current temperature", 40, INT64,
                                                                    pa.read_attributes + pa.history_attributes)

    await server_manager.server.start()

    asyncio.get_event_loop().create_task(temperature(CurrentTemp))
    #asyncio.get_event_loop().create_task(water_level(CurrentLevel))
    #asyncio.get_event_loop().create_task(pollution(CurrentPollution))

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)
    loop.run_until_complete(main())
    server_manager.server.stop()
