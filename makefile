## Shipping package
# PROTO_ROOT_DIR = $(shell brew --prefix)/Cellar/protobuf/3.6.0/include
# PROTO_ROOT_DIR = $(brew --prefix)/Cellar/protobuf/3.6.1.1/include
PROTO_ROOT_DIR = $(shell brew --prefix)/Cellar/protobuf/3.6.1.1/include
proto_root=${JCLOUD_HOME}/assets/langs/workspace/langprocs/src/main/proto

PROJECT_NAME = sagas-grpc

## Dart requires you to manually ship all google provided proto files too.
_gendart:
	@mkdir -p model/gen/ship/dart
	@protoc -I=model/protodefs --dart_out=grpc:model/gen/ship/dart model/protodefs/*.proto
	@protoc -I$(PROTO_ROOT_DIR) --dart_out=model/gen/ship/dart $(PROTO_ROOT_DIR)/google/protobuf/*.proto
	# protoc -I=$proto_root --go_out=plugins=grpc:protocol/nlpserv $proto_root/nlp*.proto
	@protoc -I=$(proto_root) --dart_out=grpc:model/gen/ship/dart $(proto_root)/common*.proto
	@protoc -I=$(proto_root) --dart_out=grpc:model/gen/ship/dart $(proto_root)/nlp*.proto

	## copy files
	@echo ${JCLOUD_HOME}
	# @rm -rf ${JCLOUD_HOME}/assets/langs/workspace/flutter/catalog/lib/model
	# @cp -r model/gen/ship/dart ${JCLOUD_HOME}/assets/langs/workspace/flutter/catalog/lib/model
	@rm -rf ${JCLOUD_HOME}/assets/langs/workspace/flutter/sagas_meta/lib/src/meta
	@cp -r model/gen/ship/dart ${JCLOUD_HOME}/assets/langs/workspace/flutter/sagas_meta/lib/src/meta

_gengo:
	@mkdir -p model/gen
	@protoc -I=model/protodefs --go_out=plugins=grpc:model/gen model/protodefs/*.proto

_genpy:
	@python -m grpc_tools.protoc -I$(PROTO_ROOT_DIR) -Imodel/protodefs --python_out=. --grpc_python_out=. model/protodefs/*.proto
	@python -m grpc_tools.protoc -I$(PROTO_ROOT_DIR) --python_out=. --grpc_python_out=. $(PROTO_ROOT_DIR)/google/protobuf/*.proto

_genjava:
	@rm -rf ./model/gen/ship/java
	@mkdir -p model/gen/ship/java
	protoc -I$(PROTO_ROOT_DIR) -Imodel/protodefs --java_out=model/gen/ship/java model/protodefs/*.proto
	protoc -I$(PROTO_ROOT_DIR) -Imodel/protodefs --plugin=protoc-gen-grpc-java=bin/protoc-gen-grpc-java-1.19.0 \
  		--grpc-java_out="model/gen/ship/java" model/protodefs/*.proto
	# @rm -rf /Users/xiaofeiwu/jcloud/vagrant/fedora/fedora-28/ofbiz/ofbiz-framework/plugins/sagas/src/main/java/com/sagas/meta/model
	@rm -rf /Users/xiaofeiwu/jcloud/vagrant/fedora/fedora-28/ofbiz/sagas-base/src/main/java/com/sagas/meta/model
	# @cp -r model/gen/ship/java/com/sagas/meta/model /Users/xiaofeiwu/jcloud/vagrant/fedora/fedora-28/ofbiz/ofbiz-framework/plugins/sagas/src/main/java/com/sagas/meta/model
	@cp -r model/gen/ship/java/com/sagas/meta/model /Users/xiaofeiwu/jcloud/vagrant/fedora/fedora-28/ofbiz/sagas-base/src/main/java/com/sagas/meta/model

_buildjava:
	cd /Users/xiaofeiwu/jcloud/vagrant/fedora/fedora-28/ofbiz/sagas-base && bash build.sh

_build_resource:
	cp model/protodefs/resources.proto $(proto_root)/resources.proto
	cp model/protodefs/forms.proto $(proto_root)/forms.proto
	cp model/protodefs/values.proto $(proto_root)/values.proto
	cd ${JCLOUD_HOME}/assets/langs/workspace/langprocs && mvn compile

_copy_to_rust:
	cp model/protodefs/*.proto ${JCLOUD_HOME}/assets/langs/workspace/rust/workspace/bigmess/sagas-servants/greeter/

gen: _gengo _gendart _genpy _genjava _buildjava _copy_to_rust

genonly: _gengo _gendart _genpy _genjava _copy_to_rust

genres: genonly _build_resource

build: get gen
	@env CGO_ENABLED=0 GOOS=linux GOARCH=386 go build -ldflags '-w -extldflags "-static"' -o build/${PROJECT_NAME}_linux_amd64 .
	@env GOARCH=amd64 go build -ldflags '-w -extldflags "-static"' -o build/${PROJECT_NAME}_macosx_amd64 .

get:
	@go get -u github.com/golang/dep/cmd/dep
	@dep ensure

install: get gen
	@cp config_template.json config.json
