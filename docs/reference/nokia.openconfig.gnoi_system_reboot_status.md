# Ansible Module: nokia.openconfig.gnoi_system_reboot_status

**Get the status of a pending reboot over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.RebootStatus`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| subcomponents {#param-subcomponents} | list | Subcomponent paths (gNMI path syntax), using the native models, for example `/state/cpm[cpm-slot=A]` on SR OS or `/platform/control[slot=A]` on SR Linux.<br/>SR OS requires at least one subcomponent. |

## Examples

```yaml
- name: Check for a pending reboot of CPM A (SR OS)
  nokia.openconfig.gnoi_system_reboot_status:
    subcomponents:
      - /state/cpm[cpm-slot=A]
  register: status

- name: Check for a pending reboot (SR Linux)
  nokia.openconfig.gnoi_system_reboot_status:
  register: status
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
