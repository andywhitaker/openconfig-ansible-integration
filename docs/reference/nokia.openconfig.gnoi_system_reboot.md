# Ansible Module: nokia.openconfig.gnoi_system_reboot

**Reboot the device or a subcomponent over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.Reboot`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| method {#param-method} | str | Reboot method.<br/>**Choices:** `COLD`, `POWERDOWN`, `HALT`, `WARM`, `NSF`, `POWERUP` |
| delay {#param-delay} | raw | Delay before the reboot, as Go duration or seconds. |
| reason {#param-reason} | str | Informational reason for the reboot, sent as the request `message` field. |
| subcomponents {#param-subcomponents} | list | Subcomponent paths to reboot (gNMI path syntax), using the native models, for example `/state/cpm[cpm-slot=A]` on SR OS or `/platform/control[slot=A]` on SR Linux. |
| force {#param-force} | bool | Force the reboot, skipping sanity checks. |

## Examples

```yaml
- name: Cold reboot of CPM A in one minute (SR OS)
  nokia.openconfig.gnoi_system_reboot:
    method: COLD
    delay: 1m
    reason: maintenance
    subcomponents:
      - /state/cpm[cpm-slot=A]

- name: Cold reboot in one minute (SR Linux)
  nokia.openconfig.gnoi_system_reboot:
    method: COLD
    delay: 1m
    reason: maintenance
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
