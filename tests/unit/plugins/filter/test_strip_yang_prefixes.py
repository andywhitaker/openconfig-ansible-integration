# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

import pytest

from ansible.errors import AnsibleFilterError

from ansible_collections.nokia.openconfig.plugins.filter.strip_yang_prefixes import strip_yang_prefixes


def test_strips_member_names_but_not_values():
    data = {'openconfig-interfaces:interfaces': {'interface': [
        {'name': 'Ethernet1', 'openconfig-if-ethernet:ethernet': {'state': {
            'port-speed': 'openconfig-if-ethernet:SPEED_10GB'}}},
    ]}}
    assert strip_yang_prefixes(data) == {'interfaces': {'interface': [
        {'name': 'Ethernet1', 'ethernet': {'state': {'port-speed': 'openconfig-if-ethernet:SPEED_10GB'}}},
    ]}}


def test_accepts_module_output_string():
    output = json.dumps({'srl_nokia-system:system': {'name': {'host-name': 'leaf1'}}})
    assert strip_yang_prefixes(output) == {'system': {'name': {'host-name': 'leaf1'}}}


def test_merges_containers_that_differ_in_prefix_only():
    data = {'lldp': {'config': {'enabled': True}}, 'openconfig-lldp:lldp': {'state': {'enabled': True}}}
    assert strip_yang_prefixes(data) == {'lldp': {'config': {'enabled': True}, 'state': {'enabled': True}}}


def test_keeps_names_that_are_not_prefixed():
    data = {'a': [1, {'b:': 2}], 'ipv6:/x': 3}
    assert strip_yang_prefixes(data) == data


def test_rejects_invalid_json():
    with pytest.raises(AnsibleFilterError):
        strip_yang_prefixes('not json')
