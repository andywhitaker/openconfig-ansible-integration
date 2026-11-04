# Ansible Module: nokia.openconfig.gnoi_healthz_get

**Get the health of a component over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNOI `Healthz.Get` for a component.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | str | Component path in SR Linux native syntax, for example `/platform/control[slot=A]`.<br/>**Required:** always |

## Examples

```yaml
- name: Get the health of control module A (SR Linux)
  nokia.openconfig.gnoi_healthz_get:
    path: /platform/control[slot=A]
  register: health

- name: Show the status and artifact IDs
  vars:
    component: "{{ (health.output | from_json).component }}"
  ansible.builtin.debug:
    msg: "{{ component.status }} {{ component.artifacts | default([]) | map(attribute='id') | list }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
