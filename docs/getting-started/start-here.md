# Start Here

The collection has more than 40 modules, but most playbooks use four of them. This page maps common tasks to the modules you need, so you can ignore the rest until a task asks for it.

## Pick your task

| I want to… | Module | Notes |
| --- | --- | --- |
| Check what a router supports | [`gnmi_capabilities`](../reference/nokia.openconfig.gnmi_capabilities.md) | gNMI version, encodings and YANG models |
| Read configuration or state | [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) | Read-only, safe in check mode |
| Change configuration safely | [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) | Check mode, `--diff`, `backup`, confirmed commit |
| Take a telemetry sample | [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) | Collects for `duration` seconds and returns |
| Run an operation (ping, file copy, reboot, OS upgrade) | One `gnoi_<service>_<rpc>` module per operation | See [gNOI and gNSI modules](../guides/user-guide.md#gnoi-and-gnsi-modules) |
| Manage device security (authorization, certificates, credentials) | One `gnsi_<service>_<rpc>` module per operation | SR Linux with gNSI enabled |

gNOI and gNSI modules are named after the RPC they send, for example `gnoi_system_ping` sends `System.Ping`. If you know the RPC, you know the module name.

## Set the connection once

Connection settings live in the inventory, not in tasks. A task only says what to read or change:

```yaml
# group_vars/routers.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 57400
ansible_user: admin
ansible_password: "{{ vault_grpc_password }}"
ansible_root_certificates_file: ./ca.pem
ansible_gnmi_origin: openconfig        # optional, origin of all gNMI paths
```

```yaml
- name: Read the hostname
  nokia.openconfig.gnmi_get:
    path: [/system/config/hostname]
```

See [Inventory Patterns](inventory-patterns.md) for ready-made group variables per platform, including routers from other vendors.

## Use a ready-made playbook

The collection ships workflow playbooks, for example a backup, preview and apply sequence for configuration changes. Run them by name after installing the collection:

```bash
ansible-playbook -i inventory.yml nokia.openconfig.safe_config_change -e @change.yml
```

See [Examples](../examples.md#shipped-playbooks) for the list.

## Next steps

1. [Installation](installation.md) — Python requirements and the collection.
2. [Quick Start](quick-start.md) — enable gRPC on the router and run a first playbook.
3. [Inventory Patterns](inventory-patterns.md) — group variables per platform.
4. [User Guide](../guides/user-guide.md) — all options, extensions and workflows.
5. [Platform Notes](../guides/platform-notes.md) — encodings, origins and limits per platform.
