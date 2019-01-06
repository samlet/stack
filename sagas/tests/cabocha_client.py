#!/usr/bin/env python
from client_wrapper import ServiceClient
import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service

from rasa_nlu.tokenizers import Tokenizer, Token

def tokenize_msg(text, msg_chunks):         
    words=[]
    for chunk in msg_chunks.chunks:        
        for token in chunk.tokens:
            # print(token, token.pos)
            words.append(token.surface)

    running_offset = 0
    tokens = []
    for word in words:
        word_offset = text.index(word, running_offset)
        word_len = len(word)
        running_offset = word_offset + word_len
        tokens.append(Token(word, word_offset))   
    return tokens
    
def run():
    serv = ServiceClient(nlp_service, 'CabochaNlpProcsStub', 'localhost', 50051)
    # Insert example metadata
    metadata = [('ip', '127.0.0.1')]
    response = serv.Tokenizer(
        nlp_messages.NlText(text="お皿を二枚ください。"),
        metadata=metadata
    )
    if response:
        print("response:")
        tokens=tokenize_msg("お皿を二枚ください。", response)
        for t in tokens:
            print(t.text, t.offset)

if __name__ == '__main__':
    run()   
