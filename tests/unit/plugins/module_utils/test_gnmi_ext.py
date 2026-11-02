# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.nokia.openconfig.plugins.module_utils import gnmi_ext
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi import GnmiError


@pytest.mark.parametrize('level, expected', [
    (None, None),
    (0, None),
    (1, {'depth': {'level': 1}}),
    ('3', {'depth': {'level': 3}}),
])
def test_depth(level, expected):
    assert gnmi_ext.depth(level) == expected


def test_depth_negative():
    with pytest.raises(GnmiError):
        gnmi_ext.depth(-1)


def test_commit_builders():
    assert gnmi_ext.commit_request('c1') == {'commit': {'id': 'c1', 'commit': {}}}
    assert gnmi_ext.commit_request('c1', '1m30s') == {'commit': {'id': 'c1', 'commit': {'rollback_duration': '90s'}}}
    assert gnmi_ext.commit_confirm('c1') == {'commit': {'id': 'c1', 'confirm': {}}}
    assert gnmi_ext.commit_cancel('c1') == {'commit': {'id': 'c1', 'cancel': {}}}
    assert gnmi_ext.set_rollback_duration('c1', '2m') == {
        'commit': {'id': 'c1', 'set_rollback_duration': {'rollback_duration': '120s'}}}


@pytest.mark.parametrize('kwargs, expected', [
    ({}, None),
    ({'commit_id': 'c', 'commit_request_': True, 'rollback_duration': '30s'},
     {'commit': {'id': 'c', 'commit': {'rollback_duration': '30s'}}}),
    ({'commit_id': 'c', 'commit_confirm_': True}, {'commit': {'id': 'c', 'confirm': {}}}),
    ({'commit_id': 'c', 'commit_cancel_': True}, {'commit': {'id': 'c', 'cancel': {}}}),
    ({'commit_id': 'c', 'rollback_duration': '10s'},
     {'commit': {'id': 'c', 'set_rollback_duration': {'rollback_duration': '10s'}}}),
])
def test_commit_extension(kwargs, expected):
    assert gnmi_ext.commit_extension(**kwargs) == expected


@pytest.mark.parametrize('kwargs', [
    {'commit_request_': True},
    {'rollback_duration': '10s'},
    {'commit_id': 'c'},
    {'commit_id': 'c', 'commit_request_': True, 'commit_confirm_': True},
    {'commit_id': 'c', 'commit_confirm_': True, 'commit_cancel_': True},
    {'commit_id': 'c', 'commit_request_': True, 'rollback_duration': 'soon'},
])
def test_commit_extension_invalid(kwargs):
    with pytest.raises(GnmiError):
        gnmi_ext.commit_extension(**kwargs)


def test_config_subscription_start():
    assert gnmi_ext.config_subscription_start() == {'config_subscription': {'start': {}}}


def test_parse_extensions_and_sync_done():
    raw = [
        {'depth': {'level': 2}},
        {'configSubscription': {'syncDone': {'commitConfirmId': 'c1', 'serverCommitId': 's1', 'done': True}}},
    ]
    parsed = gnmi_ext.parse_extensions(raw)
    assert parsed[1] == {'config_subscription': {'sync_done': {
        'commit_confirm_id': 'c1', 'server_commit_id': 's1', 'done': True}}}
    assert gnmi_ext.sync_done(raw) == {'commit_confirm_id': 'c1', 'server_commit_id': 's1', 'done': True}
    assert gnmi_ext.sync_done([{'depth': {'level': 1}}]) is None
    assert gnmi_ext.parse_extensions(None) == []
