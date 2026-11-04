# Ansible Module: nokia.openconfig.gnsi_authz_get

**Get the gRPC authorization policy over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Authz.Get`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| authz_profile_id {#param-authz-profile-id} | str | Authz profile; the default profile when omitted. |

## Examples

```yaml
- name: Read the active Authz policy (SR Linux)
  nokia.openconfig.gnsi_authz_get:
  register: authz
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
