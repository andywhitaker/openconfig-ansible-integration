# -*- coding: utf-8 -*-
# (c) 2025 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#
"""Runtime protobuf descriptor loader for gnmi_ext.proto (gNMI v0.14.1)."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2  # noqa: F401
from google.protobuf import message_factory as _message_factory
from google.protobuf import symbol_database as _symbol_database


class _EnumWrapper:
    def __init__(self, enum_desc):
        self.DESCRIPTOR = enum_desc
        for v in enum_desc.values:
            setattr(self, v.name, v.number)

    def Name(self, number):
        try:
            return self.DESCRIPTOR.values_by_number[number].name
        except KeyError:
            raise ValueError('Enum %s has no name defined for value %r' % (self.DESCRIPTOR.name, number))

    def Value(self, name):
        try:
            return self.DESCRIPTOR.values_by_name[name].number
        except KeyError:
            raise ValueError('Enum %s has no value defined for name %r' % (self.DESCRIPTOR.name, name))

    def keys(self):
        return [v.name for v in self.DESCRIPTOR.values]

    def values(self):
        return [v.number for v in self.DESCRIPTOR.values]

    def items(self):
        return [(v.name, v.number) for v in self.DESCRIPTOR.values]


_SERIALIZED_FD = (
    b'\n\x0egnmi_ext.proto\x12\x08gnmi_ext\x1a\x1egoogle/protobuf/duration.proto'
    b'\"\xaf\x02\n\tExtension\x12\x37\n\x0eregistered_ext\x18\x01 \x01(\x0b\x32\x1d.gnmi_ext.RegisteredExtensionH\x00'
    b'\x12\x39\n\x12master_arbitration\x18\x02 \x01(\x0b\x32\x1b.gnmi_ext.MasterArbitrationH\x00'
    b'\x12$\n\x07history\x18\x03 \x01(\x0b\x32\x11.gnmi_ext.HistoryH\x00'
    b'\x12\"\n\x06\x63ommit\x18\x04 \x01(\x0b\x32\x10.gnmi_ext.CommitH\x00'
    b'\x12 \n\x05\x64\x65pth\x18\x05 \x01(\x0b\x32\x0f.gnmi_ext.DepthH\x00'
    b'\x12;\n\x13\x63onfig_subscription\x18\x06 \x01(\x0b\x32\x1c.gnmi_ext.ConfigSubscriptionH\x00\x42\x05\n\x03\x65xt'
    b'\"E\n\x13RegisteredExtension\x12!\n\x02id\x18\x01 \x01(\x0e\x32\x15.gnmi_ext.ExtensionID\x12\x0b\n\x03msg\x18\x02 \x01(\x0c'
    b'\"Y\n\x11MasterArbitration\x12\x1c\n\x04role\x18\x01 \x01(\x0b\x32\x0e.gnmi_ext.Role\x12&\n\x0b\x65lection_id\x18\x02 \x01(\x0b\x32\x11.gnmi_ext.Uint128'
    b'\"$\n\x07Uint128\x12\x0c\n\x04high\x18\x01 \x01(\x04\x12\x0b\n\x03low\x18\x02 \x01(\x04'
    b'\"\x12\n\x04Role\x12\n\n\x02id\x18\x01 \x01(\t'
    b'\"S\n\x07History\x12\x17\n\rsnapshot_time\x18\x01 \x01(\x03H\x00\x12$\n\x05range\x18\x02 \x01(\x0b\x32\x13.gnmi_ext.TimeRangeH\x00\x42\t\n\x07request'
    b'\"\x27\n\tTimeRange\x12\r\n\x05start\x18\x01 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x03'
    b'\"\xe5\x01\n\x06\x43ommit\x12\n\n\x02id\x18\x01 \x01(\t\x12)\n\x06\x63ommit\x18\x02 \x01(\x0b\x32\x17.gnmi_ext.CommitRequestH\x00'
    b'\x12*\n\x07\x63onfirm\x18\x03 \x01(\x0b\x32\x17.gnmi_ext.CommitConfirmH\x00'
    b'\x12(\n\x06\x63\x61ncel\x18\x04 \x01(\x0b\x32\x16.gnmi_ext.CommitCancelH\x00'
    b'\x12\x44\n\x15set_rollback_duration\x18\x05 \x01(\x0b\x32#.gnmi_ext.CommitSetRollbackDurationH\x00\x42\x08\n\x06\x61\x63tion'
    b'\"E\n\rCommitRequest\x12\x34\n\x11rollback_duration\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration'
    b'\"\x0f\n\rCommitConfirm\"\x0e\n\x0c\x43ommitCancel'
    b'\"Q\n\x19\x43ommitSetRollbackDuration\x12\x34\n\x11rollback_duration\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration'
    b'\"\x16\n\x05\x44\x65pth\x12\r\n\x05level\x18\x01 \x01(\r'
    b'\"\x8d\x01\n\x12\x43onfigSubscription\x12\x32\n\x05start\x18\x01 \x01(\x0b\x32!.gnmi_ext.ConfigSubscriptionStartH\x00'
    b'\x12\x39\n\tsync_done\x18\x02 \x01(\x0b\x32$.gnmi_ext.ConfigSubscriptionSyncDoneH\x00\x42\x08\n\x06\x61\x63tion'
    b'\"\x19\n\x17\x43onfigSubscriptionStart'
    b'\"_\n\x1a\x43onfigSubscriptionSyncDone\x12\x19\n\x11\x63ommit_confirm_id\x18\x01 \x01(\t\x12\x18\n\x10server_commit_id\x18\x02 \x01(\t\x12\x0c\n\x04\x64one\x18\x03 \x01(\x08'
    b'*3\n\x0b\x45xtensionID\x12\r\n\tEID_UNSET\x10\x00\x12\x15\n\x10\x45ID_EXPERIMENTAL\x10\xe7\x07\x42+Z)github.com/openconfig/gnmi/proto/gnmi_extb\x06proto3'
)

_pool = _descriptor_pool.Default()
try:
    DESCRIPTOR = _pool.FindFileByName('gnmi_ext.proto')
except KeyError:
    DESCRIPTOR = _pool.AddSerializedFile(_SERIALIZED_FD)

_sym_db = _symbol_database.Default()
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_get_msg_cls = getattr(_message_factory, 'GetMessageClass', None) or _message_factory.MessageFactory().GetPrototype
for _name, _desc in DESCRIPTOR.message_types_by_name.items():
    _cls = _get_msg_cls(_desc)
    globals()[_name] = _cls
    _sym_db.RegisterMessage(_cls)
    for _sub_desc in _desc.nested_types:
        _sub_cls = getattr(_cls, _sub_desc.name, None) or _get_msg_cls(_sub_desc)
        if not hasattr(_cls, _sub_desc.name):
            setattr(_cls, _sub_desc.name, _sub_cls)
        _sym_db.RegisterMessage(_sub_cls)
    for _sub_edesc in _desc.enum_types:
        _sym_db.RegisterEnumDescriptor(_sub_edesc)

for _name, _edesc in DESCRIPTOR.enum_types_by_name.items():
    globals()[_name] = _EnumWrapper(_edesc)
    _sym_db.RegisterEnumDescriptor(_edesc)
    for _v in _edesc.values:
        globals()[_v.name] = _v.number
