from __future__ import print_function
import logging

import grpc

import mess_pb2
import mess_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mess_pb2_grpc.MessServiceStub(channel)
        response = stub.SayHello(mess_pb2.MessString(body="J'aimerais être marié."))
    print("Greeter client received:", response.lang)
    print(response)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = mess_pb2_grpc.MessServiceStub(channel)
        response = stub.SayHello(mess_pb2.MessString(body="私はアメリカ人です"))
    print("Greeter client received:", response.lang)
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    run()
