# Ansible Module: nokia.openconfig.gnoi_file_put

**Upload a file to the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Client-streaming RPC. The task streams [`local_path`](#param-local-path) in 64 KiB chunks followed by its SHA-256 hash, then returns the single response of the device. The upload must complete within the command timeout of the connection (`ansible_command_timeout`).

## Synopsis

* Invokes gNOI `File.Put`, streaming a local file in 64 KiB chunks followed by its SHA-256 hash.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| local_path {#param-local-path} | path | Source file on the controller. A relative path is resolved against the working directory of ansible-playbook.<br/>**Required:** always |
| remote_path {#param-remote-path} | str | Destination file on the device.<br/>**Required:** always |
| permissions {#param-permissions} | int | Unix permissions of the remote file, as octal digits.<br/>SR OS accepts only `777` and `555`. A file uploaded with `555` is read-only and cannot be overwritten or removed over gNOI.<br/>**Default:** `644` |

## Examples

```yaml
- name: Upload a file to the compact flash (SR OS)
  nokia.openconfig.gnoi_file_put:
    local_path: ./banner.txt
    remote_path: cf3:/banner.txt
    permissions: 777

- name: Upload a file (SR Linux)
  nokia.openconfig.gnoi_file_put:
    local_path: ./banner.txt
    remote_path: /tmp/banner.txt
    permissions: 644
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
