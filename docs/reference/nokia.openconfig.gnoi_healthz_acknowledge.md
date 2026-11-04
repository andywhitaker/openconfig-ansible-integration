# Ansible Module: nokia.openconfig.gnoi_healthz_acknowledge

**Acknowledge a health event over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `Healthz.Acknowledge`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | str | Component path in SR Linux native syntax.<br/>**Required:** always |
| id {#param-id} | str | Event ID to acknowledge.<br/>**Required:** always |

## Examples

```yaml
- name: Acknowledge a health event of control module A (SR Linux)
  nokia.openconfig.gnoi_healthz_acknowledge:
    path: /platform/control[slot=A]
    id: "{{ event_id }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
