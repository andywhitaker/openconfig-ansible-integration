# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import importlib
import json

import pytest

from ansible_collections.nokia.openconfig.tests.unit.plugins import grpc_manifest

ENTRIES = grpc_manifest.entries()
METHODS = {'gnoi': 'invokeGnoi', 'gnsi': 'invokeGnsi'}


def load(name):
    return importlib.import_module('ansible_collections.nokia.openconfig.plugins.modules.' + name)


def sample(spec):
    if spec.get('choices'):
        return spec['choices'][0]
    encoding = spec.get('encode')
    if encoding == 'duration':
        return '1s'
    if encoding == 'path':
        return '/components/component[name=A]'
    if encoding == 'paths':
        return ['/components/component[name=A]']
    return {
        'str': 'x',
        'int': 1,
        'bool': True,
        'dict': {'k': 'v'},
        'path': '/tmp/x',
        'raw': '1s',
        'list': [{'k': 'v'}] if spec.get('elements') == 'dict' else ['x'],
    }[spec['type']]


def required_args(entry):
    options = grpc_manifest.generator().doc_options(entry)
    return {name: sample(spec) for name, spec in options.items() if spec.get('required')}


@pytest.mark.parametrize('entry', ENTRIES, ids=[e['module'] for e in ENTRIES])
def test_module_sends_its_rpc(entry, connection, run_module):
    method = METHODS[entry['protocol']]
    connection.responses[method] = {'output': {'ok': True}}
    result = run_module(load(entry['module']).main, required_args(entry))
    assert connection.calls[0][0] == method
    kwargs = connection.calls[0][1]
    assert (kwargs['service'], kwargs['rpc']) == (entry['service'], entry['rpc'])
    assert result['changed'] is (not entry['read_only'])
    assert json.loads(result['output']) == {'ok': True}


@pytest.mark.parametrize('entry', ENTRIES, ids=[e['module'] for e in ENTRIES])
def test_module_check_mode(entry, connection, run_module):
    connection.responses[METHODS[entry['protocol']]] = {'output': {}}
    result = run_module(load(entry['module']).main, required_args(entry), check_mode=True)
    if entry['read_only']:
        assert len(connection.calls) == 1
        assert result['changed'] is False
    else:
        assert connection.calls == []
        assert result['skipped'] is True


def test_ping_maps_options_and_durations(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': [{'sent': 1, 'received': 1}]}
    run_module(load('gnoi_system_ping').main, {
        'destination': '192.0.2.1', 'count': 3, 'interval': '200ms', 'wait': 2,
        'do_not_fragment': True, 'network_instance': 'mgmt',
    })
    assert connection.calls[0][1]['request'] == {
        'destination': '192.0.2.1', 'count': 3, 'interval': 200000000, 'wait': 2000000000,
        'doNotFragment': True, 'networkInstance': 'mgmt',
    }


def test_reboot_encodes_subcomponent_paths(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': {}}
    run_module(load('gnoi_system_reboot').main, {'method': 'COLD', 'subcomponents': ['/components/component[name=A]']})
    assert connection.calls[0][1]['request'] == {
        'method': 'COLD',
        'subcomponents': [{'elem': [{'name': 'components'}, {'name': 'component', 'key': {'name': 'A'}}]}],
    }


def test_invalid_path_fails_with_option_name(connection, run_module):
    result = run_module(load('gnoi_healthz_get').main, {'path': '/platform/control[slot=A'})
    assert result['failed'] is True
    assert result['msg'].startswith('path: ')
    assert connection.calls == []


def test_invalid_duration_fails(connection, run_module):
    result = run_module(load('gnoi_system_ping').main, {'destination': '192.0.2.1', 'interval': 'soon'})
    assert result['failed'] is True
    assert result['msg'].startswith('interval: ')


def test_file_get_passes_transport_and_returns_hash(connection, run_module):
    connection.responses['invokeGnoi'] = {
        'output': [{'contents': 'YQ=='}], 'hash': {'method': 'SHA256'}, 'local_path': '/tmp/out',
    }
    result = run_module(load('gnoi_file_get').main, {'remote_path': '/etc/hostname', 'local_path': '/tmp/out'})
    kwargs = connection.calls[0][1]
    assert kwargs == {'service': 'file', 'rpc': 'Get', 'remote_path': '/etc/hostname', 'save_to': '/tmp/out'}
    assert result['hash'] == {'method': 'SHA256'}
    assert result['local_path'] == '/tmp/out'


def test_file_put_passes_transport(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': {}}
    run_module(load('gnoi_file_put').main, {'local_path': '/tmp/in', 'remote_path': '/tmp/r', 'permissions': 644})
    kwargs = connection.calls[0][1]
    assert kwargs == {'service': 'file', 'rpc': 'Put', 'local_path': '/tmp/in', 'remote_path': '/tmp/r',
                      'permissions': 644}


def test_relative_local_paths_are_made_absolute(connection, run_module, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    connection.responses['invokeGnoi'] = {'output': {}}
    run_module(load('gnoi_file_put').main, {'local_path': './in.txt', 'remote_path': 'cf3:/in.txt'})
    run_module(load('gnoi_file_get').main, {'remote_path': 'cf3:/config.cfg', 'local_path': 'out.cfg'})
    assert connection.calls[0][1]['local_path'] == str(tmp_path / 'in.txt')
    assert connection.calls[1][1]['save_to'] == str(tmp_path / 'out.cfg')


def test_file_stat_and_remove_use_request_fields(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': {}}
    run_module(load('gnoi_file_stat').main, {'remote_path': 'cf3:/'})
    run_module(load('gnoi_file_remove').main, {'remote_path': '/tmp/r'})
    assert connection.calls[0][1]['request'] == {'path': 'cf3:/'}
    assert connection.calls[1][1]['request'] == {'remoteFile': '/tmp/r'}


def test_os_install_streams_local_file(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': [{'validated': {}}]}
    run_module(load('gnoi_os_install').main, {'local_path': '/tmp/os.bin', 'os_version': '25.10.1'})
    kwargs = connection.calls[0][1]
    assert kwargs == {'service': 'os', 'rpc': 'Install', 'local_path': '/tmp/os.bin', 'os_version': '25.10.1'}


def test_os_activate_maps_fields(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': {}}
    run_module(load('gnoi_os_activate').main, {'os_version': '25.10.1', 'no_reboot': True})
    assert connection.calls[0][1]['request'] == {'version': '25.10.1', 'noReboot': True}


def test_factory_reset_maps_fields(connection, run_module):
    connection.responses['invokeGnoi'] = {'output': {'resetSuccess': {}}}
    result = run_module(load('gnoi_factory_reset_start').main, {'factory_os': True})
    assert connection.calls[0][1]['request'] == {'factoryOs': True}
    assert result['changed'] is True


def test_gnsi_rotate_sends_stream_only(connection, run_module):
    stream = [{'uploadRequest': {'version': 'v1', 'policy': '{}'}}, {'finalizeRotation': {}}]
    connection.responses['invokeGnsi'] = {'output': [{'uploadResponse': {}}]}
    run_module(load('gnsi_authz_rotate').main, {'stream': stream})
    assert connection.calls[0] == ('invokeGnsi', {'service': 'authz', 'rpc': 'Rotate', 'stream': stream})


def test_pathz_get_defaults_to_active_policy(connection, run_module):
    connection.responses['invokeGnsi'] = {'output': {}}
    run_module(load('gnsi_pathz_get').main, {})
    assert connection.calls[0][1]['request'] == {'policyInstance': 'POLICY_INSTANCE_ACTIVE'}


def test_pathz_probe_encodes_gnmi_path(connection, run_module):
    connection.responses['invokeGnsi'] = {'output': {'action': 'ACTION_PERMIT'}}
    run_module(load('gnsi_pathz_probe').main, {'user': 'admin', 'path': '/system/name'})
    assert connection.calls[0][1]['request'] == {
        'user': 'admin', 'path': {'elem': [{'name': 'system'}, {'name': 'name'}]},
        'mode': 'MODE_READ', 'policyInstance': 'POLICY_INSTANCE_ACTIVE',
    }
