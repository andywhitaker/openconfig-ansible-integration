# -*- coding: utf-8 -*-
# (c) 2025 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#
"""Runtime protobuf descriptor loader for gnmi.proto (gNMI v0.14.1)."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2  # noqa: F401
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2  # noqa: F401
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message_factory as _message_factory
from google.protobuf import symbol_database as _symbol_database
from ansible_collections.nokia.openconfig.plugins.utils import gnmi_ext_pb2 as gnmi__ext__pb2  # noqa: F401


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
    b'\n\ngnmi.proto\x12\x04gnmi\x1a\x19google/protobuf/any.proto\x1a google/protobuf/descriptor.proto\x1a\x0egnmi_ext.proto'
    b'\"\x94\x01\n\x0cNotification\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x1a\n\x06prefix\x18\x02 \x01(\x0b\x32\n.gnmi.Path\x12\x1c\n\x06update\x18\x04 \x03(\x0b\x32\x0c.gnmi.Update\x12\x1a\n\x06\x64\x65lete\x18\x05 \x03(\x0b\x32\n.gnmi.Path\x12\x0e\n\x06\x61tomic\x18\x06 \x01(\x08J\x04\x08\x03\x10\x04R\x05\x61lias'
    b'\"u\n\x06Update\x12\x18\n\x04path\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0b.gnmi.ValueB\x02\x18\x01\x12\x1d\n\x03val\x18\x03 \x01(\x0b\x32\x10.gnmi.TypedValue\x12\x12\n\nduplicates\x18\x04 \x01(\r'
    b'\"\x83\x03\n\nTypedValue\x12\x14\n\nstring_val\x18\x01 \x01(\tH\x00\x12\x11\n\x07int_val\x18\x02 \x01(\x03H\x00\x12\x12\n\x08uint_val\x18\x03 \x01(\x04H\x00\x12\x12\n\x08\x62ool_val\x18\x04 \x01(\x08H\x00\x12\x13\n\tbytes_val\x18\x05 \x01(\x0cH\x00\x12\x17\n\tfloat_val\x18\x06 \x01(\x02\x42\x02\x18\x01H\x00\x12\x14\n\ndouble_val\x18\x0e \x01(\x01H\x00\x12*\n\x0b\x64\x65\x63imal_val\x18\x07 \x01(\x0b\x32\x0f.gnmi.Decimal64B\x02\x18\x01H\x00\x12)\n\x0cleaflist_val\x18\x08 \x01(\x0b\x32\x11.gnmi.ScalarArrayH\x00\x12\x27\n\x07\x61ny_val\x18\t \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12\x12\n\x08json_val\x18\n \x01(\x0cH\x00\x12\x17\n\rjson_ietf_val\x18\x0b \x01(\x0cH\x00\x12\x13\n\tascii_val\x18\x0c \x01(\tH\x00\x12\x15\n\x0bproto_bytes\x18\r \x01(\x0cH\x00\x42\x07\n\x05value'
    b'\"Y\n\x04Path\x12\x13\n\x07\x65lement\x18\x01 \x03(\tB\x02\x18\x01\x12\x0e\n\x06origin\x18\x02 \x01(\t\x12\x1c\n\x04\x65lem\x18\x03 \x03(\x0b\x32\x0e.gnmi.PathElem\x12\x0e\n\x06target\x18\x04 \x01(\t'
    b'\"j\n\x08PathElem\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x03key\x18\x02 \x03(\x0b\x32\x17.gnmi.PathElem.KeyEntry\x1a*\n\x08KeyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01'
    b'\"8\n\x05Value\x12\r\n\x05value\x18\x01 \x01(\x0c\x12\x1c\n\x04type\x18\x02 \x01(\x0e\x32\x0e.gnmi.Encoding:\x02\x18\x01'
    b'\"N\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01 \x01(\r\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\"\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x18\x01'
    b'\"2\n\tDecimal64\x12\x0e\n\x06\x64igits\x18\x01 \x01(\x03\x12\x11\n\tprecision\x18\x02 \x01(\r:\x02\x18\x01'
    b'\"0\n\x0bScalarArray\x12!\n\x07\x65lement\x18\x01 \x03(\x0b\x32\x10.gnmi.TypedValue'
    b'\"\x9d\x01\n\x10SubscribeRequest\x12+\n\tsubscribe\x18\x01 \x01(\x0b\x32\x16.gnmi.SubscriptionListH\x00\x12\x1a\n\x04poll\x18\x03 \x01(\x0b\x32\n.gnmi.PollH\x00\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.ExtensionB\t\n\x07requestJ\x04\x08\x04\x10\x05R\x07\x61liases'
    b'\"\x06\n\x04Poll'
    b'\"\xa8\x01\n\x11SubscribeResponse\x12$\n\x06update\x18\x01 \x01(\x0b\x32\x12.gnmi.NotificationH\x00\x12\x17\n\rsync_response\x18\x03 \x01(\x08H\x00\x12 \n\x05\x65rror\x18\x04 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01H\x00\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.ExtensionB\n\n\x08response'
    b'\"\xd5\x02\n\x10SubscriptionList\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12(\n\x0csubscription\x18\x02 \x03(\x0b\x32\x12.gnmi.Subscription\x12\x1d\n\x03qos\x18\x04 \x01(\x0b\x32\x10.gnmi.QOSMarking\x12)\n\x04mode\x18\x05 \x01(\x0e\x32\x1b.gnmi.SubscriptionList.Mode\x12\x19\n\x11\x61llow_aggregation\x18\x06 \x01(\x08\x12#\n\nuse_models\x18\x07 \x03(\x0b\x32\x0f.gnmi.ModelData\x12 \n\x08\x65ncoding\x18\x08 \x01(\x0e\x32\x0e.gnmi.Encoding\x12\x14\n\x0cupdates_only\x18\t \x01(\x08\"&\n\x04Mode\x12\n\n\x06STREAM\x10\x00\x12\x08\n\x04ONCE\x10\x01\x12\x08\n\x04POLL\x10\x02J\x04\x08\x03\x10\x04R\x0buse_aliases'
    b'\"\x9f\x01\n\x0cSubscription\x12\x18\n\x04path\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12$\n\x04mode\x18\x02 \x01(\x0e\x32\x16.gnmi.SubscriptionMode\x12\x17\n\x0fsample_interval\x18\x03 \x01(\x04\x12\x1a\n\x12suppress_redundant\x18\x04 \x01(\x08\x12\x1a\n\x12heartbeat_interval\x18\x05 \x01(\x04'
    b'\"\x1d\n\nQOSMarking\x12\x0f\n\x07marking\x18\x01 \x01(\r'
    b'\"\xce\x01\n\nSetRequest\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x1a\n\x06\x64\x65lete\x18\x02 \x03(\x0b\x32\n.gnmi.Path\x12\x1d\n\x07replace\x18\x03 \x03(\x0b\x32\x0c.gnmi.Update\x12\x1c\n\x06update\x18\x04 \x03(\x0b\x32\x0c.gnmi.Update\x12#\n\runion_replace\x18\x06 \x03(\x0b\x32\x0c.gnmi.Update\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.Extension'
    b'\"\xac\x01\n\x0bSetResponse\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12$\n\x08response\x18\x02 \x03(\x0b\x32\x12.gnmi.UpdateResult\x12 \n\x07message\x18\x03 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\x12&\n\textension\x18\x05 \x03(\x0b\x32\x13.gnmi_ext.Extension'
    b'\"\xdd\x01\n\x0cUpdateResult\x12\x15\n\ttimestamp\x18\x01 \x01(\x03\x42\x02\x18\x01\x12\x18\n\x04path\x18\x02 \x01(\x0b\x32\n.gnmi.Path\x12 \n\x07message\x18\x03 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12(\n\x02op\x18\x04 \x01(\x0e\x32\x1c.gnmi.UpdateResult.Operation\"P\n\tOperation\x12\x0b\n\x07INVALID\x10\x00\x12\n\n\x06\x44\x45LETE\x10\x01\x12\x0b\n\x07REPLACE\x10\x02\x12\n\n\x06UPDATE\x10\x03\x12\x11\n\rUNION_REPLACE\x10\x04'
    b'\"\x97\x02\n\nGetRequest\x12\x1a\n\x06prefix\x18\x01 \x01(\x0b\x32\n.gnmi.Path\x12\x18\n\x04path\x18\x02 \x03(\x0b\x32\n.gnmi.Path\x12\x27\n\x04type\x18\x03 \x01(\x0e\x32\x19.gnmi.GetRequest.DataType\x12 \n\x08\x65ncoding\x18\x05 \x01(\x0e\x32\x0e.gnmi.Encoding\x12#\n\nuse_models\x18\x06 \x03(\x0b\x32\x0f.gnmi.ModelData\x12&\n\textension\x18\x07 \x03(\x0b\x32\x13.gnmi_ext.Extension\";\n\x08\x44\x61taType\x12\x07\n\x03\x41LL\x10\x00\x12\n\n\x06\x43ONFIG\x10\x01\x12\t\n\x05STATE\x10\x02\x12\x0f\n\x0bOPERATIONAL\x10\x03'
    b'\"\x7f\n\x0bGetResponse\x12(\n\x0cnotification\x18\x01 \x03(\x0b\x32\x12.gnmi.Notification\x12\x1e\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x0b.gnmi.ErrorB\x02\x18\x01\x12&\n\textension\x18\x03 \x03(\x0b\x32\x13.gnmi_ext.Extension'
    b'\";\n\x11\x43\x61pabilityRequest\x12&\n\textension\x18\x01 \x03(\x0b\x32\x13.gnmi_ext.Extension'
    b'\"\xaa\x01\n\x12\x43\x61pabilityResponse\x12)\n\x10supported_models\x18\x01 \x03(\x0b\x32\x0f.gnmi.ModelData\x12+\n\x13supported_encodings\x18\x02 \x03(\x0e\x32\x0e.gnmi.Encoding\x12\x14\n\x0cgNMI_version\x18\x03 \x01(\t\x12&\n\textension\x18\x04 \x03(\x0b\x32\x13.gnmi_ext.Extension'
    b'\"@\n\tModelData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0corganization\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t'
    b'*D\n\x08\x45ncoding\x12\x08\n\x04JSON\x10\x00\x12\t\n\x05\x42YTES\x10\x01\x12\t\n\x05PROTO\x10\x02\x12\t\n\x05\x41SCII\x10\x03\x12\r\n\tJSON_IETF\x10\x04'
    b'*A\n\x10SubscriptionMode\x12\x12\n\x0eTARGET_DEFINED\x10\x00\x12\r\n\tON_CHANGE\x10\x01\x12\n\n\x06SAMPLE\x10\x02'
    b'\x32\xe3\x01\n\x04gNMI\x12\x41\n\x0c\x43\x61pabilities\x12\x17.gnmi.CapabilityRequest\x1a\x18.gnmi.CapabilityResponse\x12*\n\x03Get\x12\x10.gnmi.GetRequest\x1a\x11.gnmi.GetResponse\x12*\n\x03Set\x12\x10.gnmi.SetRequest\x1a\x11.gnmi.SetResponse\x12@\n\tSubscribe\x12\x16.gnmi.SubscribeRequest\x1a\x17.gnmi.SubscribeResponse(\x01\x30\x01'
    b':3\n\x0cgnmi_service\x12\x1c.google.protobuf.FileOptions\x18\xe9\x07 \x01(\t'
    b'BT\n\x15\x63om.github.gnmi.protoB\tGnmiProtoP\x01Z%github.com/openconfig/gnmi/proto/gnmi\xca>\x06\x30.10.0b\x06proto3'
)

_pool = _descriptor_pool.Default()
try:
    DESCRIPTOR = _pool.FindFileByName('gnmi.proto')
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

for _name, _ext_desc in DESCRIPTOR.extensions_by_name.items():
    globals()[_name] = _ext_desc
    globals()[_name.upper() + '_FIELD_NUMBER'] = _ext_desc.number
