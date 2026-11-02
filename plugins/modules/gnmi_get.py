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
  - Sends a single gNMI C(GetRequest), like C(gnmic get).
  - Option names follow the gNMIc flags in snake_case, and the values follow
    the gNMI 0.10.0 protobuf messages. Enum values are case-insensitive.
  - The notifications of the C(GetResponse) are merged into a single object
    tree. Keyed list entries become lists that include their key leaves.
version_added: 1.0.0
options:
  path:
    description:
      - Paths to retrieve, gNMIc C(--path) and C(GetRequest.path).
      - XPath-like syntax with list keys, for example
        C(/interface[name=ethernet-1/1]/description).
      - The origin is given gNMIc style, for example
        C(openconfig:/interfaces/interface).
      - If omitted, the root path is retrieved.
    type: list
    elements: str
    default: ['']
  prefix:
    description:
      - Common prefix for all paths, gNMIc C(--prefix) and C(GetRequest.prefix).
    type: str
    default: ''
  target:
    description:
      - Target name set on the prefix, gNMIc C(--target) and C(Path.target).
    type: str
    version_added: 2.0.0
  model:
    description:
      - Restricts the request to a model by name as reported by
        M(nokia.openconfig.gnmi_capabilities), gNMIc C(--model) and
        C(GetRequest.use_models).
    type: str
    version_added: 2.0.0
  type:
    description:
      - Data type to retrieve, gNMIc C(--type) and C(GetRequest.type).
      - One of C(ALL), C(CONFIG), C(STATE), C(OPERATIONAL).
      - The default changed from C(CONFIG) to C(ALL) in 2.0.0, matching
        gNMIc.
    type: str
    default: ALL
  depth:
    description:
      - Limits the depth of the returned subtree using the gNMI Depth
        extension, gNMIc C(--depth).
      - C(0) means no limit, so no extension is sent.
    type: int
    version_added: 2.0.0
  encoding:
    description:
      - Overrides the encoding of the connection for this request, gNMIc
        C(--encoding). Either C(JSON) or C(JSON_IETF).
    type: str
    version_added: 2.0.0
  values_only:
    description:
      - Return a list with the decoded values only, gNMIc C(--values-only).
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
# gnmic get --path /interface[name=ethernet-1/1] --type config --depth 1
- name: Get interface configuration
  nokia.openconfig.gnmi_get:
    path:
      - /interface[name=ethernet-1/1]
    type: config
    depth: 1
  register: result

# SR Linux qualifies top-level JSON_IETF members with the YANG module name
- name: Show description
  ansible.builtin.debug:
    msg: "{{ (result.output | from_json)['srl_nokia-interfaces:interface'][0].description }}"

- name: Get openconfig interfaces, values only
  nokia.openconfig.gnmi_get:
    path:
      - openconfig:/interfaces/interface[name=ethernet-1/1]/state
    values_only: true
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
