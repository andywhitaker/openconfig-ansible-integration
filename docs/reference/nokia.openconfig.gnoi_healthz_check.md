# Ansible Module: nokia.openconfig.gnoi_healthz_check

**Run a health check on a component over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    The check does not change the configuration, but SR Linux collects new artifacts, such as a tech-support archive under `/tmp`, that remain on the device.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `Healthz.Check`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | str | Component path in SR Linux native syntax.<br/>**Required:** always |
| event_id {#param-event-id} | str | Re-run the check of an earlier event. |

## Examples

```yaml
- name: Run a health check of control module A (SR Linux)
  nokia.openconfig.gnoi_healthz_check:
    path: /platform/control[slot=A]
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
