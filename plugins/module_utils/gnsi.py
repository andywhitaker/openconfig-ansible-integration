# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Helpers for gNSI RPCs on the nokia.openconfig.grpc connection."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import traceback

GNSI_PROTO_IMPORT_ERROR = None

try:
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import authz_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import authz_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import certz_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import certz_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import credentialz_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import credentialz_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import pathz_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnsi import pathz_pb2_grpc
except ImportError:
    GNSI_PROTO_IMPORT_ERROR = traceback.format_exc()
    authz_pb2 = None
    authz_pb2_grpc = None
    certz_pb2 = None
    certz_pb2_grpc = None
    credentialz_pb2 = None
    credentialz_pb2_grpc = None
    pathz_pb2 = None
    pathz_pb2_grpc = None

HAS_GNSI_PROTOS = GNSI_PROTO_IMPORT_ERROR is None

BIDI_STREAMING = {
    ('authz', 'Rotate'),
    ('certz', 'Rotate'),
    ('pathz', 'Rotate'),
    ('credentialz', 'RotateAccountCredentials'),
    ('credentialz', 'RotateHostParameters'),
}

STREAM_REQUEST = {
    ('authz', 'Rotate'): 'RotateAuthzRequest',
    ('certz', 'Rotate'): 'RotateCertificateRequest',
    ('pathz', 'Rotate'): 'RotateRequest',
    ('credentialz', 'RotateAccountCredentials'): 'RotateAccountCredentialsRequest',
    ('credentialz', 'RotateHostParameters'): 'RotateHostParametersRequest',
}

if HAS_GNSI_PROTOS:
    SERVICES = {
        'authz': (authz_pb2, authz_pb2_grpc.AuthzStub),
        'certz': (certz_pb2, certz_pb2_grpc.CertzStub),
        'pathz': (pathz_pb2, pathz_pb2_grpc.PathzStub),
        'credentialz': (credentialz_pb2, credentialz_pb2_grpc.CredentialzStub),
    }
else:
    SERVICES = {}


class GnsiError(Exception):
    pass


def _require_gnsi_protos():
    if not HAS_GNSI_PROTOS:
        raise GnsiError(
            "gNSI protobuf modules are missing from nokia.openconfig. Install a released "
            "collection, or run tools/build_openconfig_protos.sh in a source checkout."
        )


def request_message(service, rpc, data=None):
    _require_gnsi_protos()
    if service not in SERVICES:
        raise GnsiError("Unknown gNSI service %r" % service)
    pb2 = SERVICES[service][0]
    name = rpc + 'Request'
    if not hasattr(pb2, name):
        raise GnsiError("Unknown gNSI RPC %r for service %r" % (rpc, service))
    message = getattr(pb2, name)()
    if data:
        from google.protobuf import json_format
        json_format.ParseDict(data, message)
    return message


def stream_messages(service, rpc, items):
    _require_gnsi_protos()
    if not items:
        raise GnsiError("stream requires at least one message")
    key = (service, rpc)
    if key not in STREAM_REQUEST:
        raise GnsiError("RPC %r on %r is not a client stream" % (rpc, service))
    pb2 = SERVICES[service][0]
    cls = getattr(pb2, STREAM_REQUEST[key])
    from google.protobuf import json_format
    for item in items:
        message = cls()
        json_format.ParseDict(item, message)
        yield message
