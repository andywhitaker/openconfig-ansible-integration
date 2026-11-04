# Ansible Module: nokia.openconfig.gnoi_file_remove

**Remove a file from the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

## Synopsis

* Invokes gNOI `File.Remove`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| remote_path {#param-remote-path} | str | File on the device.<br/>**Required:** always |

## Examples

```yaml
- name: Remove a file from the compact flash (SR OS)
  nokia.openconfig.gnoi_file_remove:
    remote_path: cf3:/banner.txt

- name: Remove a file (SR Linux)
  nokia.openconfig.gnoi_file_remove:
    remote_path: /tmp/banner.txt
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
