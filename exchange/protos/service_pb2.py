# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from exchange.protos import order_book_pb2 as protos_dot_order__book__pb2
try:
  protos_dot_competitor__pb2 = protos_dot_order__book__pb2.protos_dot_competitor__pb2
except AttributeError:
  protos_dot_competitor__pb2 = protos_dot_order__book__pb2.protos.competitor_pb2
from exchange.protos import competitor_pb2 as protos_dot_competitor__pb2
from exchange.protos import exchange_pb2 as protos_dot_exchange__pb2

from exchange.protos.order_book_pb2 import *
from exchange.protos.competitor_pb2 import *
from exchange.protos.exchange_pb2 import *

DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/service.proto',
  package='protos',
  syntax='proto2',
  serialized_pb=_b('\n\x14protos/service.proto\x12\x06protos\x1a\x17protos/order_book.proto\x1a\x17protos/competitor.proto\x1a\x15protos/exchange.proto\"X\n\x19RegisterCompetitorRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\"\xa2\x01\n\x1aRegisterCompetitorResponse\x12=\n\x06status\x18\x01 \x01(\x0e\x32-.protos.RegisterCompetitorResponse.StatusCode\x12\x16\n\x0estatus_message\x18\x02 \x01(\t\"-\n\nStatusCode\x12\r\n\tSTATUS_OK\x10\x01\x12\x10\n\x0cSTATUS_ERROR\x10\x02\"[\n\x1cGetCompetitorMetadataRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\"X\n\x1dGetCompetitorMetadataResponse\x12\x37\n\x13\x63ompetitor_metadata\x18\x01 \x01(\x0b\x32\x1a.protos.CompetitorMetadata\"n\n\x11PlaceOrderRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\x12\x1c\n\x05order\x18\x02 \x01(\x0b\x32\r.protos.Order\"C\n\x12PlaceOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x1b\n\x05\x66ills\x18\x02 \x03(\x0b\x32\x0c.protos.Fill\"\x85\x01\n\x12ModifyOrderRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12 \n\tnew_order\x18\x03 \x01(\x0b\x32\r.protos.Order\"\'\n\x13ModifyOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\"c\n\x12\x43\x61ncelOrderRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\x12\x10\n\x08order_id\x18\x02 \x02(\t\"&\n\x13\x43\x61ncelOrderResponse\x12\x0f\n\x07success\x18\x01 \x02(\x08\"W\n\x18GetExchangeUpdateRequest\x12;\n\x15\x63ompetitor_identifier\x18\x01 \x01(\x0b\x32\x1c.protos.CompetitorIdentifier\"\x9f\x01\n\x19GetExchangeUpdateResponse\x12\x1b\n\x05\x66ills\x18\x01 \x03(\x0b\x32\x0c.protos.Fill\x12,\n\x0emarket_updates\x18\x02 \x03(\x0b\x32\x14.protos.MarketUpdate\x12\x37\n\x13\x63ompetitor_metadata\x18\x03 \x01(\x0b\x32\x1a.protos.CompetitorMetadata2\x91\x04\n\x0f\x45xchangeService\x12]\n\x12RegisterCompetitor\x12!.protos.RegisterCompetitorRequest\x1a\".protos.RegisterCompetitorResponse\"\x00\x12\x66\n\x15GetCompetitorMetadata\x12$.protos.GetCompetitorMetadataRequest\x1a%.protos.GetCompetitorMetadataResponse\"\x00\x12\x45\n\nPlaceOrder\x12\x19.protos.PlaceOrderRequest\x1a\x1a.protos.PlaceOrderResponse\"\x00\x12H\n\x0bModifyOrder\x12\x1a.protos.ModifyOrderRequest\x1a\x1b.protos.ModifyOrderResponse\"\x00\x12H\n\x0b\x43\x61ncelOrder\x12\x1a.protos.CancelOrderRequest\x1a\x1b.protos.CancelOrderResponse\"\x00\x12\\\n\x11GetExchangeUpdate\x12 .protos.GetExchangeUpdateRequest\x1a!.protos.GetExchangeUpdateResponse\"\x00\x30\x01P\x00P\x01P\x02')
  ,
  dependencies=[protos_dot_order__book__pb2.DESCRIPTOR,protos_dot_competitor__pb2.DESCRIPTOR,protos_dot_exchange__pb2.DESCRIPTOR,],
  public_dependencies=[protos_dot_order__book__pb2.DESCRIPTOR,protos_dot_competitor__pb2.DESCRIPTOR,protos_dot_exchange__pb2.DESCRIPTOR,])



_REGISTERCOMPETITORRESPONSE_STATUSCODE = _descriptor.EnumDescriptor(
  name='StatusCode',
  full_name='protos.RegisterCompetitorResponse.StatusCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_OK', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=313,
  serialized_end=358,
)
_sym_db.RegisterEnumDescriptor(_REGISTERCOMPETITORRESPONSE_STATUSCODE)


_REGISTERCOMPETITORREQUEST = _descriptor.Descriptor(
  name='RegisterCompetitorRequest',
  full_name='protos.RegisterCompetitorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.RegisterCompetitorRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=105,
  serialized_end=193,
)


_REGISTERCOMPETITORRESPONSE = _descriptor.Descriptor(
  name='RegisterCompetitorResponse',
  full_name='protos.RegisterCompetitorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='protos.RegisterCompetitorResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_message', full_name='protos.RegisterCompetitorResponse.status_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REGISTERCOMPETITORRESPONSE_STATUSCODE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=196,
  serialized_end=358,
)


_GETCOMPETITORMETADATAREQUEST = _descriptor.Descriptor(
  name='GetCompetitorMetadataRequest',
  full_name='protos.GetCompetitorMetadataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.GetCompetitorMetadataRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=360,
  serialized_end=451,
)


_GETCOMPETITORMETADATARESPONSE = _descriptor.Descriptor(
  name='GetCompetitorMetadataResponse',
  full_name='protos.GetCompetitorMetadataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_metadata', full_name='protos.GetCompetitorMetadataResponse.competitor_metadata', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=453,
  serialized_end=541,
)


_PLACEORDERREQUEST = _descriptor.Descriptor(
  name='PlaceOrderRequest',
  full_name='protos.PlaceOrderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.PlaceOrderRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order', full_name='protos.PlaceOrderRequest.order', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=543,
  serialized_end=653,
)


_PLACEORDERRESPONSE = _descriptor.Descriptor(
  name='PlaceOrderResponse',
  full_name='protos.PlaceOrderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order_id', full_name='protos.PlaceOrderResponse.order_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fills', full_name='protos.PlaceOrderResponse.fills', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=655,
  serialized_end=722,
)


_MODIFYORDERREQUEST = _descriptor.Descriptor(
  name='ModifyOrderRequest',
  full_name='protos.ModifyOrderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.ModifyOrderRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='protos.ModifyOrderRequest.order_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='new_order', full_name='protos.ModifyOrderRequest.new_order', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=725,
  serialized_end=858,
)


_MODIFYORDERRESPONSE = _descriptor.Descriptor(
  name='ModifyOrderResponse',
  full_name='protos.ModifyOrderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order_id', full_name='protos.ModifyOrderResponse.order_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=860,
  serialized_end=899,
)


_CANCELORDERREQUEST = _descriptor.Descriptor(
  name='CancelOrderRequest',
  full_name='protos.CancelOrderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.CancelOrderRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='protos.CancelOrderRequest.order_id', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=901,
  serialized_end=1000,
)


_CANCELORDERRESPONSE = _descriptor.Descriptor(
  name='CancelOrderResponse',
  full_name='protos.CancelOrderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='protos.CancelOrderResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1002,
  serialized_end=1040,
)


_GETEXCHANGEUPDATEREQUEST = _descriptor.Descriptor(
  name='GetExchangeUpdateRequest',
  full_name='protos.GetExchangeUpdateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='competitor_identifier', full_name='protos.GetExchangeUpdateRequest.competitor_identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1042,
  serialized_end=1129,
)


_GETEXCHANGEUPDATERESPONSE = _descriptor.Descriptor(
  name='GetExchangeUpdateResponse',
  full_name='protos.GetExchangeUpdateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fills', full_name='protos.GetExchangeUpdateResponse.fills', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market_updates', full_name='protos.GetExchangeUpdateResponse.market_updates', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='competitor_metadata', full_name='protos.GetExchangeUpdateResponse.competitor_metadata', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1132,
  serialized_end=1291,
)

_REGISTERCOMPETITORREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_REGISTERCOMPETITORRESPONSE.fields_by_name['status'].enum_type = _REGISTERCOMPETITORRESPONSE_STATUSCODE
_REGISTERCOMPETITORRESPONSE_STATUSCODE.containing_type = _REGISTERCOMPETITORRESPONSE
_GETCOMPETITORMETADATAREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_GETCOMPETITORMETADATARESPONSE.fields_by_name['competitor_metadata'].message_type = protos_dot_competitor__pb2._COMPETITORMETADATA
_PLACEORDERREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_PLACEORDERREQUEST.fields_by_name['order'].message_type = protos_dot_order__book__pb2._ORDER
_PLACEORDERRESPONSE.fields_by_name['fills'].message_type = protos_dot_order__book__pb2._FILL
_MODIFYORDERREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_MODIFYORDERREQUEST.fields_by_name['new_order'].message_type = protos_dot_order__book__pb2._ORDER
_CANCELORDERREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_GETEXCHANGEUPDATEREQUEST.fields_by_name['competitor_identifier'].message_type = protos_dot_competitor__pb2._COMPETITORIDENTIFIER
_GETEXCHANGEUPDATERESPONSE.fields_by_name['fills'].message_type = protos_dot_order__book__pb2._FILL
_GETEXCHANGEUPDATERESPONSE.fields_by_name['market_updates'].message_type = protos_dot_exchange__pb2._MARKETUPDATE
_GETEXCHANGEUPDATERESPONSE.fields_by_name['competitor_metadata'].message_type = protos_dot_competitor__pb2._COMPETITORMETADATA
DESCRIPTOR.message_types_by_name['RegisterCompetitorRequest'] = _REGISTERCOMPETITORREQUEST
DESCRIPTOR.message_types_by_name['RegisterCompetitorResponse'] = _REGISTERCOMPETITORRESPONSE
DESCRIPTOR.message_types_by_name['GetCompetitorMetadataRequest'] = _GETCOMPETITORMETADATAREQUEST
DESCRIPTOR.message_types_by_name['GetCompetitorMetadataResponse'] = _GETCOMPETITORMETADATARESPONSE
DESCRIPTOR.message_types_by_name['PlaceOrderRequest'] = _PLACEORDERREQUEST
DESCRIPTOR.message_types_by_name['PlaceOrderResponse'] = _PLACEORDERRESPONSE
DESCRIPTOR.message_types_by_name['ModifyOrderRequest'] = _MODIFYORDERREQUEST
DESCRIPTOR.message_types_by_name['ModifyOrderResponse'] = _MODIFYORDERRESPONSE
DESCRIPTOR.message_types_by_name['CancelOrderRequest'] = _CANCELORDERREQUEST
DESCRIPTOR.message_types_by_name['CancelOrderResponse'] = _CANCELORDERRESPONSE
DESCRIPTOR.message_types_by_name['GetExchangeUpdateRequest'] = _GETEXCHANGEUPDATEREQUEST
DESCRIPTOR.message_types_by_name['GetExchangeUpdateResponse'] = _GETEXCHANGEUPDATERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RegisterCompetitorRequest = _reflection.GeneratedProtocolMessageType('RegisterCompetitorRequest', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERCOMPETITORREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.RegisterCompetitorRequest)
  ))
_sym_db.RegisterMessage(RegisterCompetitorRequest)

RegisterCompetitorResponse = _reflection.GeneratedProtocolMessageType('RegisterCompetitorResponse', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERCOMPETITORRESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.RegisterCompetitorResponse)
  ))
_sym_db.RegisterMessage(RegisterCompetitorResponse)

GetCompetitorMetadataRequest = _reflection.GeneratedProtocolMessageType('GetCompetitorMetadataRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCOMPETITORMETADATAREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.GetCompetitorMetadataRequest)
  ))
_sym_db.RegisterMessage(GetCompetitorMetadataRequest)

GetCompetitorMetadataResponse = _reflection.GeneratedProtocolMessageType('GetCompetitorMetadataResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETCOMPETITORMETADATARESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.GetCompetitorMetadataResponse)
  ))
_sym_db.RegisterMessage(GetCompetitorMetadataResponse)

PlaceOrderRequest = _reflection.GeneratedProtocolMessageType('PlaceOrderRequest', (_message.Message,), dict(
  DESCRIPTOR = _PLACEORDERREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.PlaceOrderRequest)
  ))
_sym_db.RegisterMessage(PlaceOrderRequest)

PlaceOrderResponse = _reflection.GeneratedProtocolMessageType('PlaceOrderResponse', (_message.Message,), dict(
  DESCRIPTOR = _PLACEORDERRESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.PlaceOrderResponse)
  ))
_sym_db.RegisterMessage(PlaceOrderResponse)

ModifyOrderRequest = _reflection.GeneratedProtocolMessageType('ModifyOrderRequest', (_message.Message,), dict(
  DESCRIPTOR = _MODIFYORDERREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.ModifyOrderRequest)
  ))
_sym_db.RegisterMessage(ModifyOrderRequest)

ModifyOrderResponse = _reflection.GeneratedProtocolMessageType('ModifyOrderResponse', (_message.Message,), dict(
  DESCRIPTOR = _MODIFYORDERRESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.ModifyOrderResponse)
  ))
_sym_db.RegisterMessage(ModifyOrderResponse)

CancelOrderRequest = _reflection.GeneratedProtocolMessageType('CancelOrderRequest', (_message.Message,), dict(
  DESCRIPTOR = _CANCELORDERREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.CancelOrderRequest)
  ))
_sym_db.RegisterMessage(CancelOrderRequest)

CancelOrderResponse = _reflection.GeneratedProtocolMessageType('CancelOrderResponse', (_message.Message,), dict(
  DESCRIPTOR = _CANCELORDERRESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.CancelOrderResponse)
  ))
_sym_db.RegisterMessage(CancelOrderResponse)

GetExchangeUpdateRequest = _reflection.GeneratedProtocolMessageType('GetExchangeUpdateRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETEXCHANGEUPDATEREQUEST,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.GetExchangeUpdateRequest)
  ))
_sym_db.RegisterMessage(GetExchangeUpdateRequest)

GetExchangeUpdateResponse = _reflection.GeneratedProtocolMessageType('GetExchangeUpdateResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETEXCHANGEUPDATERESPONSE,
  __module__ = 'protos.service_pb2'
  # @@protoc_insertion_point(class_scope:protos.GetExchangeUpdateResponse)
  ))
_sym_db.RegisterMessage(GetExchangeUpdateResponse)



_EXCHANGESERVICE = _descriptor.ServiceDescriptor(
  name='ExchangeService',
  full_name='protos.ExchangeService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=1294,
  serialized_end=1823,
  methods=[
  _descriptor.MethodDescriptor(
    name='RegisterCompetitor',
    full_name='protos.ExchangeService.RegisterCompetitor',
    index=0,
    containing_service=None,
    input_type=_REGISTERCOMPETITORREQUEST,
    output_type=_REGISTERCOMPETITORRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetCompetitorMetadata',
    full_name='protos.ExchangeService.GetCompetitorMetadata',
    index=1,
    containing_service=None,
    input_type=_GETCOMPETITORMETADATAREQUEST,
    output_type=_GETCOMPETITORMETADATARESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PlaceOrder',
    full_name='protos.ExchangeService.PlaceOrder',
    index=2,
    containing_service=None,
    input_type=_PLACEORDERREQUEST,
    output_type=_PLACEORDERRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ModifyOrder',
    full_name='protos.ExchangeService.ModifyOrder',
    index=3,
    containing_service=None,
    input_type=_MODIFYORDERREQUEST,
    output_type=_MODIFYORDERRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CancelOrder',
    full_name='protos.ExchangeService.CancelOrder',
    index=4,
    containing_service=None,
    input_type=_CANCELORDERREQUEST,
    output_type=_CANCELORDERRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetExchangeUpdate',
    full_name='protos.ExchangeService.GetExchangeUpdate',
    index=5,
    containing_service=None,
    input_type=_GETEXCHANGEUPDATEREQUEST,
    output_type=_GETEXCHANGEUPDATERESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_EXCHANGESERVICE)

DESCRIPTOR.services_by_name['ExchangeService'] = _EXCHANGESERVICE

# @@protoc_insertion_point(module_scope)
