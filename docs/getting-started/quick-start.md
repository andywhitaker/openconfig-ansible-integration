# Quick Start

Prepare a router for gRPC, connect to it from Ansible and run a read-only gNMI Get.

!!! tip "Prerequisites"
    Complete the [Installation](installation.md) first. You need a Nokia SR OS or SR Linux router, physical or virtual, that the Ansible controller can reach on the gRPC port.

## Step 1: Enable gRPC on the router

The gRPC server must be enabled with TLS, and the user Ansible logs in with must be allowed to use gRPC. The examples use a TLS server profile named `grpc-tls`; the server certificate and key must already be present on the router.

/// tab | SR OS
Import the server certificate and key into the PKI of the router (`admin system security pki import`), then enable the gRPC server in MD-CLI:

```text
/configure system security tls cert-profile "grpc-certs" admin-state enable
/configure system security tls cert-profile "grpc-certs" entry 1 certificate-file "grpc.crt"
/configure system security tls cert-profile "grpc-certs" entry 1 key-file "grpc.key"
/configure system security tls server-cipher-list "grpc-ciphers" tls13-cipher 1 name tls-aes256-gcm-sha384
/configure system security tls server-cipher-list "grpc-ciphers" tls13-cipher 2 name tls-aes128-gcm-sha256
/configure system security tls server-tls-profile "grpc-tls" admin-state enable
/configure system security tls server-tls-profile "grpc-tls" cert-profile "grpc-certs"
/configure system security tls server-tls-profile "grpc-tls" cipher-list "grpc-ciphers"

/configure system grpc admin-state enable
/configure system grpc tls-server-profile "grpc-tls"
/configure system grpc gnmi admin-state enable
/configure system grpc gnoi file admin-state enable
/configure system grpc gnoi system admin-state enable

/configure system security user-params local-user user "admin" access grpc true
```

The gRPC server of SR OS listens on port `57400`. Enable only the gNOI services you plan to use.
///
/// tab | SR Linux
Create the TLS server profile with the PEM certificate and key, then enable a gRPC server in the management network instance with the gNMI, gNOI and gNSI services:

```text
set / system tls server-profile grpc-tls authenticate-client false
set / system tls server-profile grpc-tls certificate "<PEM certificate>"
set / system tls server-profile grpc-tls key "<PEM private key>"

set / system grpc-server mgmt admin-state enable
set / system grpc-server mgmt network-instance mgmt
set / system grpc-server mgmt port 57400
set / system grpc-server mgmt tls-profile grpc-tls
set / system grpc-server mgmt services [ gnmi gnoi gnsi ]
```

The `admin` user has access to all gRPC services. Other users need an AAA role that allows the services.
///

To use OpenConfig YANG paths in addition to the native models, enable OpenConfig on the router: `/configure system management-interface yang-modules openconfig-modules true` on SR OS, `set / system management openconfig admin-state enable` on SR Linux.

!!! note "Containerlab"
    Nodes deployed with [containerlab](https://containerlab.dev) come with a gRPC server and TLS profile already configured, using a certificate issued by the containerlab CA.

## Step 2: Trust the router certificate

The connection plugin [`nokia.openconfig.grpc`](../reference/nokia.openconfig.grpc.md) verifies the router certificate against a CA bundle on the controller:

| Variable | Purpose |
| --- | --- |
| `ansible_root_certificates_file` | PEM CA bundle that signed the router certificate |
| `ansible_grpc_ssl_target_name_override` | Name to verify when `ansible_host` does not match the certificate |
| `ansible_grpc_validate_certs` | `false` trusts the certificate the router presents at connect time, for labs only |

Without a CA bundle and with `ansible_grpc_validate_certs: false`, the channel is still encrypted, but the router is not authenticated. See the [Security Guide](../guides/security-guide.md) for mutual TLS and credentials.

## Step 3: Inventory

Group the routers by platform, so platform-specific paths can live in group variables:

```yaml
# inventory.yml
all:
  vars:
    ansible_connection: nokia.openconfig.grpc
    ansible_port: 57400
    ansible_user: admin
    ansible_password: "{{ vault_grpc_password }}"
    ansible_root_certificates_file: ./ca.pem
  children:
    nokia_srsim:
      hosts:
        sros1:
          ansible_host: 192.0.2.10
      vars:
        name_path: /configure/system/name
        location_path: /configure/system/location
    nokia_srlinux:
      hosts:
        srl1:
          ansible_host: 192.0.2.20
      vars:
        name_path: /system/name/host-name
        location_path: /system/information/location
```

Store `vault_grpc_password` with [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html).

## Step 4: Write the playbook

```yaml
# quickstart.yml
- name: gNMI quick start
  hosts: all
  gather_facts: false

  tasks:
    - name: Get capabilities
      nokia.openconfig.gnmi_capabilities:
      register: caps

    - name: Show gNMI version and encodings
      ansible.builtin.debug:
        msg: "gNMI {{ caps.gnmi_version }}, encodings {{ caps.encodings }}"

    - name: Get the system name
      nokia.openconfig.gnmi_get:
        path:
          - "{{ name_path }}"
        type: config
        values_only: true
      register: system_name

    - name: Show the system name
      ansible.builtin.debug:
        msg: "{{ system_name.output | from_json | first }}"

    - name: Preview a change of the location
      nokia.openconfig.gnmi_set:
        update:
          - path: "{{ location_path }}"
            value: Antwerp
      check_mode: true
      register: preview

    - name: Show the Set request
      ansible.builtin.debug:
        var: preview.request
```

[`gnmi_capabilities`](../reference/nokia.openconfig.gnmi_capabilities.md) and [`gnmi_get`](../reference/nokia.openconfig.gnmi_get.md) are read-only. In check mode, [`gnmi_set`](../reference/nokia.openconfig.gnmi_set.md) builds the `SetRequest` and returns it without sending it.

## Step 5: Run the playbook

```bash
ansible-playbook -i inventory.yml quickstart.yml --ask-vault-pass
```

If the connection fails, check reachability of the gRPC port, the TLS settings from step 2 and the user access from step 1. Run with `-vvv` to see the connection messages. Standalone clients such as [gNMIc](https://gnmic.openconfig.net) and [gNOIc](https://gnoic.kmrd.dev) are useful to check the router side independently from Ansible.

!!! note "Further reading"
    - [User Guide](../guides/user-guide.md) — Set, Subscribe, backup and restore, confirmed commit, gNOI and gNSI.
    - [Security Guide](../guides/security-guide.md) — TLS, mutual TLS and credentials.
    - [Examples](../examples.md) — integration playbooks of the repository.
