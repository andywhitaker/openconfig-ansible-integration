# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Helpers for gNOI RPCs on the nokia.openconfig.grpc connection."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import hashlib
import os
import traceback

from ansible.module_utils.common.text.converters import to_text

GNOI_PROTO_IMPORT_ERROR = None

try:
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import bgp_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import bgp_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import factory_reset_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import factory_reset_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import file_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import file_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import healthz_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import healthz_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import os_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import os_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import system_pb2
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import system_pb2_grpc
    from ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnoi import types_pb2
except ImportError:
    GNOI_PROTO_IMPORT_ERROR = traceback.format_exc()
    bgp_pb2 = None
    bgp_pb2_grpc = None
    factory_reset_pb2 = None
    factory_reset_pb2_grpc = None
    file_pb2 = None
    file_pb2_grpc = None
    healthz_pb2 = None
    healthz_pb2_grpc = None
    os_pb2 = None
    os_pb2_grpc = None
    system_pb2 = None
    system_pb2_grpc = None
    types_pb2 = None

HAS_GNOI_PROTOS = GNOI_PROTO_IMPORT_ERROR is None

CHUNK_SIZE = 64 * 1024

# RPCs that return a stream of response messages.
SERVER_STREAMING = {
    ('system', 'Ping'),
    ('system', 'Traceroute'),
    ('file', 'Get'),
    ('healthz', 'Artifact'),
    ('os', 'Install'),
}

# Client-streaming RPCs (single final response unless noted).
CLIENT_STREAMING = {
    ('system', 'SetPackage'),
    ('file', 'Put'),
    ('os', 'Install'),
}

if HAS_GNOI_PROTOS:
    SERVICES = {
        'system': (system_pb2, system_pb2_grpc.SystemStub),
        'file': (file_pb2, file_pb2_grpc.FileStub),
        'os': (os_pb2, os_pb2_grpc.OSStub),
        'factory_reset': (factory_reset_pb2, factory_reset_pb2_grpc.FactoryResetStub),
        'healthz': (healthz_pb2, healthz_pb2_grpc.HealthzStub),
        'bgp': (bgp_pb2, bgp_pb2_grpc.BGPStub),
    }
else:
    SERVICES = {}


class GnoiError(Exception):
    pass


def _require_gnoi_protos():
    if not HAS_GNOI_PROTOS:
        raise GnoiError(
            "gNOI protobuf modules are missing from nokia.openconfig. Install a released "
            "collection, or run tools/build_openconfig_protos.sh in a source checkout."
        )


def sha256_hash(data):
    _require_gnoi_protos()
    return digest_hash(hashlib.sha256(data))


def digest_hash(digest):
    """HashType for a finished hashlib.sha256 object."""
    _require_gnoi_protos()
    return types_pb2.HashType(method=types_pb2.HashType.SHA256, hash=digest.digest())


def request_message(service, rpc, data=None):
    """Builds a protobuf request from a dict (protobuf JSON field names)."""
    _require_gnoi_protos()
    if service not in SERVICES:
        raise GnoiError("Unknown gNOI service %r" % service)
    pb2 = SERVICES[service][0]
    name = rpc + 'Request'
    if not hasattr(pb2, name):
        raise GnoiError("Unknown gNOI RPC %r for service %r" % (rpc, service))
    message = getattr(pb2, name)()
    if data:
        from google.protobuf import json_format
        json_format.ParseDict(data, message)
    return message


def read_file_chunks(path):
    path = to_text(path)
    if not os.path.isfile(path):
        raise GnoiError("Local file %r does not exist" % path)
    with open(path, 'rb') as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            yield chunk


def file_put_requests(remote_file, local_path, permissions=None):
    """Yields PutRequest messages for gNOI File.Put."""
    _require_gnoi_protos()
    details = file_pb2.PutRequest.Details(remote_file=remote_file)
    if permissions is not None:
        details.permissions = int(permissions)
    yield file_pb2.PutRequest(open=details)
    digest = hashlib.sha256()
    for chunk in read_file_chunks(local_path):
        digest.update(chunk)
        yield file_pb2.PutRequest(contents=chunk)
    yield file_pb2.PutRequest(hash=digest_hash(digest))


def set_package_requests(local_path, package_name=None, version=None, activate=False):
    """Yields SetPackageRequest messages for gNOI System.SetPackage."""
    _require_gnoi_protos()
    path = to_text(local_path)
    filename = package_name or os.path.basename(path)
    package = system_pb2.Package(filename=filename)
    if version:
        package.version = version
    if activate:
        package.activate = True
    yield system_pb2.SetPackageRequest(package=package)
    digest = hashlib.sha256()
    for chunk in read_file_chunks(path):
        digest.update(chunk)
        yield system_pb2.SetPackageRequest(contents=chunk)
    yield system_pb2.SetPackageRequest(hash=digest_hash(digest))


def os_install_requests(local_path, version='', standby_supervisor=False):
    """Yields InstallRequest messages for gNOI OS.Install."""
    _require_gnoi_protos()
    yield os_pb2.InstallRequest(transfer_request=os_pb2.TransferRequest(
        version=version or '',
        standby_supervisor=standby_supervisor,
    ))
    for chunk in read_file_chunks(local_path):
        yield os_pb2.InstallRequest(transfer_content=chunk)
    yield os_pb2.InstallRequest(transfer_end=os_pb2.TransferEnd())


def normalize_l3protocol(value):
    if value is None:
        return None
    upper = str(value).upper()
    if upper in ('IPV4', 'IPV6', 'UNSPECIFIED'):
        return upper
    raise GnoiError("Invalid l3protocol %r" % value)
