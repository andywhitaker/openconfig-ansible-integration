# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import base64
import hashlib
import json
import os
import sys

import pytest

from ansible.errors import AnsibleConnectionFailure, AnsibleError, AnsiblePluginRemovedError
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader

from ansible_collections.nokia.openconfig.plugins.connection import grpc as grpc_plugin
from ansible_collections.nokia.openconfig.plugins.module_utils import gnoi as gnoi_util
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2
from ansible_collections.nokia.openconfig.tests.unit.plugins import grpc_manifest
from ansible_collections.nokia.openconfig.tests.unit.plugins.connection.openconfig_mock_server import OpenConfigMockServer


@pytest.fixture
def server():
    with OpenConfigMockServer() as srv:
        yield srv


def make_connection(port, **options):
    conn = connection_loader.get('nokia.openconfig.grpc', PlayContext(), '/dev/null')
    direct = {
        'host': '127.0.0.1',
        'port': port,
        'remote_user': 'admin',
        'password': 'secret',
        'persistent_command_timeout': 10,
    }
    direct.update(options)
    conn.set_options(direct=direct)
    return conn


def test_dependencies_are_usable():
    assert grpc_plugin.dependency_error() is None


def test_dependency_error_missing_grpcio(monkeypatch):
    monkeypatch.setattr(grpc_plugin, 'HAS_GRPC', False)
    monkeypatch.setattr(grpc_plugin, 'GRPC_IMPORT_ERROR', ImportError("No module named 'grpc'"))
    error = grpc_plugin.dependency_error()
    assert "grpcio cannot be imported (No module named 'grpc')" in error
    assert sys.executable in error
    assert "-m pip install 'grpcio>=%s'" % grpc_plugin.GRPCIO_MIN in error


def test_dependency_error_old_protobuf(monkeypatch):
    monkeypatch.setattr(grpc_plugin, 'PROTOBUF_VERSION', '3.19.6')
    error = grpc_plugin.dependency_error()
    assert 'protobuf 3.19.6 is too old' in error
    assert "'protobuf>=%s'" % grpc_plugin.PROTOBUF_MIN in error


def test_dependency_error_missing_generated_modules(monkeypatch):
    name = 'ansible_collections.nokia.openconfig.plugins.module_utils.proto.gnmi_pb2'
    missing = ImportError("No module named '%s'" % name, name=name)
    monkeypatch.setattr(grpc_plugin, 'HAS_GNMI_PB2', False)
    monkeypatch.setattr(grpc_plugin, 'GNMI_PB2_IMPORT_ERROR', missing)
    assert 'run tools/build_openconfig_protos.sh' in grpc_plugin.dependency_error()


def test_dependency_error_incompatible_generated_modules(monkeypatch):
    monkeypatch.setattr(grpc_plugin, 'HAS_GNMI_PB2', False)
    monkeypatch.setattr(grpc_plugin, 'GNMI_PB2_IMPORT_ERROR', TypeError('Descriptors cannot be created directly'))
    error = grpc_plugin.dependency_error()
    assert error.startswith('The gNMI protobuf modules of nokia.openconfig cannot be imported with protobuf')
    assert error.endswith('Descriptors cannot be created directly')


def test_connection_reports_dependency_error(monkeypatch):
    monkeypatch.setattr(grpc_plugin, 'dependency_error', lambda: 'broken runtime')
    with pytest.raises(AnsibleError, match='broken runtime'):
        connection_loader.get('nokia.openconfig.grpc', PlayContext(), '/dev/null')


def test_gnmi_connection_was_removed():
    with pytest.raises(AnsiblePluginRemovedError, match='Use nokia.openconfig.grpc instead'):
        connection_loader.get('nokia.openconfig.gnmi', PlayContext(), '/dev/null')


@pytest.mark.parametrize('host', ['::1', '[::1]'])
def test_ipv6_host(host):
    try:
        srv = OpenConfigMockServer('::1')
    except RuntimeError:
        pytest.skip('IPv6 loopback is not available')
    with srv:
        conn = make_connection(srv.port, host=host)
        assert conn.gnmiCapabilities()['gNMIVersion'] == '0.10.0'
        assert conn._target == '[::1]:%d' % srv.port


def test_capabilities_selects_json_ietf_and_sends_credentials(server):
    conn = make_connection(server.port)
    caps = conn.gnmiCapabilities()
    assert caps['gNMIVersion'] == '0.10.0'
    assert conn._encoding == 'JSON_IETF'
    assert server.gnmi.metadata[0]['username'] == 'admin'
    assert server.gnmi.metadata[0]['password'] == 'secret'
    conn.close()


def test_configured_encoding_skips_capabilities(server):
    conn = make_connection(server.port, gnmi_encoding='json')
    conn._connect()
    assert conn._encoding == 'JSON'
    assert server.gnmi.requests == []
    conn.close()


def test_invalid_encoding(server):
    conn = make_connection(server.port, gnmi_encoding='PROTO')
    with pytest.raises(AnsibleConnectionFailure, match='Incompatible encoding'):
        conn._connect()


def test_connect_timeout():
    conn = make_connection(1, persistent_connect_timeout=1)
    with pytest.raises(AnsibleConnectionFailure, match='Failed to connect'):
        conn._connect()


def test_missing_certificate_file(server, tmp_path):
    conn = make_connection(server.port, root_certificates_file=str(tmp_path / 'missing.pem'))
    with pytest.raises(AnsibleConnectionFailure, match='root_certificates_file'):
        conn._connect()


def test_environment_and_channel_options_from_string(server, monkeypatch):
    monkeypatch.setenv('GRPC_TEST_REMOVE', '1')
    conn = make_connection(server.port,
                           grpc_environment='{"GRPC_TEST_SET": "x", "GRPC_TEST_REMOVE": 0}',
                           grpc_channel_options='{"grpc.max_receive_message_length": 1048576}')
    conn._connect()
    assert os.environ['GRPC_TEST_SET'] == 'x'
    assert 'GRPC_TEST_REMOVE' not in os.environ
    monkeypatch.delenv('GRPC_TEST_SET')
    conn.close()


def test_invalid_channel_options(server):
    conn = make_connection(server.port, grpc_channel_options='[1, 2]')
    with pytest.raises(AnsibleConnectionFailure, match='must be a dict'):
        conn._connect()


def test_get_with_depth_and_type(server):
    conn = make_connection(server.port)
    result = conn.gnmiGet(path=['openconfig:/interface[name=ethernet-1/1]'], type='config', depth=1)
    request = server.gnmi.requests[-1]
    assert request.type == gnmi_pb2.GetRequest.CONFIG
    assert request.path[0].origin == 'openconfig'
    assert request.extension[0].depth.level == 1
    assert result['output'] == {'interface': [{'name': 'ethernet-1/1', 'description': 'uplink', 'admin-state': 'enable'}]}
    assert result['extensions'] == [{'depth': {'level': 1}}]


def test_get_depth_zero_sends_no_extension(server):
    conn = make_connection(server.port)
    conn.gnmiGet(path=['/interface'], depth=0)
    request = server.gnmi.requests[-1]
    assert len(request.extension) == 0
    assert request.type == gnmi_pb2.GetRequest.ALL


def test_get_values_only(server):
    conn = make_connection(server.port)
    result = conn.gnmiGet(path=['/interface'], values_only=True)
    assert result['output'] == [{'description': 'uplink', 'admin-state': 'enable'}]


def test_get_invalid_path(server):
    conn = make_connection(server.port)
    with pytest.raises(AnsibleConnectionFailure, match='unbalanced'):
        conn.gnmiGet(path=['/interface[name=x'])


def test_set_with_commit_request(server):
    conn = make_connection(server.port)
    result = conn.gnmiSet(update=[{'path': '/system/name', 'value': {'host-name': 'r1'}}],
                          delete=['/system/banner'],
                          commit_id='c1', commit_request=True, rollback_duration='1m30s')
    request = server.gnmi.requests[-1]
    assert json.loads(request.update[0].val.json_ietf_val) == {'host-name': 'r1'}
    commit = request.extension[0].commit
    assert commit.id == 'c1'
    assert commit.commit.rollback_duration.seconds == 90
    assert [r['op'] for r in result['output']['response']] == ['DELETE', 'UPDATE']
    assert result['output']['response'][0]['path'] == 'system/banner'
    assert result['extensions'][0]['commit']['id'] == 'c1'


def test_set_commit_confirm_without_changes(server):
    conn = make_connection(server.port)
    conn.gnmiSet(commit_id='c1', commit_confirm=True)
    request = server.gnmi.requests[-1]
    assert request.extension[0].commit.HasField('confirm')
    assert len(request.update) == 0


def test_set_commit_requires_id(server):
    conn = make_connection(server.port)
    with pytest.raises(AnsibleConnectionFailure, match='commit_id is required'):
        conn.gnmiSet(commit_cancel=True)


def test_set_rpc_error_is_readable(server):
    conn = make_connection(server.port)
    with pytest.raises(AnsibleConnectionFailure, match='gRPC FAILED_PRECONDITION: commit reject in progress'):
        conn.gnmiSet(commit_id='reject', commit_cancel=True)


def test_set_dry_run_does_not_send(server):
    conn = make_connection(server.port, gnmi_encoding='JSON')
    result = conn.gnmiSet(replace=[{'path': '/system', 'value': 1, 'encoding': 'uint'}],
                          update=[{'path': '/a', 'value': 'x'}], dry_run=True)
    assert server.gnmi.requests == []
    request = result['request']
    assert request['replace'][0]['val'] == {'uint_val': '1'}
    assert base64.b64decode(request['update'][0]['val']['json_val']) == b'"x"'


def test_subscribe_once_merges(server):
    conn = make_connection(server.port)
    result = conn.gnmiSubscribe(path=['/interface[name=ethernet-1/1]/description'], mode='once')
    request = server.gnmi.requests[-1]
    assert request.subscribe.mode == gnmi_pb2.SubscriptionList.ONCE
    assert result['output'] == {'interface': [{'name': 'ethernet-1/1', 'description': 'uplink-0'}]}


def test_subscribe_poll(server):
    conn = make_connection(server.port)
    result = conn.gnmiSubscribe(path=['/interface'], mode='POLL')
    assert server.gnmi.requests[-1].HasField('poll')
    assert [u['values']['description'] for u in result['output']] == ['uplink-0', 'uplink-1']


def test_subscribe_stream_duration(server):
    conn = make_connection(server.port)
    result = conn.gnmiSubscribe(path=['/interface'], stream_mode='on_change', sample_interval='10s',
                                heartbeat_interval='1m', suppress_redundant=True, depth=2, duration=1)
    request = server.gnmi.requests[-1]
    sub = request.subscribe.subscription[0]
    assert sub.mode == gnmi_pb2.ON_CHANGE
    assert sub.sample_interval == 10 * 10 ** 9
    assert sub.heartbeat_interval == 60 * 10 ** 9
    assert sub.suppress_redundant
    assert request.extension[0].depth.level == 2
    assert len(result['output']) > 2
    assert result['output'][0]['prefix'] == '/interface[name=ethernet-1/1]'


def test_subscribe_config_subscription_until_done(server):
    conn = make_connection(server.port)
    result = conn.gnmiSubscribe(path=['/interface'], config_subscription=True)
    request = server.gnmi.requests[-1]
    assert request.extension[0].config_subscription.HasField('start')
    done = [e['config_subscription']['sync_done'] for e in result['extensions']]
    assert done[0] == {'server_commit_id': 'srv-1', 'done': True}
    assert done[-1] == {'commit_confirm_id': 'c1', 'server_commit_id': 'srv-1', 'done': True}
    assert len(result['output']) == 4


def test_subscribe_subscription_list(server):
    conn = make_connection(server.port)
    conn.gnmiSubscribe(subscription=[{'path': '/interface', 'stream_mode': 'sample', 'sample_interval': '5s'}],
                       duration=1)
    sub = server.gnmi.requests[-1].subscribe.subscription[0]
    assert sub.mode == gnmi_pb2.SAMPLE
    assert sub.sample_interval == 5 * 10 ** 9


def test_gnoi_time(server):
    conn = make_connection(server.port)
    result = conn.invokeGnoi('system', 'Time')
    assert result['output']['time'] == '1700000000000000000'
    call = server.registry.calls[-1]
    assert call['protocol'] == 'gnoi' and call['service'] == 'system' and call['rpc'] == 'Time'
    assert call['metadata']['username'] == 'admin'
    conn.close()


def test_gnoi_ping_stream(server):
    conn = make_connection(server.port)
    result = conn.invokeGnoi('system', 'Ping', request={'destination': '127.0.0.1', 'count': 1})
    assert len(result['output']) == 2
    assert result['output'][0]['received'] == 1
    conn.close()


def test_gnoi_file_stat_and_put(server, tmp_path):
    local = tmp_path / 'payload.bin'
    local.write_bytes(b'abc')
    conn = make_connection(server.port)
    stat = conn.invokeGnoi('file', 'Stat', request={'path': '/var/log/foo'})
    assert 'stats' in stat['output']
    conn.invokeGnoi('file', 'Put', local_path=str(local), remote_path='/tmp/payload.bin', permissions=644)
    puts = [c['request'] for c in server.registry.calls if c['rpc'] == 'Put']
    assert puts[0].open.remote_file == '/tmp/payload.bin'
    assert puts[0].open.permissions == 644
    assert puts[1].contents == b'abc'
    assert puts[2].hash.hash == hashlib.sha256(b'abc').digest()
    conn.close()


def test_gnoi_file_put_rejects_a_wrong_hash(server, tmp_path, monkeypatch):
    local = tmp_path / 'payload.bin'
    local.write_bytes(b'abc')
    hashed_twice = gnoi_util.types_pb2.HashType(method=gnoi_util.types_pb2.HashType.SHA256,
                                                hash=hashlib.sha256(hashlib.sha256(b'abc').digest()).digest())
    monkeypatch.setattr(gnoi_util, 'digest_hash', lambda digest: hashed_twice)
    conn = make_connection(server.port)
    with pytest.raises(AnsibleConnectionFailure, match='Hash mismatch'):
        conn.invokeGnoi('file', 'Put', local_path=str(local), remote_path='/tmp/payload.bin')
    conn.close()


def test_gnoi_file_get(server, tmp_path):
    conn = make_connection(server.port)
    dest = tmp_path / 'downloaded.bin'
    result = conn.invokeGnoi('file', 'Get', remote_path='/etc/motd', save_to=str(dest))
    assert dest.read_bytes() == b'mock-file-data'
    assert result['hash']['method'] == 'SHA256'
    conn.close()


def test_gnoi_factory_reset(server):
    conn = make_connection(server.port)
    result = conn.invokeGnoi('factory_reset', 'Start', request={'factoryOs': True})
    assert 'resetSuccess' in result['output']
    conn.close()


def test_gnsi_authz_get(server):
    conn = make_connection(server.port)
    result = conn.invokeGnsi('authz', 'Get')
    assert result['output']['version'] == 'mock-authz-1'
    conn.close()


def test_gnsi_certz_get_profile_list(server):
    conn = make_connection(server.port)
    result = conn.invokeGnsi('certz', 'GetProfileList')
    assert result['output']['sslProfileIds'] == ['default']
    conn.close()


def test_gnsi_pathz_get(server):
    conn = make_connection(server.port)
    result = conn.invokeGnsi('pathz', 'Get', request={'policyInstance': 'POLICY_INSTANCE_ACTIVE'})
    assert result['output']['version'] == 'mock-pathz-1'
    conn.close()


def test_gnsi_credentialz_get_public_keys(server):
    conn = make_connection(server.port)
    result = conn.invokeGnsi('credentialz', 'GetPublicKeys')
    assert result['output'] == {}
    conn.close()


def test_gnsi_certz_can_generate_csr(server):
    conn = make_connection(server.port)
    result = conn.invokeGnsi('certz', 'CanGenerateCSR', request={'params': {'country': 'US'}})
    assert result['output']['canGenerate'] is True
    conn.close()


def test_gnsi_rotate_collects_every_server_message(server):
    conn = make_connection(server.port)
    stream = [{'uploadRequest': {'version': 'v1', 'policy': '{}'}}, {'finalizeRotation': {}}]
    result = conn.invokeGnsi('authz', 'Rotate', stream=stream)
    assert result['output'] == [{'uploadResponse': {}}, {}]
    sent = [c['request'] for c in server.registry.calls if c['rpc'] == 'Rotate']
    assert [m.WhichOneof('rotate_request') for m in sent] == ['upload_request', 'finalize_rotation']
    conn.close()


def _manifest_call_kwargs(entry, tmp_path):
    local = tmp_path / 'payload.bin'
    local.write_bytes(b'abc')
    key = (entry['service'], entry['rpc'])
    if key == ('file', 'Put'):
        return {'local_path': str(local), 'remote_path': '/tmp/payload.bin'}
    if key in (('system', 'SetPackage'), ('os', 'Install')):
        return {'local_path': str(local)}
    if key == ('file', 'Get'):
        return {'remote_path': '/etc/motd'}
    if entry.get('stream_message'):
        return {'stream': [{}]}
    return {}


@pytest.mark.parametrize('entry', grpc_manifest.entries(), ids=[e['module'] for e in grpc_manifest.entries()])
def test_every_manifest_rpc_reaches_the_mock(server, tmp_path, entry):
    conn = make_connection(server.port)
    method = conn.invokeGnoi if entry['protocol'] == 'gnoi' else conn.invokeGnsi
    result = method(entry['service'], entry['rpc'], **_manifest_call_kwargs(entry, tmp_path))
    assert 'output' in result
    if entry['pattern'] in ('server_streaming', 'bidi_streaming'):
        assert isinstance(result['output'], list)
    call = server.registry.calls[-1]
    assert (call['protocol'], call['service'], call['rpc']) == (entry['protocol'], entry['service'], entry['rpc'])
    conn.close()
