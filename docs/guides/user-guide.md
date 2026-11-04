# User Guide

## Connection plugin

Set `ansible_connection: nokia.openconfig.grpc`. The [`nokia.openconfig.grpc`](../reference/nokia.openconfig.grpc.md) connection opens one persistent gRPC channel per host, and all gNMI, gNOI and gNSI modules reuse it through the Ansible persistent connection.

Commonly used variables (see the [reference](../reference/nokia.openconfig.grpc.md) for the full list):

| Variable | Purpose |
| --- | --- |
| `ansible_host` / `ansible_port` | Address and gRPC port of the router (default `57400`) |
| `ansible_user` / `ansible_password` | Credentials, sent as gRPC metadata `username` and `password` |
| `ansible_root_certificates_file` | PEM CA bundle to verify the router certificate |
| `ansible_grpc_ssl_target_name_override` | Name to verify when `ansible_host` does not match the router certificate |
| `ansible_grpc_validate_certs` | `false` trusts the certificate the router presents at connect time (lab only) |
| `ansible_gnmi_encoding` | `JSON` or `JSON_IETF`, instead of selecting the encoding from the Capabilities response |

The channel uses TLS when a CA bundle or client certificate is configured, or when `ansible_grpc_validate_certs` is `false`. Otherwise it is a plain-text channel. `ansible_network_os` is not used: paths, models and encodings are explicit in the module options.

## gNMI modules

There is one module per gNMI RPC. Option names are the field names of the request messages in the [gNMI specification](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md), in snake_case:

| RPC | Module | Main options |
| --- | --- | --- |
| [Capabilities](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md#32-capability-discovery) | [`gnmi_capabilities`](../reference/nokia.openconfig.gnmi_capabilities.md) | none |
| [Get](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md#33-retrieving-snapshots-of-state-information) | [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) | `path`, `prefix`, `type`, `encoding`, `depth`, `values_only` |
| [Set](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md#34-modifying-state) | [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) | `update`, `replace`, `delete`, `request_file`, commit options, `backup` |
| [Subscribe](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md#35-subscribing-to-telemetry-updates) | [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) | `path`, `subscription`, `mode`, `stream_mode`, `sample_interval`, `duration`, `config_subscription` |

Paths are gNMI path strings such as `/interface[name=ethernet-1/1]/description`. A path can name its origin, for example `openconfig:/interfaces/interface[name=ethernet-1/1]`.

### Extensions

| Extension | Module | Options |
| --- | --- | --- |
| [Depth](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-depth.md) | [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md), [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) | `depth` |
| [Commit (confirmed commit)](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-commit-confirmed.md) | [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) | `commit_id`, `commit_request`, `commit_confirm`, `commit_cancel`, `rollback_duration` |
| [ConfigSubscription](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-config-subscriptions.md) | [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) | `config_subscription`; extension data is returned in `extensions` |

### Backup, check mode and diff

These apply to [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md):

- `backup: true` reads the full configuration before the change and writes it to a file on the controller, like the `*_config` modules of other network collections. To restore, send the file content with `replace` on path `/`. The full restore is validated on SR Linux, see [gNMI_Restore_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Restore_SRL.yml).
- In check mode the `SetRequest` is built and returned without sending it, and the task reports `changed: false`. [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) is skipped in check mode; use [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) for read-only checks.
- With `--diff`, a task that changes the configuration returns `diff.before` and `diff.after` as JSON strings.

### SR OS notes

- SR OS advertises the `JSON_IETF` encoding, which requires member names qualified with the YANG module in container values, for example `nokia-conf:contact`. Without them, SR OS rejects an update with `Missing namespace`. Set `encoding: json` on [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) to send plain member names.
- SR OS accepts the ConfigSubscription extension in `STREAM` mode only.

## gNOI and gNSI modules

There is one module per RPC, named `gnoi_<service>_<rpc>` and `gnsi_<service>_<rpc>` in snake_case. Options are the fields of the RPC request message in snake_case. Paths take gNMI path strings, and durations take values such as `500ms` or `2s`.

```yaml
- name: Ping from the management network instance
  nokia.openconfig.gnoi_system_ping:
    destination: 192.0.2.1
    network_instance: mgmt
    count: 3
  register: ping
```

The collection ships modules for the services below. See the module reference for the platforms, options and behaviour of each RPC.

| Service | Modules | SR OS | SR Linux |
| --- | --- | --- | --- |
| gNOI System | [`time`](../reference/nokia.openconfig.gnoi_system_time.md), [`ping`](../reference/nokia.openconfig.gnoi_system_ping.md), [`traceroute`](../reference/nokia.openconfig.gnoi_system_traceroute.md), [`reboot`](../reference/nokia.openconfig.gnoi_system_reboot.md), [`cancel_reboot`](../reference/nokia.openconfig.gnoi_system_cancel_reboot.md), [`reboot_status`](../reference/nokia.openconfig.gnoi_system_reboot_status.md), [`switch_control_processor`](../reference/nokia.openconfig.gnoi_system_switch_control_processor.md), [`kill_process`](../reference/nokia.openconfig.gnoi_system_kill_process.md), [`set_package`](../reference/nokia.openconfig.gnoi_system_set_package.md) | yes | yes |
| gNOI File | [`get`](../reference/nokia.openconfig.gnoi_file_get.md), [`put`](../reference/nokia.openconfig.gnoi_file_put.md), [`stat`](../reference/nokia.openconfig.gnoi_file_stat.md), [`remove`](../reference/nokia.openconfig.gnoi_file_remove.md), [`transfer_to_remote`](../reference/nokia.openconfig.gnoi_file_transfer_to_remote.md) | yes | yes |
| gNOI OS | [`install`](../reference/nokia.openconfig.gnoi_os_install.md), [`activate`](../reference/nokia.openconfig.gnoi_os_activate.md), [`verify`](../reference/nokia.openconfig.gnoi_os_verify.md) | no | yes |
| gNOI FactoryReset | [`start`](../reference/nokia.openconfig.gnoi_factory_reset_start.md) | yes | yes |
| gNOI Healthz | [`get`](../reference/nokia.openconfig.gnoi_healthz_get.md), [`list`](../reference/nokia.openconfig.gnoi_healthz_list.md), [`acknowledge`](../reference/nokia.openconfig.gnoi_healthz_acknowledge.md), [`check`](../reference/nokia.openconfig.gnoi_healthz_check.md), [`artifact`](../reference/nokia.openconfig.gnoi_healthz_artifact.md) | no | yes |
| gNOI BGP | [`clear_bgp_neighbor`](../reference/nokia.openconfig.gnoi_bgp_clear_bgp_neighbor.md) | no | yes |
| gNSI Authz | [`get`](../reference/nokia.openconfig.gnsi_authz_get.md), [`probe`](../reference/nokia.openconfig.gnsi_authz_probe.md), [`rotate`](../reference/nokia.openconfig.gnsi_authz_rotate.md) | no | yes |
| gNSI Certz | [`get_profile_list`](../reference/nokia.openconfig.gnsi_certz_get_profile_list.md), [`add_profile`](../reference/nokia.openconfig.gnsi_certz_add_profile.md), [`delete_profile`](../reference/nokia.openconfig.gnsi_certz_delete_profile.md), [`can_generate_csr`](../reference/nokia.openconfig.gnsi_certz_can_generate_csr.md), [`rotate`](../reference/nokia.openconfig.gnsi_certz_rotate.md) | no | yes |
| gNSI Pathz | [`get`](../reference/nokia.openconfig.gnsi_pathz_get.md), [`probe`](../reference/nokia.openconfig.gnsi_pathz_probe.md), [`rotate`](../reference/nokia.openconfig.gnsi_pathz_rotate.md) | no | yes |
| gNSI Credentialz | [`get_public_keys`](../reference/nokia.openconfig.gnsi_credentialz_get_public_keys.md), [`can_generate_key`](../reference/nokia.openconfig.gnsi_credentialz_can_generate_key.md), [`rotate_account_credentials`](../reference/nokia.openconfig.gnsi_credentialz_rotate_account_credentials.md), [`rotate_host_parameters`](../reference/nokia.openconfig.gnsi_credentialz_rotate_host_parameters.md) | no | yes |

Read-only RPCs run in check mode and report `changed: false`. All other RPCs are skipped in check mode and report `changed: true` when they run.

## Streaming RPCs

An Ansible task runs once and returns. The connection plugin therefore opens, feeds and drains every stream before the task returns, and no module exposes an open stream:

| Pattern | Examples | What the task does |
| --- | --- | --- |
| Unary | [`gnoi_system_time`](../reference/nokia.openconfig.gnoi_system_time.md), [`gnsi_pathz_get`](../reference/nokia.openconfig.gnsi_pathz_get.md) | One request, one response in `output`. |
| Server streaming | [`gnoi_system_ping`](../reference/nokia.openconfig.gnoi_system_ping.md), [`gnoi_file_get`](../reference/nokia.openconfig.gnoi_file_get.md), [`gnoi_healthz_artifact`](../reference/nokia.openconfig.gnoi_healthz_artifact.md) | Collects the response messages until the router ends the stream. |
| Client streaming | [`gnoi_file_put`](../reference/nokia.openconfig.gnoi_file_put.md), [`gnoi_system_set_package`](../reference/nokia.openconfig.gnoi_system_set_package.md) | Streams a local file to the router and returns the single response. |
| Bidirectional streaming | [`gnoi_os_install`](../reference/nokia.openconfig.gnoi_os_install.md), [`gnsi_certz_rotate`](../reference/nokia.openconfig.gnsi_certz_rotate.md) | Sends the request sequence and collects the server messages until the RPC ends. |
| gNMI Subscribe | [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) | Collects notifications until the subscription completes or `duration` expires. |

The module reference describes for each streaming module when the task completes and which messages it sends.

## Idempotency and `changed`

- [`gnmi_capabilities`](../reference/nokia.openconfig.gnmi_capabilities.md), [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) and [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md) report `changed: false`.
- [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) compares configuration snapshots of the affected paths, or of the full configuration with `backup: true`, to set `changed`.
- Commit-only operations (`commit_confirm`, `commit_cancel`) may report `changed: true` when run again; treat the commit ID as workflow state.
- gNOI and gNSI modules report `changed: true` for RPCs that change the router, and `changed: false` for read-only RPCs.

## Migration from 1.0.0

Release 2.0.0 removes the `nokia.openconfig.gnmi` connection, the `gnmi_config` module and legacy option names. Use [`nokia.openconfig.grpc`](../reference/nokia.openconfig.grpc.md) and [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) instead. See the [CHANGELOG](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/CHANGELOG.md) for details.
