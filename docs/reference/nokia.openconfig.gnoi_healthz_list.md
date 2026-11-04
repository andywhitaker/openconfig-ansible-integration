# Ansible Module: nokia.openconfig.gnoi_healthz_list

**List health events of a component over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNOI `Healthz.List` for a component.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | str | Component path in SR Linux native syntax.<br/>**Required:** always |
| include_acknowledged {#param-include-acknowledged} | bool | Include acknowledged events. |

## Examples

```yaml
- name: List the health events of control module A (SR Linux)
  nokia.openconfig.gnoi_healthz_list:
    path: /platform/control[slot=A]
    include_acknowledged: true
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
