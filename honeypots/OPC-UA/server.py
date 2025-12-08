import logging
from opcua import Server, ua

logging.basicConfig(level=logging.DEBUG)

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840")
idx = server.register_namespace("MyNamespace")

myvar = server.get_objects_node().add_variable(idx, "MyVariable", 0)

myvar.set_writable(writable=True)

server.start()
print("OPC-UA server running...")
