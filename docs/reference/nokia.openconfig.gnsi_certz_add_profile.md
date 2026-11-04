# Ansible Module: nokia.openconfig.gnsi_certz_add_profile

**Add a TLS profile over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

## Synopsis

* Invokes gNSI `Certz.AddProfile`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| ssl_profile_id {#param-ssl-profile-id} | str | Profile ID.<br/>**Required:** always |

## Examples

```yaml
- name: Add a profile (SR Linux)
  nokia.openconfig.gnsi_certz_add_profile:
    ssl_profile_id: telemetry
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
