# Ansible Module: nokia.openconfig.gnoi_system_traceroute

**Traceroute from the device over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR OS and SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Server-streaming RPC. The task sends one request and collects every response message until the device ends the stream, then returns them in R`output`. The task fails if the stream does not end within the command timeout of the connection (`ansible_command_timeout`).

## Synopsis

* Invokes gNOI `System.Traceroute` and returns one entry per streamed hop response.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| destination {#param-destination} | str | Destination address.<br/>**Required:** always |
| source {#param-source} | str | Source address. |
| initial_ttl {#param-initial-ttl} | int | Initial TTL. |
| max_ttl {#param-max-ttl} | int | Maximum number of hops. |
| wait {#param-wait} | raw | Time to wait for a response, as Go duration or seconds. |
| do_not_fragment {#param-do-not-fragment} | bool | Set the do-not-fragment bit (IPv4). |
| do_not_resolve {#param-do-not-resolve} | bool | Do not resolve the returned addresses. |
| l3protocol {#param-l3protocol} | str | Layer-3 protocol.<br/>**Choices:** `IPV4`, `IPV6` |
| l4protocol {#param-l4protocol} | str | Probe protocol. SR OS only supports `UDP`.<br/>**Choices:** `ICMP`, `TCP`, `UDP` |
| do_not_lookup_asn {#param-do-not-lookup-asn} | bool | Do not look up the ASN of each hop. |
| network_instance {#param-network-instance} | str | Network instance to trace in, for example `Base` on SR OS or `default` on SR Linux. |

## Examples

```yaml
- name: Traceroute in the base router (SR OS)
  nokia.openconfig.gnoi_system_traceroute:
    destination: 192.0.2.1
    network_instance: Base
    l4protocol: UDP
    max_ttl: 5
    wait: 1s

- name: Traceroute in the default network instance (SR Linux)
  nokia.openconfig.gnoi_system_traceroute:
    destination: 192.0.2.1
    network_instance: default
    max_ttl: 5
    wait: 1s
    do_not_resolve: true
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response messages as a JSON list in stream order (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
