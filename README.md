![NOKIA](media/logo.png)

---

# Ansible Collection – `nokia.openconfig`

This [collection](https://galaxy.ansible.com/nokia/openconfig) for Ansible by RedHat provides connection plugins and modules to interact with devices that support OpenConfig gRPC API services.

## Status of this project
This collection implements the gRPC Network Management Interface (gNMI) service, version 0.10.0. The gRPC PROTO interface definition is available from [GitHub](https://github.com/openconfig/gnmi/blob/v0.14.1/proto/gnmi/gnmi.proto). The gNMI specification can be found [here](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md). The gNMI extensions Depth, Commit (confirmed commit) and ConfigSubscription are supported.

Please be aware, that the gRPC connection plugin establishes a dedicated, persistent gRPC session. Therefore transport, connectivity and API service are all collapsed into the connection plugin without the need to have a loader for any sort of vendor specific sub-plugins.

Even this project is supposed to be agnostic to vendors and device families, this collection has only been validated against Nokia SR OS and SRLinux nodes running 25.7 release.

As of today, the gNMI modules of this collection only support JSON_IETF (preferred) and JSON encoding. The implementation will run a Capability request during session setup, to determine the list of encodings supported by the networking device (acting as gNMI server). The encoding auto-discovery can be disabled, by setting the required encoding in the playbook, host file or using an environment variable.

## Installation
Distribution is via [ansible-galaxy](https://galaxy.ansible.com/).
To install this collection, please use the following command:
```bash
ansible-galaxy collection install nokia.openconfig
```

If you have already installed a previous version, you can upgrade to the latest version of this collection, by adding the `--force-with-deps` option:
```bash
ansible-galaxy collection install nokia.openconfig --force-with-deps
```

Pre-releases, like 2.0.0-beta.1, are only installed if the version is given explicitly:
```bash
ansible-galaxy collection install 'nokia.openconfig:==2.0.0-beta.1'
```

The connection plugin requires the Python packages `grpcio` and `protobuf` on the Ansible controller, installed into the same Python environment as Ansible (for example the pipx or virtualenv of `ansible-core`). The collection ships the list as `requirements.txt`, which is also used by `ansible-builder` for execution environments:
```bash
pip install 'grpcio>=1.59.0' 'protobuf>=3.20.3'
```

On Python 3.14, `protobuf` must be 5.29.0 or newer. If a dependency is missing or too old, the connection fails with a message that names the problem and the `pip` command to fix it.

## Usage
To use the gNMI modules from this collection, please make sure to set `ansible_connection` variable to `nokia.openconfig.grpc`. Due to the nature of gNMI being vendor agnostic, the `network_os` does not have any impact to the function of this module.

Connection options follow the naming of `ansible.netcommon.grpc`, for example `ansible_root_certificates_file`. The module names and parameters follow the [gNMIc](https://gnmic.openconfig.net) commands and flags, for example `gnmic get --path /system --type config --depth 1` translates into the `nokia.openconfig.gnmi_get` parameters `path`, `type` and `depth`.

Release 2.0.0 removed the connection name `nokia.openconfig.gnmi`, the module name `gnmi_config` and the 1.0.0 option and parameter names. Please check the [CHANGELOG](CHANGELOG.md) for the replacements.

## Requirements
* Ansible Core 2.20 (or newer)
* Python 3.12 (or newer)
* grpcio 1.59.0 (or newer)
* protobuf 3.20.3 (or newer), 5.29.0 (or newer) on Python 3.14

## Supported vendors
Tested with Nokia SR OS and SRLinux

## Playbooks

Please check examples contained in the `tests/playbooks` folder as part of the CI/CD test automation.

## Modules
* gnmi_capabilities
* gnmi_get
* gnmi_set
* gnmi_subscribe
