# Ansible Module: nokia.openconfig.gnoi_system_switch_control_processor

**Switch to the standby control processor over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.SwitchControlProcessor`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| control_processor {#param-control-processor} | str | Path of the control processor to switch to (gNMI path syntax), using the native models, for example `/state/cpm[cpm-slot=B]` on SR OS or `/platform/control[slot=B]` on SR Linux.<br/>**Required:** always |

## Examples

```yaml
- name: Switch to CPM B (SR OS)
  nokia.openconfig.gnoi_system_switch_control_processor:
    control_processor: /state/cpm[cpm-slot=B]

- name: Switch to control module B (SR Linux)
  nokia.openconfig.gnoi_system_switch_control_processor:
    control_processor: /platform/control[slot=B]
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
