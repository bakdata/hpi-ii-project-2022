# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: student/academic/v1/transparency.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&student/academic/v1/transparency.proto\x12\x13student.academic.v1\"\xd5\x05\n\x0cTransparency\x12\x17\n\x0fregister_number\x18\x01 \x01(\t\x12\x10\n\x08\x65ntry_id\x18\x02 \x01(\r\x12\x14\n\x0c\x65mployee_min\x18\x03 \x01(\r\x12\x14\n\x0c\x65mployee_max\x18\x04 \x01(\r\x12\x17\n\x0frefuse_expenses\x18\x05 \x01(\x08\x12\x19\n\x0c\x65xpenses_min\x18\x06 \x01(\rH\x00\x88\x01\x01\x12\x19\n\x0c\x65xpenses_max\x18\x07 \x01(\rH\x01\x88\x01\x01\x12\x18\n\x0b\x66iscal_year\x18\x08 \x01(\tH\x02\x88\x01\x01\x12\x18\n\x10refuse_allowance\x18\t \x01(\x08\x12\x17\n\x0frefuse_donation\x18\n \x01(\x08\x12*\n\x1d\x64onation_information_required\x18\x0b \x01(\x08H\x03\x88\x01\x01\x12\x1c\n\x14\x66irstPublicationDate\x18\x0c \x01(\t\x12\x18\n\x10\x61\x63\x63ount_inactive\x18\r \x01(\x08\x12:\n\x07persons\x18\x0e \x03(\x0b\x32).student.academic.v1.LegalRepresentatives\x12\x36\n\temployees\x18\x0f \x03(\x0b\x32#.student.academic.v1.NamedEmployees\x12=\n\rorganisations\x18\x10 \x03(\x0b\x32&.student.academic.v1.MembershipEntries\x12\x30\n\tcompanies\x18\x11 \x03(\x0b\x32\x1d.student.academic.v1.Donators\x12\x35\n\x06\x66ields\x18\x12 \x03(\x0b\x32%.student.academic.v1.fieldsOfInterestB\x0f\n\r_expenses_minB\x0f\n\r_expenses_maxB\x0e\n\x0c_fiscal_yearB \n\x1e_donation_information_required\"a\n\x14LegalRepresentatives\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x15\n\x08\x66unction\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x0b\n\t_function\"7\n\x0eNamedEmployees\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\"!\n\x11MembershipEntries\x12\x0c\n\x04name\x18\x01 \x01(\t\"D\n\x08\x44onators\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x66iscal_year\x18\x02 \x01(\t\x12\x15\n\rdonation_euro\x18\x03 \x01(\r\"5\n\x10\x66ieldsOfInterest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\tb\x06proto3')



_TRANSPARENCY = DESCRIPTOR.message_types_by_name['Transparency']
_LEGALREPRESENTATIVES = DESCRIPTOR.message_types_by_name['LegalRepresentatives']
_NAMEDEMPLOYEES = DESCRIPTOR.message_types_by_name['NamedEmployees']
_MEMBERSHIPENTRIES = DESCRIPTOR.message_types_by_name['MembershipEntries']
_DONATORS = DESCRIPTOR.message_types_by_name['Donators']
_FIELDSOFINTEREST = DESCRIPTOR.message_types_by_name['fieldsOfInterest']
Transparency = _reflection.GeneratedProtocolMessageType('Transparency', (_message.Message,), {
  'DESCRIPTOR' : _TRANSPARENCY,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.Transparency)
  })
_sym_db.RegisterMessage(Transparency)

LegalRepresentatives = _reflection.GeneratedProtocolMessageType('LegalRepresentatives', (_message.Message,), {
  'DESCRIPTOR' : _LEGALREPRESENTATIVES,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.LegalRepresentatives)
  })
_sym_db.RegisterMessage(LegalRepresentatives)

NamedEmployees = _reflection.GeneratedProtocolMessageType('NamedEmployees', (_message.Message,), {
  'DESCRIPTOR' : _NAMEDEMPLOYEES,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.NamedEmployees)
  })
_sym_db.RegisterMessage(NamedEmployees)

MembershipEntries = _reflection.GeneratedProtocolMessageType('MembershipEntries', (_message.Message,), {
  'DESCRIPTOR' : _MEMBERSHIPENTRIES,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.MembershipEntries)
  })
_sym_db.RegisterMessage(MembershipEntries)

Donators = _reflection.GeneratedProtocolMessageType('Donators', (_message.Message,), {
  'DESCRIPTOR' : _DONATORS,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.Donators)
  })
_sym_db.RegisterMessage(Donators)

fieldsOfInterest = _reflection.GeneratedProtocolMessageType('fieldsOfInterest', (_message.Message,), {
  'DESCRIPTOR' : _FIELDSOFINTEREST,
  '__module__' : 'student.academic.v1.transparency_pb2'
  # @@protoc_insertion_point(class_scope:student.academic.v1.fieldsOfInterest)
  })
_sym_db.RegisterMessage(fieldsOfInterest)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRANSPARENCY._serialized_start=64
  _TRANSPARENCY._serialized_end=789
  _LEGALREPRESENTATIVES._serialized_start=791
  _LEGALREPRESENTATIVES._serialized_end=888
  _NAMEDEMPLOYEES._serialized_start=890
  _NAMEDEMPLOYEES._serialized_end=945
  _MEMBERSHIPENTRIES._serialized_start=947
  _MEMBERSHIPENTRIES._serialized_end=980
  _DONATORS._serialized_start=982
  _DONATORS._serialized_end=1050
  _FIELDSOFINTEREST._serialized_start=1052
  _FIELDSOFINTEREST._serialized_end=1105
# @@protoc_insertion_point(module_scope)
