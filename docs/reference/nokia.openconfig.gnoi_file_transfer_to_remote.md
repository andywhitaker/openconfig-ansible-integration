# Ansible Module: nokia.openconfig.gnoi_file_transfer_to_remote

**Transfer a device file to a remote server over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS. SR Linux does not implement this RPC.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `File.TransferToRemote`; the device uploads one of its files to a remote server.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| remote_path {#param-remote-path} | str | File on the device to transfer.<br/>**Required:** always |
| remote_download {#param-remote-download} | dict | Destination as gNOI `RemoteDownload` fields (protobuf JSON names), for example `path`, `protocol` and `credentials`.<br/>**Required:** always |

## Examples

```yaml
- name: Upload the configuration to an SFTP server (SR OS)
  nokia.openconfig.gnoi_file_transfer_to_remote:
    remote_path: cf3:/config.cfg
    remote_download:
      path: 192.0.2.10:/backups/config.cfg
      protocol: SFTP
      credentials:
        username: backup
        cleartext: secret
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
