# Ansible Module: nokia.openconfig.gnmi_get

**Retrieve configuration and state using gNMI Get**

!!! note "Notes"

    Requires the [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md) connection.

    Check mode is supported. The module never changes the device.

## Synopsis

* Sends a single gNMI `GetRequest`.
* Option names are the `GetRequest` fields in snake_case, and the values follow the gNMI 0.10.0 protobuf messages. Enum values are case-insensitive.
* The notifications of the `GetResponse` are merged into a single object tree. Keyed list entries become lists that include their key leaves.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | list | Paths to retrieve, `GetRequest.path`.<br/>gNMI path strings with list keys, for example `/interface[name=ethernet-1/1]/description`.<br/>The origin is given as prefix, for example `openconfig:/interfaces/interface`.<br/>If omitted, the root path is retrieved.<br/>**Default:** `['']` |
| prefix {#param-prefix} | str | Common prefix for all paths, `GetRequest.prefix`.<br/>**Default:** `''` |
| target {#param-target} | str | Target name set on the prefix, `Path.target`. |
| model {#param-model} | str | Restricts the request to a model by name as reported by [nokia.openconfig.gnmi_capabilities](nokia.openconfig.gnmi_capabilities.md), `GetRequest.use_models`. |
| type {#param-type} | str | Data type to retrieve, `GetRequest.type`.<br/>One of `ALL`, `CONFIG`, `STATE`, `OPERATIONAL`.<br/>The default changed from `CONFIG` to `ALL` in 2.0.0, matching the default of the gNMI specification.<br/>**Default:** `ALL` |
| depth {#param-depth} | int | Limits the depth of the returned subtree using the gNMI Depth extension, `Depth.level`.<br/>`0` means no limit, so no extension is sent. |
| encoding {#param-encoding} | str | Overrides the encoding of the connection for this request, `GetRequest.encoding`. Either `JSON` or `JSON_IETF`. |
| values_only {#param-values-only} | bool | Return a list with the decoded values only, without paths.<br/>**Default:** `false` |

## Examples

```yaml
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
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str |  - Merged object tree (or list of values if [`values_only=true`](#param-values-only)) as JSON<br/>**Returned:** success<br/>**Sample:** `{"interface":[{"name":"ethernet-1/1","admin-state":"enable"}]}` |
| extensions {#return-extensions} | list |  - Extensions returned in the `GetResponse`, using protobuf field names.<br/>**Returned:** success<br/>**Sample:** `[{"depth":{"level":1}}]` |

*New in version 1.0.0*
