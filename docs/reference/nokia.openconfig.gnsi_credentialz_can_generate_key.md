# Ansible Module: nokia.openconfig.gnsi_credentialz_can_generate_key

**Check if the device can generate an SSH host key over gNSI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux. gNSI must be enabled on the gRPC server.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNSI `Credentialz.CanGenerateKey`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| key_params {#param-key-params} | str | Key type.<br/>**Choices:** `KEY_GEN_SSH_KEY_TYPE_RSA_2048`, `KEY_GEN_SSH_KEY_TYPE_ECDSA_P_256`, `KEY_GEN_SSH_KEY_TYPE_ECDSA_P_521`, `KEY_GEN_SSH_KEY_TYPE_EDDSA_ED25519`<br/>**Required:** always |

## Examples

```yaml
- name: Can the device generate an Ed25519 host key? (SR Linux)
  nokia.openconfig.gnsi_credentialz_can_generate_key:
    key_params: KEY_GEN_SSH_KEY_TYPE_EDDSA_ED25519
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
