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
module: gnmi_capabilities
author:
  - "Hans Thienpondt (@HansThienpondt)"
  - "Sven Wisotzky (@wisotzky)"
short_description: Get gNMI server capabilities
description:
  - Sends a gNMI C(CapabilityRequest), like C(gnmic capabilities), and
    returns the gNMI version, supported encodings and supported models of the
    device.
version_added: 1.0.0
options: {}
notes:
  - Requires the P(nokia.openconfig.grpc#connection) connection.
  - Check mode is supported. The module never changes the device.
requirements:
  - grpcio
  - protobuf
"""

EXAMPLES = """
# gnmic capabilities
- name: Get gNMI capabilities
  nokia.openconfig.gnmi_capabilities:
  register: caps

- name: Require gNMI 0.10.0 or later
  ansible.builtin.assert:
    that: caps.gnmi_version is version('0.10.0', '>=')
"""

RETURN = """
output:
  description:
    - The C(CapabilityResponse) in protobuf JSON form (camelCase keys).
  returned: success
  type: dict
  sample:
    gNMIVersion: 0.10.0
    supportedEncodings: [JSON_IETF, ASCII, BYTES]
    supportedModels:
      - name: nokia-conf
        organization: Nokia
        version: 25.7.R2
gnmi_version:
  description:
    - gNMI service version of the device.
  returned: success
  type: str
  sample: 0.10.0
  version_added: 2.0.0
encodings:
  description:
    - Supported encodings.
  returned: success
  type: list
  elements: str
  sample: [JSON_IETF, ASCII, BYTES]
  version_added: 2.0.0
models:
  description:
    - Supported models with C(name), C(organization) and C(version).
  returned: success
  type: list
  elements: dict
  sample: [{"name": "nokia-conf", "organization": "Nokia", "version": "25.7.R2"}]
  version_added: 2.0.0
extensions:
  description:
    - Extensions returned in the C(CapabilityResponse), using protobuf field
      names.
  returned: success
  type: list
  elements: dict
  version_added: 2.0.0
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_ext import parse_extensions
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_module import Rpc


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    response = Rpc(module)('gnmiCapabilities')
    module.exit_json(
        changed=False,
        output=response,
        gnmi_version=response.get('gNMIVersion', ''),
        encodings=response.get('supportedEncodings', []),
        models=response.get('supportedModels', []),
        extensions=parse_extensions(response.get('extension')),
    )


if __name__ == '__main__':
    main()
