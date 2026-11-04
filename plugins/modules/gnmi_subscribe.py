#!/usr/bin/python
# (c) 2020-2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: gnmi_subscribe
author:
  - "Hans Thienpondt (@HansThienpondt)"
  - "Sven Wisotzky (@wisotzky)"
short_description: Retrieve configuration and state using gNMI Subscribe
description:
  - Sends a gNMI C(SubscribeRequest) and collects the responses.
  - Option names are the C(SubscriptionList) and C(Subscription) fields in
    snake_case, and the values follow the gNMI 0.10.0 protobuf messages. Enum
    values are case-insensitive.
  - C(ONCE) returns the merged object tree, like M(nokia.openconfig.gnmi_get).
  - C(STREAM) collects notifications until O(duration) expires. C(POLL) sends
    one Poll after the initial synchronization and returns both rounds.
version_added: 1.0.0
options:
  path:
    description:
      - Paths to subscribe to, C(Subscription.path). Every path uses the same
        O(stream_mode), O(sample_interval), O(heartbeat_interval) and
        O(suppress_redundant).
      - Mutually exclusive with O(subscription).
    type: list
    elements: str
    version_added: 2.0.0
  subscription:
    description:
      - Subscriptions with individual settings, C(SubscriptionList.subscription).
        Each entry has C(path) and optionally C(stream_mode),
        C(sample_interval), C(heartbeat_interval) and C(suppress_redundant),
        with the same meaning as the top-level options.
      - The 1.0.0 keys C(mode), C(sampleInterval), C(heartbeatInterval) and
        C(suppressRedundant) were removed in 2.0.0.
      - Mutually exclusive with O(path).
    type: list
    elements: dict
  origin:
    description:
      - Origin of the paths, C(Path.origin), for example C(openconfig) or
        C(rfc7951). Set on O(prefix) if given, otherwise on each path that
        does not name its own origin.
      - With an origin, element names keep their YANG module prefix.
      - Defaults to the C(gnmi_origin) option of the connection. An empty
        string sends the paths without origin.
    type: str
    version_added: 2.0.1
  prefix:
    description:
      - Common prefix for all paths, C(SubscriptionList.prefix).
    type: str
    default: ''
  target:
    description:
      - Target name set on the prefix, C(Path.target).
    type: str
    version_added: 2.0.0
  model:
    description:
      - Restricts the subscription to a model by name,
        C(SubscriptionList.use_models).
    type: str
    version_added: 2.0.0
  mode:
    description:
      - Subscription mode, C(SubscriptionList.mode).
      - One of C(STREAM), C(ONCE), C(POLL).
      - The default changed from C(ONCE) to C(STREAM) in 2.0.0, matching the
        default of the gNMI specification.
    type: str
    default: STREAM
  stream_mode:
    description:
      - Mode of each subscription if O(mode=STREAM), C(Subscription.mode).
      - One of C(SAMPLE), C(ON_CHANGE), C(TARGET_DEFINED). Defaults to
        C(SAMPLE).
    type: str
    version_added: 2.0.0
  sample_interval:
    description:
      - Sample interval as Go duration, for example C(10s),
        C(Subscription.sample_interval).
      - Omitted or C(0s) lets the target choose.
    type: str
    version_added: 2.0.0
  heartbeat_interval:
    description:
      - Heartbeat interval as Go duration,
        C(Subscription.heartbeat_interval).
    type: str
    version_added: 2.0.0
  suppress_redundant:
    description:
      - Suppress updates of unchanged values,
        C(Subscription.suppress_redundant).
    type: bool
    version_added: 2.0.0
  updates_only:
    description:
      - Do not send the initial state, only changes after the
        synchronization, C(SubscriptionList.updates_only).
    type: bool
  allow_aggregation:
    description:
      - Allow the target to aggregate elements that are marked as eligible
        for aggregation in the schema.
    type: bool
  qos:
    description:
      - DSCP marking of the subscription, C(SubscriptionList.qos).
    type: int
  encoding:
    description:
      - Overrides the encoding of the connection, C(SubscriptionList.encoding).
        Either C(JSON) or C(JSON_IETF).
    type: str
    version_added: 2.0.0
  depth:
    description:
      - Limits the depth of the returned subtrees using the gNMI Depth
        extension, C(Depth.level). C(0) means no limit.
    type: int
    version_added: 2.0.0
  config_subscription:
    description:
      - Subscribe to configuration nodes only, using the gNMI
        ConfigSubscription extension (C(ConfigSubscriptionStart)).
      - SR OS supports the extension with O(mode=STREAM) only.
      - The target reports each commit with a C(sync_done) extension, returned
        in RV(extensions) with C(commit_confirm_id), C(server_commit_id) and
        C(done).
      - With O(mode=STREAM) and no O(duration), the subscription ends when the
        target reports C(done=true), at the latest when the command timeout
        of the connection expires.
    type: bool
    default: false
    version_added: 2.0.0
  duration:
    description:
      - Time in seconds to collect responses. A task cannot keep a
        subscription open, so a C(STREAM) subscription always ends.
      - For C(STREAM) the subscription is closed when it expires. For C(ONCE)
        and C(POLL) it is a timeout.
      - Defaults to C(20), except for O(config_subscription) in C(STREAM)
        mode, see there.
      - Must be lower than the C(persistent_command_timeout) of the connection.
    type: int
notes:
  - Requires the P(nokia.openconfig.grpc#connection) connection.
  - Check mode is supported. The task is skipped and no Subscribe RPC is
    sent (use M(nokia.openconfig.gnmi_get) for read-only checks).
  - The Subscribe RPC is a bidirectional stream. The connection sends the
    C(SubscribeRequest), and in C(POLL) mode one C(Poll) after the initial
    synchronization, then reads responses until the subscription completes.
  - C(ONCE) completes with the C(sync_response) of the target, C(POLL) with
    the second C(sync_response). If O(duration) expires first, the task
    fails.
  - C(STREAM) is closed by the client when O(duration) expires, and the task
    returns the notifications received until then. With O(config_subscription)
    and no O(duration), the task returns as soon as the target reports a
    C(sync_done) with C(done=true) after the initial synchronization.
requirements:
  - grpcio
  - protobuf
"""

EXAMPLES = """
- name: Get the system configuration using Subscribe ONCE (SR OS)
  nokia.openconfig.gnmi_subscribe:
    mode: once
    path:
      - /configure/system

- name: Get the system information using Subscribe ONCE (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    mode: once
    path:
      - /system/information

- name: Collect management port statistics for 5 seconds (SR OS)
  nokia.openconfig.gnmi_subscribe:
    prefix: /state
    path:
      - /port[port-id=A/1]/statistics
    stream_mode: sample
    sample_interval: 1s
    duration: 5

- name: Collect management interface statistics for 5 seconds (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /interface[name=mgmt0]/statistics
    stream_mode: sample
    sample_interval: 1s
    duration: 5

- name: Sample OpenConfig interface counters every 10 seconds for 30 seconds
  nokia.openconfig.gnmi_subscribe:
    origin: openconfig
    path:
      - /interfaces/interface/state/counters
    stream_mode: sample
    sample_interval: 10s
    duration: 30

- name: Collect configuration changes for 60 seconds (SR OS)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /configure/system
    stream_mode: on_change
    config_subscription: true
    duration: 60
  register: commits

- name: Collect configuration changes for 60 seconds (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /interface[name=ethernet-1/1]
    stream_mode: on_change
    config_subscription: true
    duration: 60
  register: commits
"""

RETURN = """
output:
  description:
    - For C(ONCE), the merged object tree as JSON string.
    - For C(STREAM) and C(POLL), a JSON string with a list of notifications,
      each with C(prefix), C(timestamp), C(values) and C(deletes).
  returned: success
  type: str
  sample: '[{"prefix": "/state/port[port-id=1/1/c1/1]/ethernet/statistics", "timestamp": "2020-02-18T00:19:34.954275", "values": {"in-octets": "0"}}]'
extensions:
  description:
    - Extensions returned in the C(SubscribeResponse) messages, using
      protobuf field names.
  returned: success
  type: list
  elements: dict
  sample: [{"config_subscription": {"sync_done": {"commit_confirm_id": "c1", "server_commit_id": "17", "done": true}}}]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi import (
    REMOVED_SUBSCRIPTION_KEYS,
    STREAM_MODES,
    SUBSCRIBE_MODES,
    GnmiError,
    parse_duration,
)
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_module import (
    Rpc,
    normalize_enum,
    to_json,
)

SUBSCRIPTION_KEYS = ('path', 'stream_mode', 'sample_interval', 'heartbeat_interval', 'suppress_redundant')


def _check_subscription(module, subscription):
    for entry in subscription:
        removed = sorted(set(entry) & set(REMOVED_SUBSCRIPTION_KEYS))
        if removed:
            module.fail_json(msg="Subscription keys removed in 2.0.0: %s. Use %s instead" % (
                ', '.join(removed), ', '.join(REMOVED_SUBSCRIPTION_KEYS[k] for k in removed)))
        unknown = set(entry) - set(SUBSCRIPTION_KEYS)
        if unknown:
            module.fail_json(msg="Unsupported keys in subscription: %s" % ', '.join(sorted(unknown)))
        if 'path' not in entry:
            module.fail_json(msg="Each subscription needs a path")
        if entry.get('stream_mode'):
            normalize_enum(module, 'subscription.stream_mode', STREAM_MODES, entry['stream_mode'])
        for name in ('sample_interval', 'heartbeat_interval'):
            try:
                parse_duration(entry.get(name))
            except GnmiError as exc:
                module.fail_json(msg="subscription %s: %s" % (name, exc))


def main():
    argument_spec = dict(
        path=dict(type='list', elements='str'),
        subscription=dict(type='list', elements='dict'),
        origin=dict(type='str'),
        prefix=dict(type='str', default=''),
        target=dict(type='str'),
        model=dict(type='str'),
        mode=dict(type='str', default='STREAM'),
        stream_mode=dict(type='str'),
        sample_interval=dict(type='str'),
        heartbeat_interval=dict(type='str'),
        suppress_redundant=dict(type='bool'),
        updates_only=dict(type='bool'),
        allow_aggregation=dict(type='bool'),
        qos=dict(type='int'),
        encoding=dict(type='str'),
        depth=dict(type='int'),
        config_subscription=dict(type='bool', default=False),
        duration=dict(type='int'),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[('path', 'subscription')],
        required_one_of=[('path', 'subscription')],
        supports_check_mode=True,
    )

    params = dict(module.params)
    params['mode'] = normalize_enum(module, 'mode', SUBSCRIBE_MODES)
    params['stream_mode'] = normalize_enum(module, 'stream_mode', STREAM_MODES)
    params['encoding'] = normalize_enum(module, 'encoding', ('JSON', 'JSON_IETF'))
    if params['subscription']:
        _check_subscription(module, params['subscription'])
    for name in ('sample_interval', 'heartbeat_interval'):
        try:
            parse_duration(params[name])
        except GnmiError as exc:
            module.fail_json(msg="%s: %s" % (name, exc))
    if params['depth'] is not None and params['depth'] < 0:
        module.fail_json(msg="depth must be zero or positive")
    if params['duration'] is not None and params['duration'] <= 0:
        module.fail_json(msg="duration must be positive")

    if module.check_mode:
        module.exit_json(changed=False, skipped=True, msg='check mode')

    response = Rpc(module)('gnmiSubscribe', **params)
    module.exit_json(changed=False, output=to_json(response['output']), extensions=response['extensions'])


if __name__ == '__main__':
    main()
