from concurrent import futures
import time

import grpc
import requests
import json

import blueprints_pb2_grpc
import blueprints_pb2
from sagas.ofbiz.blackboard import Blackboard, BlackboardReceiver

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

"""
$ start as
# or: python -m sagas.ofbiz.rpc_artifacts
"""

#$ ./query.py talk "hi"
#$ ./query.py talk "/joke"
def talk(sender, a_str):
    headers = {
        'content-type': 'application/json',
    }
    # data = '{'+'"message": "{}"'.format(a_str)+'}'
    data={'sender':sender, 'message':a_str}
    response = requests.post('http://localhost:5005/webhooks/rest/webhook',
                             headers=headers, data=json.dumps(data))
    # print(response.text)
    return response.json()

class ArtifactService(blueprints_pb2_grpc.ArtifactServiceServicer):
    def Talk(self, request, context):
        rs=talk(request.sender, request.message)
        recips = []
        for r in rs:
            recips.append(blueprints_pb2.BotRecipient(id=r['recipient_id'], text=r['text']))
        return blueprints_pb2.BotResponse(recipients=recips)

    def SetSlot(self, request, context):
        return super().SetSlot(request, context)

    def __init__(self, artifacts):
        self.artifacts=artifacts

    def Ping(self, request, context):
        print('get %s'%request)
        self.artifacts.blackboard.send(request.message)
        return blueprints_pb2.PingResponse(response="world")

class Artifacts(object):
    def __init__(self, port='0.0.0.0:20051'):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        blueprints_pb2_grpc.add_ArtifactServiceServicer_to_server(ArtifactService(self), self.server)
        self.port=port
        self.server.add_insecure_port(port)

        self.blackboard=Blackboard()
        # self.receiver=BlackboardReceiver()

    def serve(self, blocking=True):
        self.server.start()
        print(".. artifacts servant started on", self.port)

        if blocking:
            try:
                while True:
                    time.sleep(_ONE_DAY_IN_SECONDS)
            except KeyboardInterrupt:
                self.server.stop(0)
                self.blackboard.close()
        # else:
        #    self.receiver.serve('anonymous.info')


if __name__ == '__main__':
    # import asyncio
    # from sagas.tests.bus.aio.receive_logs_topic import main
    # # message receiver
    # loop = asyncio.get_event_loop()
    # loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages ..")

    # rpc and message sender
    s=Artifacts()
    s.serve()

    # loop.run_forever()


