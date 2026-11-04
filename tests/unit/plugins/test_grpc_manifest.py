# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Keeps modules, connection tables and the mock server in line with tools/nokia_grpc_modules.yaml."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

import pytest
import yaml

from ansible_collections.nokia.openconfig.plugins.module_utils import gnoi
from ansible_collections.nokia.openconfig.plugins.module_utils import gnsi
from ansible_collections.nokia.openconfig.tests.unit.plugins import grpc_manifest
from ansible_collections.nokia.openconfig.tests.unit.plugins.connection.openconfig_mock_server import OpenConfigMockServer

MODULE_DIR = os.path.join(grpc_manifest.ROOT, 'plugins', 'modules')


def test_generated_modules_are_current():
    gen = grpc_manifest.generator()
    rendered = gen.render_all()
    outdated = []
    for name, content in rendered.items():
        path = os.path.join(MODULE_DIR, name)
        if not os.path.exists(path) or open(path).read() != content:
            outdated.append(name)
    assert outdated == [], 'run python tools/generate_grpc_modules.py'
    assert gen.stale_modules(rendered) == []


@pytest.mark.parametrize('name, rpc, error', [
    ('gnoi_system_clock', 'Time', 'must be named gnoi_system_time'),
    ('gnoi_system_time', 'Time', None),
])
def test_manifest_enforces_naming(name, rpc, error):
    gen = grpc_manifest.generator()
    entry = dict(module=name, protocol='gnoi', service='system', rpc=rpc, pattern='unary',
                 platforms=['srl'], validation=['unit'], read_only=True,
                 short_description='x', description='x', options={}, examples='')
    if error:
        with pytest.raises(gen.ManifestError, match=error):
            gen.validate_entry(entry)
    else:
        gen.validate_entry(entry)


@pytest.mark.parametrize('option', ['message', 'syslog_facility', 'stream'])
def test_manifest_rejects_reserved_option_names(option):
    gen = grpc_manifest.generator()
    entry = dict(module='gnoi_system_time', protocol='gnoi', service='system', rpc='Time', pattern='unary',
                 platforms=['srl'], validation=['unit'], read_only=True, short_description='x',
                 description='x', options={option: dict(description='x', type='str', field=option)}, examples='')
    with pytest.raises(gen.ManifestError, match='%s is reserved' % option):
        gen.validate_entry(entry)


def test_long_documentation_items_are_folded():
    gen = grpc_manifest.generator()
    text = ' '.join(['word'] * 60) + ' with C(markup) and O(stream).'
    lines = gen.list_item('  ', text)
    assert len(lines) > 1
    assert all(len(line) <= gen.LINE_WIDTH for line in lines)
    assert yaml.safe_load('\n'.join(lines)) == [text]


def test_documentation_items_that_need_quotes_stay_valid():
    gen = grpc_manifest.generator()
    text = 'Paths such as cf3: and words: that look like YAML keys.'
    assert yaml.safe_load('\n'.join(gen.list_item('  ', text))) == [text]


def test_snake_case_keeps_acronyms_together():
    gen = grpc_manifest.generator()
    assert gen.snake('ClearBGPNeighbor') == 'clear_bgp_neighbor'
    assert gen.snake('CanGenerateCSR') == 'can_generate_csr'
    assert gen.snake('RotateAccountCredentials') == 'rotate_account_credentials'


@pytest.mark.parametrize('protocol, table', [('gnoi', gnoi.SERVICES), ('gnsi', gnsi.SERVICES)])
def test_connection_services_match_manifest(protocol, table):
    assert set(table) == grpc_manifest.services(protocol)


def test_mock_server_implements_exactly_the_manifest():
    with OpenConfigMockServer() as server:
        for protocol in ('gnoi', 'gnsi'):
            servicers = getattr(server, protocol)
            assert set(servicers) == grpc_manifest.services(protocol)
            for service, servicer in servicers.items():
                implemented = {n for n in type(servicer).__dict__ if n[:1].isupper()}
                assert implemented == grpc_manifest.rpcs(protocol, service), '%s.%s' % (protocol, service)


def test_streaming_tables_match_manifest():
    expected = {
        'unary': (False, False),
        'server_streaming': (True, False),
        'client_streaming': (False, True),
        'bidi_streaming': (True, True),
    }
    for entry in grpc_manifest.entries():
        key = (entry['service'], entry['rpc'])
        if entry['protocol'] == 'gnoi':
            actual = (key in gnoi.SERVER_STREAMING, key in gnoi.CLIENT_STREAMING)
            assert actual == expected[entry['pattern']], entry['module']
        else:
            assert (key in gnsi.BIDI_STREAMING) == (entry['pattern'] == 'bidi_streaming'), entry['module']
            assert gnsi.STREAM_REQUEST.get(key) == entry.get('stream_message'), entry['module']

    listed = {(e['service'], e['rpc']) for e in grpc_manifest.entries()}
    assert gnoi.SERVER_STREAMING | gnoi.CLIENT_STREAMING <= listed
    assert set(gnsi.BIDI_STREAMING) <= listed
