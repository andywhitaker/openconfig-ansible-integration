# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from google.protobuf import json_format

from ansible_collections.nokia.openconfig.plugins.module_utils import gnmi
from ansible_collections.nokia.openconfig.plugins.module_utils import gnmi_ext
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2


def test_gnmi_service_version_is_pinned():
    options = gnmi_pb2.DESCRIPTOR.GetOptions()
    assert options.Extensions[gnmi_pb2.gnmi_service] == '0.10.0'


def test_builders_produce_valid_messages():
    get = gnmi.build_get_request(path=['openconfig:/interfaces'], type='CONFIG')
    get['extension'] = [gnmi_ext.depth(2)]
    message = json_format.ParseDict(get, gnmi_pb2.GetRequest())
    assert message.extension[0].depth.level == 2

    sets = gnmi.build_set_request(update=[{'path': '/a', 'value': 1}], delete=['/b'])
    sets['extension'] = [gnmi_ext.commit_request('c1', '30s')]
    message = json_format.ParseDict(sets, gnmi_pb2.SetRequest())
    assert message.extension[0].commit.commit.rollback_duration.seconds == 30

    sub = {
        'subscribe': gnmi.build_subscription_list(path=['/a'], sample_interval='1s', qos=0),
        'extension': [gnmi_ext.config_subscription_start()],
    }
    message = json_format.ParseDict(sub, gnmi_pb2.SubscribeRequest())
    assert message.subscribe.subscription[0].sample_interval == 10 ** 9
    assert message.extension[0].config_subscription.HasField('start')
