# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: services_common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import metainfo_pb2 as metainfo__pb2
import values_pb2 as values__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='services_common.proto',
  package='model',
  syntax='proto3',
  serialized_options=_b('\n\024com.sagas.meta.modelP\001'),
  serialized_pb=_b('\n\x15services_common.proto\x12\x05model\x1a\x0emetainfo.proto\x1a\x0cvalues.proto\"\x15\n\x05Names\x12\x0c\n\x04name\x18\x01 \x03(\t\"\x1f\n\tInfoQuery\x12\x12\n\nqueryItems\x18\x01 \x03(\t\"^\n\x07InfoMap\x12&\n\x04info\x18\x01 \x03(\x0b\x32\x18.model.InfoMap.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\",\n\nModifyInfo\x12\r\n\x05total\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t2p\n\x07SysInfo\x12\x30\n\nGetSysInfo\x12\x10.model.InfoQuery\x1a\x0e.model.InfoMap\"\x00\x12\x33\n\tQueryMeta\x12\x10.model.MetaQuery\x1a\x12.model.MetaPayload\"\x00\x32\x81\x01\n\rEntityServant\x12\x32\n\x0eGetEntityNames\x12\x10.model.InfoQuery\x1a\x0c.model.Names\"\x00\x12<\n\x08StoreAll\x12\x1b.model.TaStringEntriesBatch\x1a\x11.model.ModifyInfo\"\x00\x42\x18\n\x14\x63om.sagas.meta.modelP\x01\x62\x06proto3')
  ,
  dependencies=[metainfo__pb2.DESCRIPTOR,values__pb2.DESCRIPTOR,])




_NAMES = _descriptor.Descriptor(
  name='Names',
  full_name='model.Names',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='model.Names.name', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=62,
  serialized_end=83,
)


_INFOQUERY = _descriptor.Descriptor(
  name='InfoQuery',
  full_name='model.InfoQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='queryItems', full_name='model.InfoQuery.queryItems', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=85,
  serialized_end=116,
)


_INFOMAP_INFOENTRY = _descriptor.Descriptor(
  name='InfoEntry',
  full_name='model.InfoMap.InfoEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='model.InfoMap.InfoEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='model.InfoMap.InfoEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=212,
)

_INFOMAP = _descriptor.Descriptor(
  name='InfoMap',
  full_name='model.InfoMap',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='model.InfoMap.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_INFOMAP_INFOENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=118,
  serialized_end=212,
)


_MODIFYINFO = _descriptor.Descriptor(
  name='ModifyInfo',
  full_name='model.ModifyInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='total', full_name='model.ModifyInfo.total', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='model.ModifyInfo.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=214,
  serialized_end=258,
)

_INFOMAP_INFOENTRY.containing_type = _INFOMAP
_INFOMAP.fields_by_name['info'].message_type = _INFOMAP_INFOENTRY
DESCRIPTOR.message_types_by_name['Names'] = _NAMES
DESCRIPTOR.message_types_by_name['InfoQuery'] = _INFOQUERY
DESCRIPTOR.message_types_by_name['InfoMap'] = _INFOMAP
DESCRIPTOR.message_types_by_name['ModifyInfo'] = _MODIFYINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Names = _reflection.GeneratedProtocolMessageType('Names', (_message.Message,), dict(
  DESCRIPTOR = _NAMES,
  __module__ = 'services_common_pb2'
  # @@protoc_insertion_point(class_scope:model.Names)
  ))
_sym_db.RegisterMessage(Names)

InfoQuery = _reflection.GeneratedProtocolMessageType('InfoQuery', (_message.Message,), dict(
  DESCRIPTOR = _INFOQUERY,
  __module__ = 'services_common_pb2'
  # @@protoc_insertion_point(class_scope:model.InfoQuery)
  ))
_sym_db.RegisterMessage(InfoQuery)

InfoMap = _reflection.GeneratedProtocolMessageType('InfoMap', (_message.Message,), dict(

  InfoEntry = _reflection.GeneratedProtocolMessageType('InfoEntry', (_message.Message,), dict(
    DESCRIPTOR = _INFOMAP_INFOENTRY,
    __module__ = 'services_common_pb2'
    # @@protoc_insertion_point(class_scope:model.InfoMap.InfoEntry)
    ))
  ,
  DESCRIPTOR = _INFOMAP,
  __module__ = 'services_common_pb2'
  # @@protoc_insertion_point(class_scope:model.InfoMap)
  ))
_sym_db.RegisterMessage(InfoMap)
_sym_db.RegisterMessage(InfoMap.InfoEntry)

ModifyInfo = _reflection.GeneratedProtocolMessageType('ModifyInfo', (_message.Message,), dict(
  DESCRIPTOR = _MODIFYINFO,
  __module__ = 'services_common_pb2'
  # @@protoc_insertion_point(class_scope:model.ModifyInfo)
  ))
_sym_db.RegisterMessage(ModifyInfo)


DESCRIPTOR._options = None
_INFOMAP_INFOENTRY._options = None

_SYSINFO = _descriptor.ServiceDescriptor(
  name='SysInfo',
  full_name='model.SysInfo',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=260,
  serialized_end=372,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetSysInfo',
    full_name='model.SysInfo.GetSysInfo',
    index=0,
    containing_service=None,
    input_type=_INFOQUERY,
    output_type=_INFOMAP,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='QueryMeta',
    full_name='model.SysInfo.QueryMeta',
    index=1,
    containing_service=None,
    input_type=metainfo__pb2._METAQUERY,
    output_type=metainfo__pb2._METAPAYLOAD,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SYSINFO)

DESCRIPTOR.services_by_name['SysInfo'] = _SYSINFO


_ENTITYSERVANT = _descriptor.ServiceDescriptor(
  name='EntityServant',
  full_name='model.EntityServant',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=375,
  serialized_end=504,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetEntityNames',
    full_name='model.EntityServant.GetEntityNames',
    index=0,
    containing_service=None,
    input_type=_INFOQUERY,
    output_type=_NAMES,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StoreAll',
    full_name='model.EntityServant.StoreAll',
    index=1,
    containing_service=None,
    input_type=values__pb2._TASTRINGENTRIESBATCH,
    output_type=_MODIFYINFO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ENTITYSERVANT)

DESCRIPTOR.services_by_name['EntityServant'] = _ENTITYSERVANT

# @@protoc_insertion_point(module_scope)