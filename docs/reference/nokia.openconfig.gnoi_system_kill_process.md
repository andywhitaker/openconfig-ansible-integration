# Ansible Module: nokia.openconfig.gnoi_system_kill_process

**Signal a process on the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.KillProcess`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| pid {#param-pid} | int | Process ID. |
| name {#param-name} | str | Process name. |
| signal {#param-signal} | str | Signal to send.<br/>**Choices:** `SIGNAL_TERM`, `SIGNAL_KILL`, `SIGNAL_HUP`, `SIGNAL_ABRT` |
| restart {#param-restart} | bool | Restart the process after it terminates. |

## Examples

```yaml
- name: Restart the BGP manager (SR Linux)
  nokia.openconfig.gnoi_system_kill_process:
    name: sr_bgp_mgr
    signal: SIGNAL_TERM
    restart: true
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
