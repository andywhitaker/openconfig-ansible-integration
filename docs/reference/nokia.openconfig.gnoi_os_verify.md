# Ansible Module: nokia.openconfig.gnoi_os_verify

**Get the running OS version over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    SR Linux hardware platforms only; the SR Linux simulator rejects gNOI OS RPCs.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `OS.Verify`.

## Examples

```yaml
- name: Verify the running version (SR Linux)
  nokia.openconfig.gnoi_os_verify:
  register: os
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
