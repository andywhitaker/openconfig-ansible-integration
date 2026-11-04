# Ansible Module: nokia.openconfig.gnsi_credentialz_get_public_keys

**Get the SSH host public keys over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Credentialz.GetPublicKeys`.

## Examples

```yaml
- name: Read SSH host keys (SR Linux)
  nokia.openconfig.gnsi_credentialz_get_public_keys:
  register: keys
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
