# Ansible Module: nokia.openconfig.gnsi_certz_can_generate_csr

**Check if the device can generate a CSR over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Certz.CanGenerateCSR`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| params {#param-params} | dict | CSR parameters as gNSI `CSRParams` fields (protobuf JSON names).<br/>**Required:** always |

## Examples

```yaml
- name: Can the device generate an ECDSA CSR? (SR Linux)
  nokia.openconfig.gnsi_certz_can_generate_csr:
    params:
      csrSuite: CSRSUITE_X509_KEY_TYPE_ECDSA_PRIME256V1_SIGNATURE_ALGORITHM_SHA_2_256
      commonName: router.example.com
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
