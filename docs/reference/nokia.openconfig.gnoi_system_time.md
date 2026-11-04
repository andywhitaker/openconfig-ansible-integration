# Ansible Module: nokia.openconfig.gnoi_system_time

**Get the device time over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNOI `System.Time` and returns the device time in nanoseconds since the epoch.

## Examples

```yaml
- name: Query device time
  nokia.openconfig.gnoi_system_time:
  register: result
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
