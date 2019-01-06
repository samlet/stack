"""The Python implementation of the GRPC ${package_name}.${service_name} server."""

from concurrent import futures
import time

import grpc

import common_types_pb2 as common
import ${package_name}_pb2
import ${package_name}_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ${service_name}(${package_name}_pb2_grpc.${service_name}Servicer):

    def Ping(self, request, context):
        return common.PingReply(message='Ping, %s!' % request.name)


def serve(addr):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ${package_name}_pb2_grpc.add_${service_name}Servicer_to_server(${service_name}(), server)
    server.add_insecure_port('[::]:50051')
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

