from concurrent import futures
import sys
import time
import grpc

from google.protobuf.json_format import MessageToJson
from cabocha.analyzer import CaboChaAnalyzer

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CabochaService(nlp_service.CabochaNlpProcsServicer):

    def Tokenizer(self, request, context):
        metadata = dict(context.invocation_metadata())
        print(metadata)

        text=request.text
        print(".. analyse ", text)

        analyzer = CaboChaAnalyzer()
        tree = analyzer.parse(text)
        msg_chunks = nlp_messages.NlCabochaChunks()
        chunks = []
        for chunk in tree:
            msg_chunk = nlp_messages.NlCabochaChunk()
            msg_chunk.id = chunk.id
            if not chunk.additional_info is None:
                msg_chunk.additional_info = chunk.additional_info
            msg_chunk.feature_list.extend(chunk.feature_list)
            msg_chunk.func_pos = chunk.func_pos
            msg_chunk.head_pos = chunk.head_pos
            msg_chunk.link = chunk.link
            msg_chunk.score = chunk.score
            msg_chunk.token_pos = chunk.token_pos
            msg_chunk.next_link_id = chunk.next_link_id
            msg_chunk.prev_link_ids.extend(chunk.prev_link_ids)

            words = []
            for token in chunk:
                # print(token, token.pos)
                word = nlp_messages.NlCabochaToken(surface=token.surface,
                                                   id=token.id,
                                                   additional_info=token.additional_info,
                                                   feature_list=token.feature_list,
                                                   ne=token.ne,
                                                   normalized_surface=token.normalized_surface,
                                                   pos=token.pos,
                                                   pos1=token.pos1,
                                                   pos2=token.pos2,
                                                   pos3=token.pos3,
                                                   ctype=token.ctype,
                                                   cform=token.cform,
                                                   genkei=token.genkei,
                                                   yomi=token.yomi
                                                   )
                words.append(word)
            msg_chunk.tokens.extend(words)
            chunks.append(msg_chunk)

        msg_chunks.chunks.extend(chunks)
        return msg_chunks

def serve(address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nlp_service.add_CabochaNlpProcsServicer_to_server(CabochaService(), server)
    server.add_insecure_port(address)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    """
    $ python -m sagas.backend.cabocha_backend
    """
    address='0.0.0.0:50051'
    print("serve on", address)
    serve(address)
