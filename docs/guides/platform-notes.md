# Platform Notes

The modules send standard gNMI, gNOI and gNSI messages. What differs between routers is which paths, encodings, subscription modes and services they accept. This page collects those differences in one place.

## Paths and origins

A gNMI path can carry an origin, which names the schema the path belongs to:

| Origin | Schema | Example |
| --- | --- | --- |
| none | Native models of the router | `/interface[name=ethernet-1/1]` on SR Linux, `/configure/system` on SR OS |
| `openconfig` | OpenConfig models | `/interfaces/interface[name=ethernet-1/1]/state` |
| `rfc7951` | YANG models with module-qualified first element | `/Cisco-IOS-XE-native:native/hostname` |

There are three ways to set it, from most to least specific:

1. In the path: `openconfig:/system/config/hostname`.
2. The `origin` option of [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md), [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) and [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md), for all paths of the task.
3. The `ansible_gnmi_origin` variable, for all gNMI tasks of a host. `origin: ""` on a task sends paths without origin.

With a `prefix`, the origin is set on the prefix, because gNMI does not allow it in both prefix and path.

Once an origin is set, a module name on a path element is kept as part of the name, as `rfc7951` paths require. Without any origin, a module name on an element, as in `/oc:lldp`, becomes the origin of the path, which is how the 1.0.0 collection behaved.

## Encodings

The connection reads the encodings from the Capabilities response and prefers `JSON_IETF` over `JSON`. Set `ansible_gnmi_encoding` to skip that request, or `encoding` on a task to override it for one request. `PROTO`, `BYTES` and `ASCII` are not used for Get, Set and Subscribe.

With `JSON_IETF`, routers qualify member names with the YANG module, for example `openconfig-lldp:lldp`, at different levels. The [`nokia.openconfig.strip_yang_prefixes`](#reading-responses) filter removes the prefixes so the same expression works everywhere.

## Reading responses

[`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) and `ONCE` subscriptions return the notifications merged into one tree as a JSON string. Keyed list entries become lists that include their key leaves:

```yaml
- name: Read the OpenConfig LLDP neighbors
  nokia.openconfig.gnmi_get:
    origin: openconfig
    path:
      - /lldp/interfaces/interface/neighbors
  register: lldp

- name: List the interfaces with neighbors
  vars:
    tree: "{{ lldp.output | nokia.openconfig.strip_yang_prefixes }}"
  ansible.builtin.debug:
    msg: "{{ tree.lldp.interfaces.interface | map(attribute='name') }}"
```

Use `values_only: true` when you only need the values of a few leaves.

## Large responses

gRPC limits a received message to 4 MB. A Get of a full configuration or state tree can exceed that. Raise the limit for the hosts that need it:

```yaml
ansible_grpc_channel_options:
  grpc.max_receive_message_length: 67108864   # 64 MB
```

Long operations, such as a Get of a large tree or an OS install, are bounded by `ansible_command_timeout` (default 300 seconds).

## Nokia SR OS

- The gRPC server listens on port `57400`. Enable each gNOI service that you use.
- SR OS advertises `JSON_IETF`, which requires module-qualified member names in container values, for example `nokia-conf:contact`. Without them, SR OS rejects an update with `Missing namespace`. Set `encoding: json` on [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) to send plain names.
- The ConfigSubscription extension is accepted in `STREAM` mode only.
- OpenConfig configuration is returned only for what was configured through OpenConfig; OpenConfig state is always available.
- A full restore with `replace` on `/` from a Get of the router is rejected; use it on SR Linux, or restore subtrees.
- gNOI Ping and Traceroute: intervals in whole seconds, Traceroute over UDP only.

## Nokia SR Linux

- The gRPC server is configured per network instance, usually `mgmt` on port `57400`, with the services `gnmi`, `gnoi` and `gnsi`.
- Top-level `JSON_IETF` members are qualified with the YANG module, for example `srl_nokia-interfaces:interface`.
- gNOI OS runs on hardware platforms only; the simulator rejects the RPCs.
- gNSI requires `gnsi` in the services of the gRPC server.

## Services per platform

| Service | Modules | SR OS | SR Linux |
| --- | --- | --- | --- |
| gNOI System | `gnoi_system_*` (9) | yes | yes |
| gNOI File | `gnoi_file_*` (5) | yes | yes |
| gNOI OS | `gnoi_os_install`, `gnoi_os_activate`, `gnoi_os_verify` | no | hardware |
| gNOI FactoryReset | `gnoi_factory_reset_start` | yes | yes |
| gNOI Healthz | `gnoi_healthz_*` (5) | no | yes |
| gNOI BGP | `gnoi_bgp_clear_bgp_neighbor` | no | yes |
| gNSI Authz, Certz, Pathz, Credentialz | `gnsi_*` (15) | no | yes |

The reference page of each module lists its platforms and validation.

## Other vendors

Routers of other vendors work with the same connection and modules when they implement the OpenConfig gRPC services. They are not part of the validated test matrix. Check these points per platform:

| Topic | What to check |
| --- | --- |
| Port | The gNMI port, for example `9339` (IOS XE, standard gNMI port), `57400` (IOS XR), `50051` (NX-OS), `6030` (Arista EOS) |
| TLS | Most routers use a self-signed certificate by default; export its CA or use `ansible_grpc_validate_certs: false` in a lab |
| Encoding | Usually `JSON_IETF`; Capabilities selects it automatically |
| Origin | `openconfig` for OpenConfig paths; native paths differ per vendor |
| Subscribe | Supported modes, for example `STREAM` only on IOS XE |
| gNOI and gNSI | Which services the router implements; unsupported RPCs return `UNIMPLEMENTED` |

### Cisco IOS XE

- gNMI secure server on port `9339`, encoding `JSON_IETF`.
- OpenConfig paths with origin `openconfig`; native and IETF models with origin `rfc7951` and the module-qualified first element, for example `/Cisco-IOS-XE-native:native/hostname`.
- Subscribe supports `STREAM` with `SAMPLE` and `ON_CHANGE`. Use [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) instead of `ONCE` or `POLL`.
- The default device certificate is self-signed; `ansible_grpc_validate_certs: false` trusts it and verifies against its common name.
- gNOI is served on the gNMI port. Of the gNOI services in this collection, IOS XE implements OS and FactoryReset.

### Cisco IOS XR

- gNMI on the port configured under `grpc`, often `57400`, encoding `JSON_IETF`.
- OpenConfig paths with origin `openconfig`; native paths with the YANG module as first element, for example `/Cisco-IOS-XR-shellutil-oper:system-time/uptime`, which sets the module as origin.

### Cisco NX-OS

- gNMI on port `50051` by default.
- OpenConfig paths with origin `openconfig`; native paths of the device model with origin `device`.
