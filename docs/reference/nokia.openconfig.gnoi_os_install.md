# Ansible Module: nokia.openconfig.gnoi_os_install

**Install an OS image over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    SR Linux hardware platforms only; the SR Linux simulator rejects gNOI OS RPCs.

    The connection sends a fixed request sequence: `TransferRequest` with [`os_version`](#param-os-version) and [`standby_supervisor`](#param-standby-supervisor), the image in 64 KiB `transfer_content` chunks, then `TransferEnd`. It does not wait for `TransferReady` before sending the image; gRPC flow control paces the upload.

    The task returns when the device closes the stream, normally after `Validated` or `InstallError`. All server messages, such as `TransferReady`, `TransferProgress` and `Validated`, are returned in R`output`. The upload and validation must complete within the command timeout of the connection (`ansible_command_timeout`); raise it for large images.

    The image is installed, not activated. Use [nokia.openconfig.gnoi_os_activate](nokia.openconfig.gnoi_os_activate.md) to boot it.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Bidirectional streaming RPC. The connection sends the request sequence built from the options and collects every server message until the device closes the stream.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `OS.Install`, streaming a local image to the device and returning all server messages.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| local_path {#param-local-path} | path | OS image on the controller. A relative path is resolved against the working directory of ansible-playbook.<br/>**Required:** always |
| os_version {#param-os-version} | str | Version string of the image. |
| standby_supervisor {#param-standby-supervisor} | bool | Install on the standby supervisor. |

## Examples

```yaml
- name: Transfer an OS image (SR Linux)
  nokia.openconfig.gnoi_os_install:
    local_path: ./srlinux-25.10.1.bin
    os_version: 25.10.1
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response messages as a JSON list in stream order (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
