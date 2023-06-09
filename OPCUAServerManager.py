from asyncua import ua, Server
from asyncua.server.history_sql import HistorySQLite
import logging
from datetime import timedelta


class PredefinedAttributes:
    read_attributes = [
        (ua.AttributeIds.AccessLevel, ua.AccessLevel.CurrentRead),
        (ua.AttributeIds.UserAccessLevel, ua.AccessLevel.CurrentRead)
    ]
    write_attributes = [
        (ua.AttributeIds.AccessLevel, ua.AccessLevel.CurrentWrite),
        (ua.AttributeIds.UserAccessLevel, ua.AccessLevel.CurrentWrite)
    ]
    history_attributes = [
        (ua.AttributeIds.AccessLevel, ua.AccessLevel.HistoryRead),
        (ua.AttributeIds.UserAccessLevel, ua.AccessLevel.HistoryRead)
    ]


class OPCUAServerManager:
    def __init__(self):
        self.nodes = dict()
        self.folders = dict()
        self.methods = dict()
        self.server = Server(iserver=None)

    async def create_server(self, endpoint, server_name):
        logging.basicConfig(level=logging.CRITICAL)
        self.server.iserver.history_manager.set_storage(HistorySQLite("Greenhouse_hist.sql"))
        await self.server.init()
        await self.server.nodes.server.delete()  # Delete autogenerated Server Node
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(server_name)
        self.namespace_id = await self.server.register_namespace(
            'http://{0}'.format(str(server_name).replace(' ', '_')))
        self.server.default_timeout = 3600000

    async def add_node(self, node_name):
        self.nodes[node_name] = await self.server.get_objects_node().add_object(self.namespace_id, node_name)
        await self.nodes[node_name].set_attr_bit(ua.AttributeIds.EventNotifier, ua.EventNotifier.SubscribeToEvents)
        return self.nodes[node_name]

    async def add_variable_to_object(self, object_ref, var_name, var_value, var_type, attributes_bits=[]):
        variable = await object_ref.add_variable(self.namespace_id, var_name, ua.Variant(var_value, var_type))
        for attr, bit in attributes_bits:
            await variable.set_attr_bit(attr, bit)
        return variable

    async def activate_historizing_for_variables(self, list_of_variables):
        for variable in list_of_variables:
            await self.server.historize_node_data_change(variable, period=timedelta(minutes=1), count=100)

    async def add_folder_to_object(self, object_ref, folder_name):
        self.folders[folder_name] = await object_ref.add_folder(self.namespace_id, folder_name)
        return self.folders[folder_name]

    async def add_method_to_object(self, object_ref, method_name, method_ref, arguments, output):
        self.methods[method_name] = await object_ref.add_method(self.namespace_id, method_name, method_ref, arguments, output)
        return self.methods[method_name]