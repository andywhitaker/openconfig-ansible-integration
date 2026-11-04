# Ansible Module: nokia.openconfig.gnoi_file_get

**Download a file from the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Server-streaming RPC. The task sends one request and collects every response message until the device ends the stream, then returns them in R`output`. The task fails if the stream does not end within the command timeout of the connection (`ansible_command_timeout`).

## Synopsis

* Invokes gNOI `File.Get` and writes the streamed contents to a file on the controller.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| remote_path {#param-remote-path} | str | File on the device, for example `/etc/hostname` on SR Linux or `cf3:/bof.cfg` on SR OS.<br/>**Required:** always |
| local_path {#param-local-path} | path | Destination file on the controller. A relative path is resolved against the working directory of ansible-playbook. Without it only the stream messages are returned. |

## Examples

```yaml
- name: Download the saved configuration (SR OS)
  nokia.openconfig.gnoi_file_get:
    remote_path: cf3:/config.cfg
    local_path: "./{{ inventory_hostname }}.cfg"

- name: Download the saved configuration (SR Linux)
  nokia.openconfig.gnoi_file_get:
    remote_path: /etc/opt/srlinux/config.json
    local_path: "./{{ inventory_hostname }}.json"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response messages as a JSON list in stream order (protobuf JSON names).<br/>**Returned:** success |
| hash {#return-hash} | dict | Hash sent by the device at the end of the stream.<br/>**Returned:** when supported |
| local_path {#return-local-path} | str | File written on the controller.<br/>**Returned:** when [`local_path`](#param-local-path) is set |

*New in version 2.0.0*
