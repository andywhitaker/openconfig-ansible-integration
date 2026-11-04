# Ansible Module: nokia.openconfig.gnoi_os_activate

**Activate an installed OS version over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    SR Linux hardware platforms only; the SR Linux simulator rejects gNOI OS RPCs.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `OS.Activate`. The device reboots unless [`no_reboot`](#param-no-reboot) is set.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| os_version {#param-os-version} | str | Installed version to activate.<br/>**Required:** always |
| standby_supervisor {#param-standby-supervisor} | bool | Activate on the standby supervisor. |
| no_reboot {#param-no-reboot} | bool | Activate without rebooting. |

## Examples

```yaml
- name: Activate a version and reboot (SR Linux)
  nokia.openconfig.gnoi_os_activate:
    os_version: 25.10.1
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
