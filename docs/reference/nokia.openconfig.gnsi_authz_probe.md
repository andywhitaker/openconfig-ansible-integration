# Ansible Module: nokia.openconfig.gnsi_authz_probe

**Check if a user may call a gRPC method over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Authz.Probe` and returns the policy decision.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| user {#param-user} | str | User name.<br/>**Required:** always |
| rpc {#param-rpc} | str | Fully qualified gRPC method, for example `/gnmi.gNMI/Get`.<br/>**Required:** always |

## Examples

```yaml
- name: May admin call gNMI Set? (SR Linux)
  nokia.openconfig.gnsi_authz_probe:
    user: admin
    rpc: /gnmi.gNMI/Set
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
