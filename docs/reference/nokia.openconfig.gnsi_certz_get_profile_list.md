# Ansible Module: nokia.openconfig.gnsi_certz_get_profile_list

**List TLS profiles over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Certz.GetProfileList`.

## Examples

```yaml
- name: List TLS profiles (SR Linux)
  nokia.openconfig.gnsi_certz_get_profile_list:
  register: profiles
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
