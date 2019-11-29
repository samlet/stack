#!/bin/bash
rm lib/src/generated/*
proto_root=$HOME/jcloud/assets/langs/workspace/langprocs/src/main/proto
protoc --dart_out=grpc:lib/src/generated -I$proto_root $proto_root/*.proto

