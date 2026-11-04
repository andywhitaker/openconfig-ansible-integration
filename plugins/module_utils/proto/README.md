# OpenConfig gNxI proto files (gNMI, gNOI, gNSI)

---

Protobuf sources for the **`nokia.openconfig.grpc`** connection and modules live under this directory:

| Protocol | Location | Upstream |
|----------|----------|----------|
| **gNMI** 0.10.0 | `gnmi.proto`, `gnmi_ext.proto` | [openconfig/gnmi](https://github.com/openconfig/gnmi) tag **`v0.14.1`** |
| **gNOI** | `gnoi/` | [openconfig/gnoi](https://github.com/openconfig/gnoi) (see `gnoi/README.md`) |
| **gNSI** | `gnsi/` | [openconfig/gnsi](https://github.com/openconfig/gnsi) (see `gnsi/README.md`) |

Import paths are flattened so `grpc_tools.protoc` can compile from this tree. gNSI `pathz.proto` imports `gnmi.proto` from the parent directory.

## Refresh from upstream

Clone the three upstream repositories once (or set `GNMI_SRC`, `GNOI_SRC`, `GNSI_SRC`), then:

```shell
git clone https://github.com/openconfig/gnmi.git  .tmp/gnmi-src
git clone https://github.com/openconfig/gnoi.git  .tmp/gnoi-src
git clone https://github.com/openconfig/gnsi.git  .tmp/gnsi-src

tools/sync_openconfig_protos.sh          # all protocols
tools/sync_openconfig_protos.sh gnmi     # gNMI only
tools/build_openconfig_protos.sh
```

Override gNMI tag with `GNMI_TAG` (default `v0.14.1`). gNOI OS proto is pinned to commit `93cdd9ae` (see `sync_openconfig_protos.sh`).

## Compilation

Generated `*_pb2.py` and `*_pb2_grpc.py` files are not stored in git. Build them with:

```shell
pip install -r requirements-dev.txt
tools/build_openconfig_protos.sh
```

The script compiles gNMI, gNOI, and gNSI, rewrites generated imports to
`ansible_collections.nokia.openconfig.plugins.module_utils.proto`, and prints the gNMI service version as a check.

Release builds use a pinned protoc (grpcio-tools 1.47.5, libprotoc 3.19.5) so generated code works with protobuf 3.20 through 7.x and any grpcio release. Do not regenerate with a newer grpcio-tools.

## Unit tests

Connection unit tests use **`OpenConfigMockServer`** (`tests/unit/plugins/connection/openconfig_mock_server.py`) and **`test_openconfig_grpc.py`**, with gNMI, gNOI, and gNSI on one insecure port.
