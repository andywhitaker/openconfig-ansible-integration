# Ansible Module: nokia.openconfig.gnmi_capabilities

**Get gNMI server capabilities**

!!! note "Notes"

    Requires the [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md) connection.

    Check mode is supported. The module never changes the device.

## Synopsis

* Sends a gNMI `CapabilityRequest` and returns the gNMI version, supported encodings and supported models of the device.

## Examples

```yaml
- name: Get gNMI capabilities
  nokia.openconfig.gnmi_capabilities:
  register: caps

- name: Require JSON_IETF and the native configuration model (SR OS)
  ansible.builtin.assert:
    that:
      - "'JSON_IETF' in caps.encodings"
      - caps.models | selectattr('name', 'equalto', 'nokia-conf') | list | length > 0

- name: Require gNMI 0.10.0 and the native system model (SR Linux)
  ansible.builtin.assert:
    that:
      - caps.gnmi_version is version('0.10.0', '>=')
      - caps.models | selectattr('name', 'search', ':srl_nokia-system$') | list | length > 0
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | dict |  - The `CapabilityResponse` in protobuf JSON form (camelCase keys). - name: nokia-conf<br/>**Returned:** success<br/>**Sample:** `` |
| gnmi_version {#return-gnmi-version} | str |  - gNMI service version of the device.<br/>**Returned:** success<br/>**Sample:** `0.10.0` |
| encodings {#return-encodings} | list |  - Supported encodings.<br/>**Returned:** success<br/>**Sample:** `[JSON_IETF, ASCII, BYTES]` |
| models {#return-models} | list |  - Supported models with `name`, `organization` and `version`.<br/>**Returned:** success<br/>**Sample:** `[{"name":"nokia-conf","organization":"Nokia","version":"25.7.R2"}]` |
| extensions {#return-extensions} | list |  - Extensions returned in the `CapabilityResponse`, using protobuf field<br/>**Returned:** success |

*New in version 1.0.0*
