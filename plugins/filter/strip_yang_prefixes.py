# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import re

from ansible.errors import AnsibleFilterError
from ansible.module_utils.common.text.converters import to_text

_PREFIX = re.compile(r'^[A-Za-z_][A-Za-z0-9_.-]*:(?=[^:/])')


def _merge(target, key, value):
    if isinstance(target.get(key), dict) and isinstance(value, dict):
        for k, v in value.items():
            _merge(target[key], k, v)
    else:
        target[key] = value


def _strip(data):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            name = _PREFIX.sub('', key) if isinstance(key, str) else key
            _merge(result, name, _strip(value))
        return result
    if isinstance(data, list):
        return [_strip(item) for item in data]
    return data


def strip_yang_prefixes(data):
    """Removes YANG module prefixes from the member names of a data tree."""
    if isinstance(data, (bytes, str)):
        try:
            data = json.loads(data)
        except ValueError as exc:
            raise AnsibleFilterError('strip_yang_prefixes expects a data tree or a JSON string: %s' % to_text(exc))
    return _strip(data)


class FilterModule(object):

    def filters(self):
        return {'strip_yang_prefixes': strip_yang_prefixes}
