#!/bin/bash
# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./general.proto

proto_root=$HOME/jcloud/assets/langs/workspace/langprocs/src/main/proto
# python -m grpc_tools.protoc -I$proto_root --python_out=./protocol --grpc_python_out=./protocol $proto_root/nlpserv.proto
# python -m grpc_tools.protoc -I$proto_root --python_out=. --grpc_python_out=. $proto_root/nlpserv.proto
python -m grpc_tools.protoc -I$proto_root --python_out=. --grpc_python_out=. $proto_root/*.proto

protoc -I=$proto_root --go_out=plugins=grpc:protocol/nlpserv $proto_root/nlp*.proto

## 
python -m grpc_tools.protoc -Iprotocol --python_out=. --grpc_python_out=. protocol/*.proto
