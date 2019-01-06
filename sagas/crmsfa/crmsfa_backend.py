"""The Python implementation of the GRPC crmsfa.CrmsfaProcs server."""

from concurrent import futures
import time

import grpc

import common_types_pb2 as common
import crmsfa_pb2
import crmsfa_pb2_grpc

import users_pb2_grpc
from sagas.users.users_backend import UsersService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CrmsfaProcs(crmsfa_pb2_grpc.CrmsfaProcsServicer):

    def Ping(self, request, context):
        return common.PingReply(message='Ping, %s!' % request.name)


def serve(addr):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crmsfa_pb2_grpc.add_CrmsfaProcsServicer_to_server(CrmsfaProcs(), server)
    users_pb2_grpc.add_UsersServicer_to_server(UsersService(), server)

    server.add_insecure_port(addr)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    addr='[::]:50051'
    print("serve on", addr)
    serve(addr)
