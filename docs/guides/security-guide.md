# Security Guide

## Transport

Production deployments should use **TLS** with a trusted CA:

```yaml
ansible_connection: nokia.openconfig.grpc
ansible_port: 57400
ansible_root_certificates_file: /path/to/ca.pem
ansible_grpc_ssl_target_name_override: router1.example.com   # when the certificate name ≠ ansible_host
```

When **`ansible_grpc_validate_certs`** is **`false`**, the connection fetches the server certificate at connect time and pins it (intended for **lab / containerlab** only). Do not disable verification in production without a compensating control.

Without a CA bundle, a client certificate or `ansible_grpc_validate_certs: false`, the connection uses a plain-text channel. Use this only for routers that expose an insecure gRPC server for troubleshooting.

### Mutual TLS

When the router authenticates clients by certificate, add the client certificate chain and key:

```yaml
ansible_certificate_chain_file: /path/to/client.pem
ansible_private_key_file: /path/to/client.key
```

Proxy variables can be cleared for gRPC via **`ansible_grpc_environment`** (see connection documentation).

## Credentials

User and password are passed as **gRPC metadata** (`username`, `password`). Prefer **Ansible Vault** for secrets in inventory and group_vars:

```yaml
ansible_password: "{{ vault_device_password }}"
```

Rotate credentials according to your platform policy; the gNSI Credentialz modules, for example [`gnsi_credentialz_rotate_account_credentials`](../reference/nokia.openconfig.gnsi_credentialz_rotate_account_credentials.md), manage credentials on SR Linux.

## gNSI

gNSI modules (**Authz**, **Certz**, **Pathz**, **Credentialz**) manage authorization policy, TLS profiles, path authorization, and credentials on the device. They are **powerful mutating** RPCs—restrict playbook access, use check mode for read-only RPCs where supported, and test rotations in a maintenance window.

Read-only checks, for example [`gnsi_certz_get_profile_list`](../reference/nokia.openconfig.gnsi_certz_get_profile_list.md) and [`gnsi_credentialz_get_public_keys`](../reference/nokia.openconfig.gnsi_credentialz_get_public_keys.md), are suitable for validation playbooks. The policy Get modules [`gnsi_authz_get`](../reference/nokia.openconfig.gnsi_authz_get.md) and [`gnsi_pathz_get`](../reference/nokia.openconfig.gnsi_pathz_get.md) may fail with `FAILED_PRECONDITION` if no active policy exists on the device.

## Controller hardening

- Run Ansible from a dedicated venv or execution image with pinned **`grpcio`** / **`protobuf`** versions (`requirements.txt`).
- Limit who can execute gNOI modules that reboot, reset, or install software, for example [`gnoi_system_reboot`](../reference/nokia.openconfig.gnoi_system_reboot.md), [`gnoi_os_install`](../reference/nokia.openconfig.gnoi_os_install.md) and [`gnoi_factory_reset_start`](../reference/nokia.openconfig.gnoi_factory_reset_start.md).
- Review **`validate_certs: false`** and **`ignore_errors`** in playbooks before promoting to production.

## Reporting security issues

Do **not** open public issues for vulnerabilities. Use [GitHub Security Advisories](https://github.com/nokia-steward/openconfig-ansible-integration/security/advisories) or contact the maintainers privately.
