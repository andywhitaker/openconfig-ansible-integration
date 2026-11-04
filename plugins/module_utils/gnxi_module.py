# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Shared runner for the per-RPC gnoi_* and gnsi_* modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from ansible.module_utils.common.text.converters import to_text

from ansible_collections.nokia.openconfig.plugins.module_utils import gnmi
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_module import Rpc, to_json


def _encode(value, encoding):
    if encoding == 'path':
        return gnmi.encode_path(value)
    if encoding == 'paths':
        return [gnmi.encode_path(item) for item in value]
    if encoding == 'duration':
        return gnmi.parse_duration(value)
    return value


def build_request(module, fields=None, encode=None):
    """Builds the protobuf-JSON request dict: one field per typed option."""
    request = {}
    encode = encode or {}
    for param, field in (fields or {}).items():
        value = module.params.get(param)
        if value is None or value == '':
            continue
        try:
            request[field] = _encode(value, encode.get(param))
        except gnmi.GnmiError as exc:
            module.fail_json(msg='%s: %s' % (param, to_text(exc)))
    return request


def run(module, method, service, rpc, read_only, fields=None, encode=None, transport=None, stream=False):
    """Sends one RPC over the persistent connection and exits the module.

    Mutating RPCs are not sent in check mode. transport maps module params
    to keyword arguments of the connection method (local files, paths).
    """
    if module.check_mode and not read_only:
        module.exit_json(changed=False, skipped=True, msg='check mode: %s.%s not sent' % (service, rpc))

    kwargs = {'service': service, 'rpc': rpc}
    if stream:
        kwargs['stream'] = module.params['stream']
    else:
        request = build_request(module, fields, encode)
        if request:
            kwargs['request'] = request
    for param, name in (transport or {}).items():
        value = module.params.get(param)
        if value is not None:
            if param == 'local_path' and not os.path.isabs(value):
                # the persistent connection process has a different working directory
                value = os.path.abspath(value)
            kwargs[name] = value

    result = Rpc(module)(method, **kwargs)
    output = result.get('output')
    payload = {
        'changed': not read_only,
        'output': output if isinstance(output, str) else to_json(output),
    }
    for key in ('hash', 'local_path'):
        if key in result:
            payload[key] = result[key]
    module.exit_json(**payload)
