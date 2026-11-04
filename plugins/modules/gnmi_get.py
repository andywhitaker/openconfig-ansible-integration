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
module: gnmi_get
author:
  - "Hans Thienpondt (@HansThienpondt)"
  - "Sven Wisotzky (@wisotzky)"
short_description: Retrieve configuration and state using gNMI Get
description:
  - Sends a single gNMI C(GetRequest).
  - Option names are the C(GetRequest) fields in snake_case, and the values
    follow the gNMI 0.10.0 protobuf messages. Enum values are
    case-insensitive.
  - The notifications of the C(GetResponse) are merged into a single object
    tree. Keyed list entries become lists that include their key leaves.
version_added: 1.0.0
options:
  path:
    description:
      - Paths to retrieve, C(GetRequest.path).
      - gNMI path strings with list keys, for example
        C(/interface[name=ethernet-1/1]/description).
      - A path can name its origin, for example
        C(openconfig:/interfaces/interface). Otherwise O(origin) applies.
      - If omitted, the root path is retrieved.
    type: list
    elements: str
    default: ['']
  origin:
    description:
      - Origin of the paths, C(Path.origin), for example C(openconfig) or
        C(rfc7951). Set on O(prefix) if given, otherwise on each path that
        does not name its own origin.
      - With an origin, element names keep their YANG module prefix, for
        example C(/Cisco-IOS-XE-native:native/hostname) with C(rfc7951).
      - Defaults to the C(gnmi_origin) option of the connection. An empty
        string sends the paths without origin.
    type: str
    version_added: 2.0.1
  prefix:
    description:
      - Common prefix for all paths, C(GetRequest.prefix).
    type: str
    default: ''
  target:
    description:
      - Target name set on the prefix, C(Path.target).
    type: str
    version_added: 2.0.0
  model:
    description:
      - Restricts the request to a model by name as reported by
        M(nokia.openconfig.gnmi_capabilities), C(GetRequest.use_models).
    type: str
    version_added: 2.0.0
  type:
    description:
      - Data type to retrieve, C(GetRequest.type).
      - One of C(ALL), C(CONFIG), C(STATE), C(OPERATIONAL).
      - The default changed from C(CONFIG) to C(ALL) in 2.0.0, matching the
        default of the gNMI specification.
    type: str
    default: ALL
  depth:
    description:
      - Limits the depth of the returned subtree using the gNMI Depth
        extension, C(Depth.level).
      - C(0) means no limit, so no extension is sent.
    type: int
    version_added: 2.0.0
  encoding:
    description:
      - Overrides the encoding of the connection for this request,
        C(GetRequest.encoding). Either C(JSON) or C(JSON_IETF).
    type: str
    version_added: 2.0.0
  values_only:
    description:
      - Return a list with the decoded values only, without paths.
    type: bool
    default: false
    version_added: 2.0.0
notes:
  - Requires the P(nokia.openconfig.grpc#connection) connection.
  - Check mode is supported. The module never changes the device.
requirements:
  - grpcio
  - protobuf
"""

EXAMPLES = """
- name: Get the system configuration, one level deep (SR OS)
  nokia.openconfig.gnmi_get:
    path:
      - /configure/system
    type: config
    depth: 1
  register: result

# SR OS qualifies JSON_IETF members below the top-level container
- name: Show the system name (SR OS)
  ansible.builtin.debug:
    msg: "{{ (result.output | from_json).configure.system['nokia-conf:name'] }}"

- name: Get the interface configuration, one level deep (SR Linux)
  nokia.openconfig.gnmi_get:
    path:
      - /interface[name=ethernet-1/1]
    type: config
    depth: 1
  register: result

# SR Linux qualifies top-level JSON_IETF members with the YANG module name
- name: Show the description (SR Linux)
  ansible.builtin.debug:
    msg: "{{ (result.output | from_json)['srl_nokia-interfaces:interface'][0].description }}"

- name: Get the OpenConfig port state, values only (SR OS)
  nokia.openconfig.gnmi_get:
    path:
      - openconfig:/interfaces/interface[name=1/1/c1/1]/state/oper-status
    values_only: true

- name: Get the OpenConfig interface state, values only (SR Linux)
  nokia.openconfig.gnmi_get:
    path:
      - openconfig:/interfaces/interface[name=ethernet-1/1]/state/oper-status
    values_only: true

- name: Get several OpenConfig paths with one origin
  nokia.openconfig.gnmi_get:
    origin: openconfig
    path:
      - /system/config/hostname
      - /interfaces/interface[name=ethernet-1/1]/state/oper-status

# Module-qualified first element, as used by Cisco IOS XE native models
- name: Get the hostname from a native YANG model with RFC 7951 paths
  nokia.openconfig.gnmi_get:
    origin: rfc7951
    path:
      - /Cisco-IOS-XE-native:native/hostname
    type: config
"""

RETURN = """
output:
  description:
    - Merged object tree (or list of values if O(values_only=true)) as JSON
      string. Use the C(from_json) filter to access it.
  returned: success
  type: str
  sample: '{"interface": [{"name": "ethernet-1/1", "admin-state": "enable"}]}'
extensions:
  description:
    - Extensions returned in the C(GetResponse), using protobuf field names.
  returned: success
  type: list
  elements: dict
  sample: [{"depth": {"level": 1}}]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi import GET_TYPES
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_module import (
    Rpc,
    normalize_enum,
    to_json,
)


def main():
    argument_spec = dict(
        path=dict(type='list', elements='str', default=['']),
        origin=dict(type='str'),
        prefix=dict(type='str', default=''),
        target=dict(type='str'),
        model=dict(type='str'),
        type=dict(type='str', default='ALL'),
        depth=dict(type='int'),
        encoding=dict(type='str'),
        values_only=dict(type='bool', default=False),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    params = dict(module.params)
    params['type'] = normalize_enum(module, 'type', GET_TYPES)
    params['encoding'] = normalize_enum(module, 'encoding', ('JSON', 'JSON_IETF'))
    if params['depth'] is not None and params['depth'] < 0:
        module.fail_json(msg="depth must be zero or positive")

    response = Rpc(module)('gnmiGet', **params)
    module.exit_json(changed=False, output=to_json(response['output']), extensions=response['extensions'])


if __name__ == '__main__':
    main()
