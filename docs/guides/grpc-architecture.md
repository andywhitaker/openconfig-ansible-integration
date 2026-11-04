# gRPC Architecture

This page explains how the collection talks to routers, and how its connection plugin relates to the gRPC connection of `ansible.netcommon`.

## Overview

```text
Ansible controller                                                     Router
┌───────────────────────────────────────────────────────────────┐
│ inventory variables ──┐                                       │
│                       ▼                                       │
│ gnmi_* / gnoi_* ──> persistent connection process (per host)  │
│ gnsi_* tasks   socket   nokia.openconfig.grpc                 │
│                         one gRPC channel ─────────────────────┼──> gRPC server
│                                            gNMI, gNOI, gNSI   │    (TLS)
└───────────────────────────────────────────────────────────────┘
```

- Every host gets one persistent connection process, started by the first task and reused by all later tasks of the run. It holds one gRPC channel with TLS and credentials.
- Modules do not open connections. They validate their options and call a method of the connection, for example `gnmiGet` or `invokeGnoi`, through the local socket that Ansible provides for persistent connections.
- The connection builds the protobuf messages, sends them and converts the responses back to JSON. Streams are opened and drained before the task returns, see [Streaming RPCs](user-guide.md#streaming-rpcs).
- At connect, a Capabilities request selects the encoding unless `ansible_gnmi_encoding` is set.

## Relation to ansible.netcommon.grpc

Ansible's network collections include the connection plugin [`ansible.netcommon.grpc`](https://docs.ansible.com/ansible/latest/collections/ansible/netcommon/grpc_connection.html) and the modules `ansible.netcommon.grpc_get` and `ansible.netcommon.grpc_config`. Both collections use the same Ansible mechanism:

| | `nokia.openconfig.grpc` | `ansible.netcommon.grpc` |
| --- | --- | --- |
| Ansible base class | `NetworkConnectionBase`, persistent | `NetworkConnectionBase`, persistent |
| Connection variables | `ansible_host`, `ansible_port`, `ansible_user`, `ansible_password`, `ansible_root_certificates_file`, `ansible_certificate_chain_file`, `ansible_private_key_file`, `ansible_grpc_ssl_target_name_override` | Same names |
| Timeouts | `ansible_connect_timeout`, `ansible_command_timeout` | Same names |
| Protocol logic | In the connection plugin, from the OpenConfig protos | In a platform sub-plugin, loaded by `ansible_network_os` or `grpc_type` |
| Services | gNMI, gNOI and gNSI on one channel | What the platform sub-plugin implements |
| Modules | One module per RPC, options are request fields | `grpc_get` and `grpc_config` with `section` and `command` options, mapped by the sub-plugin |

The difference is where the protocol lives. `ansible.netcommon.grpc` is a framework: it opens the channel and delegates every call to a sub-plugin at `<namespace>.<collection>.plugins.sub_plugins.grpc.<platform>`, which a platform collection has to provide. The sub-plugins that exist implement the vendor-specific gRPC services of their platform, not the OpenConfig services, and there is no generic sub-plugin for gNMI. Without a sub-plugin for the platform, the connection fails with `unable to load API plugin for network_os`.

OpenConfig gRPC services are the same on every platform, so this collection implements them once, in the connection plugin itself:

- One channel serves gNMI, gNOI and gNSI, so a playbook can read state, change configuration, ping and rotate certificates without reconnecting.
- gNMI extensions (Depth, Commit, ConfigSubscription), Subscribe modes and gNOI/gNSI streaming patterns need RPC-specific handling, which a generic `section`/`command` interface cannot express.
- No `ansible_network_os` is needed: platform differences are paths, origins and encodings, which tasks and inventory variables set explicitly.

The connection variables keep the `ansible.netcommon.grpc` names, so inventories can be shared, and moving a host between the two plugins only changes `ansible_connection`.

## Where to look in the code

| Path | Content |
| --- | --- |
| `plugins/connection/grpc.py` | Channel, TLS, credentials, encoding selection, one method per gNMI RPC, gNOI and gNSI dispatch |
| `plugins/module_utils/gnmi.py` | Path, value and request encoding, response merging, without gRPC dependencies |
| `plugins/module_utils/gnmi_module.py` | `Rpc`, the module side of the socket call |
| `plugins/module_utils/gnxi_module.py` | Shared runner of the generated gNOI and gNSI modules |
| `plugins/action/gnmi_set.py` | Controller side of `gnmi_set`: request files and backup files |

The [Developer Guide](developer-guide.md) describes the streaming implementation, the module generator and the mock server used by the unit tests.
