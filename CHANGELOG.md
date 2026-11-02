# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0-beta.1] - Unreleased

Modules now follow the gNMIc commands and flags, and the connection follows `ansible.netcommon.grpc`. This is a breaking release: the 1.0.0 connection, module, option and parameter names were removed. See "Removed" below for the replacements.

### Added
- Connection plugin `nokia.openconfig.grpc`, which replaces `nokia.openconfig.gnmi`. The new name leaves room for gNOI and gNSI.
- gNMI 0.10.0 protos (gnmi v0.14.1), compiled by `tools/build_protos.sh` with a pinned protoc 3.19.5 (grpcio-tools 1.47.5), so the generated code works with protobuf 3.20.3 up to 7.x and any grpcio release.
- Depth extension: `depth` on `gnmi_get` and `gnmi_subscribe`.
- Commit extension (confirmed commit) on `gnmi_set`: `commit_id`, `commit_request`, `commit_confirm`, `commit_cancel`, `rollback_duration`.
- ConfigSubscription extension: `config_subscription` on `gnmi_subscribe`. In `STREAM` mode it waits for the next sync-done.
- Response extensions are returned as `extensions`, using protobuf field names.
- `gnmi_get`: `target`, `model`, `encoding`, `values_only`.
- `gnmi_set`: `target`, `encoding`, per-item `encoding`, `request_file` (gNMIc set-request file), `dry_run`, check mode, and `diff`.
- `gnmi_subscribe`:
  - `path` with `stream_mode`, `sample_interval`, `heartbeat_interval` and `suppress_redundant` (gNMIc flags).
  - `POLL` mode, `target`, `model`, `encoding`.
- `gnmi_capabilities` returns `gnmi_version`, `encodings`, `models` and `extensions` next to the raw `output`.
- Connection options:
  - `ssl_target_name_override`.
  - `[defaults]` and `[persistent_connection]` ini and `ANSIBLE_*` environment sources for port, user and timeouts.
  - `persistent_command_timeout` is used as the gRPC deadline for Capabilities, Get and Set.
- Unit tests with a fake gNMI server, and `ansible-test sanity` and `units` in CI on ansible-core 2.20, 2.21 and 2.22.
- Integration test categories `depth`, `commit_confirmed` and `config_subscription`. They check that each extension takes effect, so a server that silently ignores it fails the test. Every playbook now asserts its results.
- `run.sh units`, `run.sh sanity` and `run.sh integration`, plus JUnit and Markdown reports.
- CI integration job on containerlab: SR Linux always, and SR OS when the `SRSIM_LICENSE` secret is set. A weekly `devel` workflow runs sanity and units.

### Changed
- `gnmi_config` is renamed to `gnmi_set`.
- `gnmi_get` `type` defaults to `ALL` instead of `CONFIG`, matching gNMIc.
- `gnmi_subscribe` `mode` defaults to `STREAM` instead of `ONCE`, matching gNMIc.
- Connection options are renamed to the `ansible.netcommon.grpc` names, and the ini section is now `[grpc_connection]`.
- Supported versions are ansible-core 2.20 or newer and controller Python 3.12 or newer. `grpcio` must be 1.59.0 or newer and `protobuf` 3.20.3 or newer (5.29.0 or newer on Python 3.14).
- A missing, too old or broken `grpcio` or `protobuf` fails with a message that names the problem, the Python interpreter and the `pip` command to fix it.
- `meta/execution-environment.yml` points `ansible-builder` to `requirements.txt`.
- The protos and generated code moved to `plugins/module_utils/proto`. The unused `collector.proto` and `target.proto` were dropped.
- gRPC errors are reported as `gRPC <CODE>: <details>`.

### Removed
The 1.0.0 names below were removed. Playbooks using the old connection or module name fail with a message that names the replacement, and so do the old `gnmi_set` and `gnmi_subscribe` keys.
- Connection `nokia.openconfig.gnmi`. Use `nokia.openconfig.grpc`.
- Module `nokia.openconfig.gnmi_config`. Use `nokia.openconfig.gnmi_set`.
- 1.0.0 connection option names:
  - `ansible_root_ca_cert`. Use `ansible_root_certificates_file`.
  - `ansible_cert_chain` and `ANSIBLE_CERT_CHAIN`. Use `ansible_certificate_chain_file` and `ANSIBLE_CERTIFICATE_CHAIN_FILE`.
  - `ansible_channel_options`. Use `ansible_grpc_channel_options`.
  - `ansible_grpc_env`. Use `ansible_grpc_environment`.
  - The `[grpc]` ini section. Use `[grpc_connection]` with the keys `root_certificates_file`, `certificate_chain_file`, `private_key_file`, `gnmi_encoding`, `grpc_channel_options` and `grpc_environment`.
- `gnmi_set` item key `val`. Use `value`.
- `gnmi_subscribe` subscription keys `mode`, `sampleInterval`, `heartbeatInterval` and `suppressRedundant`. Use `stream_mode`, `sample_interval`, `heartbeat_interval` and `suppress_redundant`.
- Connection option `certificate_path` from `nokia.grpc`. Certificate options take a file path.

### Fixed
- IPv6 management addresses: `ansible_host: 2001:db8::1` failed to connect because the address was not put in brackets. Both forms, with and without brackets, now work.
- Release tarballs did not contain the compiled protos, so the connection plugin could not be imported.
- Subscribe results were truncated at the first response without updates, for example a ConfigSubscription sync-done.
- Path origins were lost when decoding responses.
- `depth: 0` and `false` values were silently dropped from requests.
- A missing certificate file now fails with a clear error.
- Source file lookup in the shared network action code did not detect URLs or role-relative paths.
- Re-enabled the Restore integration test.
- `run.sh` no longer reports success when an inventory group has no hosts.
- The SR Linux image in the lab topologies used the SR OS version variable.
- `galaxy.yml` repository, documentation and issue URLs.

## [1.0.0]
### Added
- Renamed Ansible collection from `nokia.grpc` to `nokia.openconfig`
- Dedicated GitHub repository for `nokia.openconfig` for simplified release management and CI/CD
- Containerlab topology for test-automation
- GitHub workflow to build collection for every new release
- Updated playbooks for compatibility with latest Ansible releases
