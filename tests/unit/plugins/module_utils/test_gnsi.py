# (c) 2026 Nokia
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.nokia.openconfig.plugins.module_utils import gnsi


def test_authz_get_request():
    msg = gnsi.request_message('authz', 'Get', {})
    assert msg.DESCRIPTOR.name == 'GetRequest'
