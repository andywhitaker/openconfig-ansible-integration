# Ansible Module: nokia.openconfig.gnoi_system_set_package

**Upload a software package over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Client-streaming RPC. The task streams [`local_path`](#param-local-path) in 64 KiB chunks followed by its SHA-256 hash, then returns the single response of the device. The upload must complete within the command timeout of the connection (`ansible_command_timeout`).

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `System.SetPackage`, streaming a local package file to the device.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| local_path {#param-local-path} | path | Package file on the controller. A relative path is resolved against the working directory of ansible-playbook.<br/>**Required:** always |
| package_filename {#param-package-filename} | str | Destination file name on the device. Defaults to the local file name. |
| package_version {#param-package-version} | str | Package version string. |
| package_activate {#param-package-activate} | bool | Activate the package after upload. |

## Examples

```yaml
- name: Upload a package
  nokia.openconfig.gnoi_system_set_package:
    local_path: ./package.tgz
    package_version: '1.0'
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
