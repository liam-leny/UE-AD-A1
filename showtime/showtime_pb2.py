# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: showtime.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'showtime.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eshowtime.proto\"\x07\n\x05\x45mpty\"\x1b\n\x0b\x44\x61teRequest\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\",\n\x0cShowtimeData\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0e\n\x06movies\x18\x02 \x03(\t2j\n\x08Showtime\x12)\n\x0cGetShowtimes\x12\x06.Empty\x1a\r.ShowtimeData\"\x00\x30\x01\x12\x33\n\x12GetShowtimesByDate\x12\x0c.DateRequest\x1a\r.ShowtimeData\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'showtime_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=18
  _globals['_EMPTY']._serialized_end=25
  _globals['_DATEREQUEST']._serialized_start=27
  _globals['_DATEREQUEST']._serialized_end=54
  _globals['_SHOWTIMEDATA']._serialized_start=56
  _globals['_SHOWTIMEDATA']._serialized_end=100
  _globals['_SHOWTIME']._serialized_start=102
  _globals['_SHOWTIME']._serialized_end=208
# @@protoc_insertion_point(module_scope)