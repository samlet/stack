from client_wrapper import ServiceClient
import common_types_pb2 as common
import ${package_name}_pb2
import ${package_name}_pb2_grpc

serv = ServiceClient(${package_name}_pb2_grpc, '${service_name}Stub', 'localhost', 50051)

def run():
    response = serv.Ping(common.PingRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    run()
