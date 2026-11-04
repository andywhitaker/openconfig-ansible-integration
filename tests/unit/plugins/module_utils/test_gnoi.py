# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import hashlib

import pytest

from ansible_collections.nokia.openconfig.plugins.module_utils import gnoi


def test_file_put_requests(tmp_path):
    local = tmp_path / 'data.bin'
    local.write_bytes(b'hello')
    messages = list(gnoi.file_put_requests('/tmp/remote', str(local), permissions=644))
    assert messages[0].WhichOneof('request') == 'open'
    assert messages[0].open.remote_file == '/tmp/remote'
    assert messages[0].open.permissions == 644
    assert messages[1].WhichOneof('request') == 'contents'
    assert messages[1].contents == b'hello'
    assert messages[2].WhichOneof('request') == 'hash'
    assert messages[2].hash.hash == hashlib.sha256(b'hello').digest()


def test_set_package_requests_hash_the_file(tmp_path):
    local = tmp_path / 'image.bin'
    local.write_bytes(b'image')
    messages = list(gnoi.set_package_requests(str(local), version='1.0'))
    assert messages[0].package.filename == 'image.bin'
    assert messages[-1].hash.hash == hashlib.sha256(b'image').digest()


def test_request_message_time():
    msg = gnoi.request_message('system', 'Time', {})
    assert msg.DESCRIPTOR.name == 'TimeRequest'


def test_normalize_l3protocol():
    assert gnoi.normalize_l3protocol('ipv4') == 'IPV4'
    with pytest.raises(gnoi.GnoiError):
        gnoi.normalize_l3protocol('mpls')
