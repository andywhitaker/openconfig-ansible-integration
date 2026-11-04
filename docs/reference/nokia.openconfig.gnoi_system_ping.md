# Ansible Module: nokia.openconfig.gnoi_system_ping

**Ping from the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Server-streaming RPC. The task sends one request and collects every response message until the device ends the stream, then returns them in R`output`. The task fails if the stream does not end within the command timeout of the connection (`ansible_command_timeout`).

## Synopsis

* Invokes gNOI `System.Ping` and returns one entry per streamed response, the last being the summary.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| destination {#param-destination} | str | Destination address to ping.<br/>**Required:** always |
| source {#param-source} | str | Source address to ping from. |
| count {#param-count} | int | Number of packets. |
| interval {#param-interval} | raw | Time between requests, as Go duration (`500ms`, `1s`) or seconds.<br/>SR OS accepts whole seconds only. |
| wait {#param-wait} | raw | Time to wait for a response, as Go duration or seconds. |
| size {#param-size} | int | Size of the request packet, excluding the ICMP header. |
| do_not_fragment {#param-do-not-fragment} | bool | Set the do-not-fragment bit (IPv4). |
| do_not_resolve {#param-do-not-resolve} | bool | Do not resolve the returned addresses. |
| l3protocol {#param-l3protocol} | str | Layer-3 protocol.<br/>**Choices:** `IPV4`, `IPV6` |
| network_instance {#param-network-instance} | str | Network instance, for example `management` or `Base` on SR OS, `mgmt` or `default` on SR Linux. |

## Examples

```yaml
- name: Ping from the management router (SR OS)
  nokia.openconfig.gnoi_system_ping:
    destination: 192.0.2.1
    network_instance: management
    count: 3
    interval: 1s
  register: ping

- name: Ping from the management network instance (SR Linux)
  nokia.openconfig.gnoi_system_ping:
    destination: 192.0.2.1
    network_instance: mgmt
    count: 3
    interval: 200ms
  register: ping

- name: Show the summary
  ansible.builtin.debug:
    msg: "{{ (ping.output | from_json) | last }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response messages as a JSON list in stream order (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
