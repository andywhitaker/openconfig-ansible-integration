# Ansible Module: nokia.openconfig.gnsi_pathz_get

**Get the gNMI path authorization policy over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    The RPC fails with `FAILED_PRECONDITION` if no Pathz policy is installed for the requested instance.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Pathz.Get`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| policy_instance {#param-policy-instance} | str | Policy instance.<br/>**Choices:** `POLICY_INSTANCE_ACTIVE`, `POLICY_INSTANCE_SANDBOX`<br/>**Default:** `POLICY_INSTANCE_ACTIVE` |

## Examples

```yaml
- name: Read the active Pathz policy (SR Linux)
  nokia.openconfig.gnsi_pathz_get:
  register: pathz
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
