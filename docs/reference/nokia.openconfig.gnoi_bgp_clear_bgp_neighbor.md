# Ansible Module: nokia.openconfig.gnoi_bgp_clear_bgp_neighbor

**Clear a BGP session over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    Reports `changed=true`. In check mode the RPC is not sent and the task is skipped.

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `BGP.ClearBGPNeighbor`.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| address {#param-address} | str | IPv4 or IPv6 neighbor address.<br/>**Required:** always |
| routing_instance {#param-routing-instance} | str | Network instance of the BGP neighbor. |
| mode {#param-mode} | str | Clear mode.<br/>**Choices:** `SOFT`, `SOFTIN`, `HARD_RESET`, `GRACEFUL_RESET` |

## Examples

```yaml
- name: Soft-clear a neighbor in the default network instance (SR Linux)
  nokia.openconfig.gnoi_bgp_clear_bgp_neighbor:
    address: 192.0.2.1
    routing_instance: default
    mode: SOFT
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response message as JSON (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
