# Ansible Module: nokia.openconfig.gnoi_system_cancel_reboot

**Cancel a pending reboot over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.CancelReboot`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| reason {#param-reason} | str | Informational reason for the cancel, sent as the request `message` field. |
| subcomponents {#param-subcomponents} | list | Subcomponent paths (gNMI path syntax), using the native models, for example `/state/cpm[cpm-slot=A]` on SR OS or `/platform/control[slot=A]` on SR Linux. |

## Examples

```yaml
- name: Cancel a pending reboot of CPM A (SR OS)
  nokia.openconfig.gnoi_system_cancel_reboot:
    reason: change aborted
    subcomponents:
      - /state/cpm[cpm-slot=A]

- name: Cancel a pending reboot (SR Linux)
  nokia.openconfig.gnoi_system_cancel_reboot:
    reason: change aborted
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
