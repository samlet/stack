# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crmsfa.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_types_pb2 as common__types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='crmsfa.proto',
  package='crmsfa',
  syntax='proto3',
  serialized_options=_b('\n\021com.samlet.crmsfaB\013CrmsfaProtoP\001\242\002\006Crmsfa'),
  serialized_pb=_b('\n\x0c\x63rmsfa.proto\x12\x06\x63rmsfa\x1a\x12\x63ommon_types.proto\"\x14\n\x05\x46\x61Ids\x12\x0b\n\x03ids\x18\x01 \x03(\x05\"h\n\x06\x46\x61Odoo\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x12\r\n\x05login\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x05 \x01(\t\x12\x0f\n\x07timeout\x18\x06 \x01(\x05\"\x8d\x01\n\rFaEnvironment\x12\x0b\n\x03uid\x18\x01 \x01(\x05\x12\x33\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\".crmsfa.FaEnvironment.ContextEntry\x12\n\n\x02\x64\x62\x18\x03 \x01(\t\x1a.\n\x0c\x43ontextEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"Y\n\tFaSession\x12\"\n\x03\x65nv\x18\x02 \x01(\x0b\x32\x15.crmsfa.FaEnvironment\x12\x0c\n\x04user\x18\x03 \x01(\t\x12\r\n\x05token\x18\x04 \x01(\t\x12\x0b\n\x03org\x18\x05 \x01(\t\"8\n\x07\x46\x61Model\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1f\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x0f.crmsfa.FaField\"7\n\x07\x46\x61\x46ield\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x10\n\x08readonly\x18\x03 \x01(\x08\"s\n\x08\x46\x61Record\x12\n\n\x02id\x18\x01 \x01(\x05\x12,\n\x06values\x18\x02 \x03(\x0b\x32\x1c.crmsfa.FaRecord.ValuesEntry\x1a-\n\x0bValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"P\n\x0b\x46\x61Recordset\x12\x1e\n\x05model\x18\x01 \x01(\x0b\x32\x0f.crmsfa.FaModel\x12!\n\x07records\x18\x02 \x03(\x0b\x32\x10.crmsfa.FaRecord2?\n\x0b\x43rmsfaProcs\x12\x30\n\x04Ping\x12\x13.common.PingRequest\x1a\x11.common.PingReply\"\x00\x32\xb0\x02\n\tOdooProcs\x12,\n\x05Login\x12\x0e.crmsfa.FaOdoo\x1a\x11.crmsfa.FaSession\"\x00\x12,\n\nSwitchLang\x12\x0c.common.Text\x1a\x0e.common.Result\"\x00\x12/\n\tFieldsGet\x12\x0f.crmsfa.FaModel\x1a\x0f.crmsfa.FaModel\"\x00\x12\x34\n\x0c\x42rowseRecord\x12\r.crmsfa.FaIds\x1a\x13.crmsfa.FaRecordset\"\x00\x12\x34\n\x0bWriteRecord\x12\x13.crmsfa.FaRecordset\x1a\x0e.common.Result\"\x00\x12*\n\x03Ref\x12\x0c.common.Text\x1a\x13.crmsfa.FaRecordset\"\x00\x42+\n\x11\x63om.samlet.crmsfaB\x0b\x43rmsfaProtoP\x01\xa2\x02\x06\x43rmsfab\x06proto3')
  ,
  dependencies=[common__types__pb2.DESCRIPTOR,])




_FAIDS = _descriptor.Descriptor(
  name='FaIds',
  full_name='crmsfa.FaIds',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ids', full_name='crmsfa.FaIds.ids', index=0,
      number=1, type=5, cpp_type=1, label=3,
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
  serialized_start=44,
  serialized_end=64,
)


_FAODOO = _descriptor.Descriptor(
  name='FaOdoo',
  full_name='crmsfa.FaOdoo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='crmsfa.FaOdoo.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='crmsfa.FaOdoo.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='login', full_name='crmsfa.FaOdoo.login', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='crmsfa.FaOdoo.password', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='database', full_name='crmsfa.FaOdoo.database', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='crmsfa.FaOdoo.timeout', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=66,
  serialized_end=170,
)


_FAENVIRONMENT_CONTEXTENTRY = _descriptor.Descriptor(
  name='ContextEntry',
  full_name='crmsfa.FaEnvironment.ContextEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='crmsfa.FaEnvironment.ContextEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='crmsfa.FaEnvironment.ContextEntry.value', index=1,
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
  serialized_start=268,
  serialized_end=314,
)

_FAENVIRONMENT = _descriptor.Descriptor(
  name='FaEnvironment',
  full_name='crmsfa.FaEnvironment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='crmsfa.FaEnvironment.uid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='context', full_name='crmsfa.FaEnvironment.context', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='db', full_name='crmsfa.FaEnvironment.db', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_FAENVIRONMENT_CONTEXTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=173,
  serialized_end=314,
)


_FASESSION = _descriptor.Descriptor(
  name='FaSession',
  full_name='crmsfa.FaSession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='env', full_name='crmsfa.FaSession.env', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user', full_name='crmsfa.FaSession.user', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='token', full_name='crmsfa.FaSession.token', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='org', full_name='crmsfa.FaSession.org', index=3,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=316,
  serialized_end=405,
)


_FAMODEL = _descriptor.Descriptor(
  name='FaModel',
  full_name='crmsfa.FaModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='crmsfa.FaModel.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fields', full_name='crmsfa.FaModel.fields', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=407,
  serialized_end=463,
)


_FAFIELD = _descriptor.Descriptor(
  name='FaField',
  full_name='crmsfa.FaField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='crmsfa.FaField.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='crmsfa.FaField.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='readonly', full_name='crmsfa.FaField.readonly', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=465,
  serialized_end=520,
)


_FARECORD_VALUESENTRY = _descriptor.Descriptor(
  name='ValuesEntry',
  full_name='crmsfa.FaRecord.ValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='crmsfa.FaRecord.ValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='crmsfa.FaRecord.ValuesEntry.value', index=1,
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
  serialized_start=592,
  serialized_end=637,
)

_FARECORD = _descriptor.Descriptor(
  name='FaRecord',
  full_name='crmsfa.FaRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='crmsfa.FaRecord.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='values', full_name='crmsfa.FaRecord.values', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_FARECORD_VALUESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=522,
  serialized_end=637,
)


_FARECORDSET = _descriptor.Descriptor(
  name='FaRecordset',
  full_name='crmsfa.FaRecordset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='crmsfa.FaRecordset.model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='records', full_name='crmsfa.FaRecordset.records', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=639,
  serialized_end=719,
)

_FAENVIRONMENT_CONTEXTENTRY.containing_type = _FAENVIRONMENT
_FAENVIRONMENT.fields_by_name['context'].message_type = _FAENVIRONMENT_CONTEXTENTRY
_FASESSION.fields_by_name['env'].message_type = _FAENVIRONMENT
_FAMODEL.fields_by_name['fields'].message_type = _FAFIELD
_FARECORD_VALUESENTRY.containing_type = _FARECORD
_FARECORD.fields_by_name['values'].message_type = _FARECORD_VALUESENTRY
_FARECORDSET.fields_by_name['model'].message_type = _FAMODEL
_FARECORDSET.fields_by_name['records'].message_type = _FARECORD
DESCRIPTOR.message_types_by_name['FaIds'] = _FAIDS
DESCRIPTOR.message_types_by_name['FaOdoo'] = _FAODOO
DESCRIPTOR.message_types_by_name['FaEnvironment'] = _FAENVIRONMENT
DESCRIPTOR.message_types_by_name['FaSession'] = _FASESSION
DESCRIPTOR.message_types_by_name['FaModel'] = _FAMODEL
DESCRIPTOR.message_types_by_name['FaField'] = _FAFIELD
DESCRIPTOR.message_types_by_name['FaRecord'] = _FARECORD
DESCRIPTOR.message_types_by_name['FaRecordset'] = _FARECORDSET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FaIds = _reflection.GeneratedProtocolMessageType('FaIds', (_message.Message,), dict(
  DESCRIPTOR = _FAIDS,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaIds)
  ))
_sym_db.RegisterMessage(FaIds)

FaOdoo = _reflection.GeneratedProtocolMessageType('FaOdoo', (_message.Message,), dict(
  DESCRIPTOR = _FAODOO,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaOdoo)
  ))
_sym_db.RegisterMessage(FaOdoo)

FaEnvironment = _reflection.GeneratedProtocolMessageType('FaEnvironment', (_message.Message,), dict(

  ContextEntry = _reflection.GeneratedProtocolMessageType('ContextEntry', (_message.Message,), dict(
    DESCRIPTOR = _FAENVIRONMENT_CONTEXTENTRY,
    __module__ = 'crmsfa_pb2'
    # @@protoc_insertion_point(class_scope:crmsfa.FaEnvironment.ContextEntry)
    ))
  ,
  DESCRIPTOR = _FAENVIRONMENT,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaEnvironment)
  ))
_sym_db.RegisterMessage(FaEnvironment)
_sym_db.RegisterMessage(FaEnvironment.ContextEntry)

FaSession = _reflection.GeneratedProtocolMessageType('FaSession', (_message.Message,), dict(
  DESCRIPTOR = _FASESSION,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaSession)
  ))
_sym_db.RegisterMessage(FaSession)

FaModel = _reflection.GeneratedProtocolMessageType('FaModel', (_message.Message,), dict(
  DESCRIPTOR = _FAMODEL,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaModel)
  ))
_sym_db.RegisterMessage(FaModel)

FaField = _reflection.GeneratedProtocolMessageType('FaField', (_message.Message,), dict(
  DESCRIPTOR = _FAFIELD,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaField)
  ))
_sym_db.RegisterMessage(FaField)

FaRecord = _reflection.GeneratedProtocolMessageType('FaRecord', (_message.Message,), dict(

  ValuesEntry = _reflection.GeneratedProtocolMessageType('ValuesEntry', (_message.Message,), dict(
    DESCRIPTOR = _FARECORD_VALUESENTRY,
    __module__ = 'crmsfa_pb2'
    # @@protoc_insertion_point(class_scope:crmsfa.FaRecord.ValuesEntry)
    ))
  ,
  DESCRIPTOR = _FARECORD,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaRecord)
  ))
_sym_db.RegisterMessage(FaRecord)
_sym_db.RegisterMessage(FaRecord.ValuesEntry)

FaRecordset = _reflection.GeneratedProtocolMessageType('FaRecordset', (_message.Message,), dict(
  DESCRIPTOR = _FARECORDSET,
  __module__ = 'crmsfa_pb2'
  # @@protoc_insertion_point(class_scope:crmsfa.FaRecordset)
  ))
_sym_db.RegisterMessage(FaRecordset)


DESCRIPTOR._options = None
_FAENVIRONMENT_CONTEXTENTRY._options = None
_FARECORD_VALUESENTRY._options = None

_CRMSFAPROCS = _descriptor.ServiceDescriptor(
  name='CrmsfaProcs',
  full_name='crmsfa.CrmsfaProcs',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=721,
  serialized_end=784,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='crmsfa.CrmsfaProcs.Ping',
    index=0,
    containing_service=None,
    input_type=common__types__pb2._PINGREQUEST,
    output_type=common__types__pb2._PINGREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CRMSFAPROCS)

DESCRIPTOR.services_by_name['CrmsfaProcs'] = _CRMSFAPROCS


_ODOOPROCS = _descriptor.ServiceDescriptor(
  name='OdooProcs',
  full_name='crmsfa.OdooProcs',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=787,
  serialized_end=1091,
  methods=[
  _descriptor.MethodDescriptor(
    name='Login',
    full_name='crmsfa.OdooProcs.Login',
    index=0,
    containing_service=None,
    input_type=_FAODOO,
    output_type=_FASESSION,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SwitchLang',
    full_name='crmsfa.OdooProcs.SwitchLang',
    index=1,
    containing_service=None,
    input_type=common__types__pb2._TEXT,
    output_type=common__types__pb2._RESULT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FieldsGet',
    full_name='crmsfa.OdooProcs.FieldsGet',
    index=2,
    containing_service=None,
    input_type=_FAMODEL,
    output_type=_FAMODEL,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='BrowseRecord',
    full_name='crmsfa.OdooProcs.BrowseRecord',
    index=3,
    containing_service=None,
    input_type=_FAIDS,
    output_type=_FARECORDSET,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WriteRecord',
    full_name='crmsfa.OdooProcs.WriteRecord',
    index=4,
    containing_service=None,
    input_type=_FARECORDSET,
    output_type=common__types__pb2._RESULT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Ref',
    full_name='crmsfa.OdooProcs.Ref',
    index=5,
    containing_service=None,
    input_type=common__types__pb2._TEXT,
    output_type=_FARECORDSET,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ODOOPROCS)

DESCRIPTOR.services_by_name['OdooProcs'] = _ODOOPROCS

# @@protoc_insertion_point(module_scope)