# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hello.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hello.proto',
  package='model',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bhello.proto\x12\x05model\x1a\x1bgoogle/protobuf/empty.proto\"!\n\rResponseHello\x12\x10\n\x08response\x18\x01 \x01(\t2J\n\x0cHelloService\x12:\n\x08SayHello\x12\x16.google.protobuf.Empty\x1a\x14.model.ResponseHello\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_RESPONSEHELLO = _descriptor.Descriptor(
  name='ResponseHello',
  full_name='model.ResponseHello',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='model.ResponseHello.response', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=84,
)

DESCRIPTOR.message_types_by_name['ResponseHello'] = _RESPONSEHELLO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResponseHello = _reflection.GeneratedProtocolMessageType('ResponseHello', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSEHELLO,
  __module__ = 'hello_pb2'
  # @@protoc_insertion_point(class_scope:model.ResponseHello)
  ))
_sym_db.RegisterMessage(ResponseHello)



_HELLOSERVICE = _descriptor.ServiceDescriptor(
  name='HelloService',
  full_name='model.HelloService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=86,
  serialized_end=160,
  methods=[
  _descriptor.MethodDescriptor(
    name='SayHello',
    full_name='model.HelloService.SayHello',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_RESPONSEHELLO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_HELLOSERVICE)

DESCRIPTOR.services_by_name['HelloService'] = _HELLOSERVICE

# @@protoc_insertion_point(module_scope)
