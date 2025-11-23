from opcua import Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840")
server.start()
print("OPC-UA server running")