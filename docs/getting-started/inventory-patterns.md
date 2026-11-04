# Inventory Patterns

Everything that depends on the router platform — port, TLS, encoding and path origin — belongs in group variables. Tasks and shipped playbooks then stay the same for every platform. Copy the group that matches your routers and adjust addresses and credentials.

The same files are shipped with the collection under `playbooks/examples/`, together with an example inventory.

## Variables you set once

| Variable | Purpose | Default |
| --- | --- | --- |
| `ansible_connection` | Always `nokia.openconfig.grpc` | — |
| `ansible_host`, `ansible_port` | Address and gRPC port | inventory name, `57400` |
| `ansible_user`, `ansible_password` | Credentials, sent as gRPC metadata | — |
| `ansible_root_certificates_file` | CA bundle that signed the router certificate | — |
| `ansible_grpc_validate_certs` | `false` trusts the certificate presented at connect time (labs only) | `true` |
| `ansible_grpc_ssl_target_name_override` | Certificate name to verify when it differs from `ansible_host` | — |
| `ansible_gnmi_encoding` | `JSON` or `JSON_IETF`; otherwise taken from Capabilities | Capabilities |
| `ansible_gnmi_origin` | Origin of gNMI paths that do not name one | none |
| `ansible_grpc_channel_options` | gRPC channel options, for example a larger message size | — |

See the [connection reference](../reference/nokia.openconfig.grpc.md) for all options.

## Nokia SR Linux

```yaml
# group_vars/nokia_srlinux.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 57400
ansible_user: admin
ansible_password: "{{ vault_srl_password }}"
ansible_root_certificates_file: ./certs/ca.pem
```

Native SR Linux paths need no origin, for example `/interface[name=ethernet-1/1]/description`. For OpenConfig, enable it on the router and set `origin: openconfig` on the task, or `ansible_gnmi_origin: openconfig` for hosts that are managed through OpenConfig only.

## Nokia SR OS

```yaml
# group_vars/nokia_sros.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 57400
ansible_user: admin
ansible_password: "{{ vault_sros_password }}"
ansible_root_certificates_file: ./certs/ca.pem
```

Native SR OS paths start with `/configure` or `/state`. SR OS expects module-qualified member names in `JSON_IETF` container values; set `encoding: json` on [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) to send plain names. See [Platform Notes](../guides/platform-notes.md#nokia-sr-os).

## Other gNMI routers

The connection and the gNMI modules implement the OpenConfig specifications, so routers from other vendors work with the same tasks once the connection is configured. They are not part of the validated test matrix; see [Platform Notes](../guides/platform-notes.md#other-vendors) for what to check.

### Generic

```yaml
# group_vars/generic_gnmi.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 6030                      # the gNMI port of the router
ansible_user: admin
ansible_password: "{{ vault_gnmi_password }}"
ansible_root_certificates_file: ./certs/ca.pem
ansible_gnmi_origin: openconfig
```

### Cisco IOS XE

```yaml
# group_vars/cisco_iosxe.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 9339                      # gNMI secure server
ansible_user: admin
ansible_password: "{{ vault_iosxe_password }}"
ansible_root_certificates_file: ./certs/iosxe-ca.pem
ansible_gnmi_encoding: JSON_IETF
ansible_gnmi_origin: openconfig
```

Native models use the origin `rfc7951` with the module-qualified first element. Override the host default on the task:

```yaml
- name: Read the hostname from the native model
  nokia.openconfig.gnmi_get:
    origin: rfc7951
    path:
      - /Cisco-IOS-XE-native:native/hostname
    type: config
```

IOS XE supports Subscribe in `STREAM` mode only; use [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) for snapshots.

### Cisco IOS XR

```yaml
# group_vars/cisco_iosxr.yml
ansible_connection: nokia.openconfig.grpc
ansible_port: 57400                     # the port configured under "grpc"
ansible_user: admin
ansible_password: "{{ vault_iosxr_password }}"
ansible_root_certificates_file: ./certs/iosxr-ca.pem
```

OpenConfig paths take the origin `openconfig`. Native paths are written with the YANG module as first element, for example `/Cisco-IOS-XR-shellutil-oper:system-time/uptime`, without an `origin` option: the module name becomes the origin, which IOS XR accepts.

## Lab routers with self-signed certificates

```yaml
ansible_grpc_validate_certs: false
```

The channel stays encrypted, but the router is not authenticated: the connection reads the certificate the router presents and trusts it for this connection, and uses its common name as `ssl_target_name_override`. Use a CA bundle in production. See the [Security Guide](../guides/security-guide.md#tls-modes).

## Defaults per play

Variables apply per host. To set module options for all gNMI tasks of a play instead, use `module_defaults` with the action group `group/nokia.openconfig.gnmi`, which contains [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md), [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) and [`gnmi_subscribe`](../reference/nokia.openconfig.gnmi_subscribe.md):

```yaml
- name: OpenConfig maintenance
  hosts: routers
  gather_facts: false
  module_defaults:
    group/nokia.openconfig.gnmi:
      origin: openconfig
      encoding: json_ietf
  tasks:
    - name: Read the hostname
      nokia.openconfig.gnmi_get:
        path: [/system/config/hostname]
```

`module_defaults` is a play, block or task keyword; it cannot be set in group variables.
