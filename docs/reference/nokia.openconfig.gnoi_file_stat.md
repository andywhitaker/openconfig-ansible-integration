# Ansible Module: nokia.openconfig.gnoi_file_stat

**Get file metadata from the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

## Synopsis

* Invokes gNOI `File.Stat` for a file or directory.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| remote_path {#param-remote-path} | str | File or directory on the device, for example `/tmp` on SR Linux or `cf3:/` on SR OS.<br/>**Required:** always |

## Examples

```yaml
- name: List the root of the compact flash (SR OS)
  nokia.openconfig.gnoi_file_stat:
    remote_path: cf3:/
  register: files

- name: List the configuration directory (SR Linux)
  nokia.openconfig.gnoi_file_stat:
    remote_path: /etc/opt/srlinux
  register: files

- name: Show the file names
  ansible.builtin.debug:
    msg: "{{ (files.output | from_json).stats | map(attribute='path') | list }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
