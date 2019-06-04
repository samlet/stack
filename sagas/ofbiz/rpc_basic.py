from concurrent import futures
import time

import grpc

import hello_pb2_grpc
import hello_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BasicService(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        print('get %s'%request)
        return hello_pb2.ResponseHello(response="world")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(BasicService(), server)
    port='0.0.0.0:5051'
    server.add_insecure_port(port)
    server.start()
    print(".. service started on", port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

