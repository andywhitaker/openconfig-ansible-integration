# Ansible Module: nokia.openconfig.gnoi_factory_reset_start

**Factory reset the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `FactoryReset.Start`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| factory_os {#param-factory-os} | bool | Roll back to the factory OS image. |
| zero_fill {#param-zero-fill} | bool | Zero-fill persistent storage. |
| retain_certs {#param-retain-certs} | bool | Keep certificates across the reset. |

## Examples

```yaml
- name: Factory reset, keeping certificates
  nokia.openconfig.gnoi_factory_reset_start:
    retain_certs: true
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
