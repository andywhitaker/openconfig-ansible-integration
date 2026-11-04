# OpenConfig gNOI proto files

---

Sources under this directory are copied from [openconfig/gnoi](https://github.com/openconfig/gnoi)
with import paths flattened for `tools/build_openconfig_protos.sh` (upstream commit `e8e54f7`, OS pinned
to commit `93cdd9ae`). The versions are the `gnoi_version` option of each proto file:

| Service | Proto version |
|---------|---------------|
| System | 1.4.0 |
| File | 0.1.1 |
| OS | 0.1.1 (commit `93cdd9ae`) |
| FactoryReset | 0.1.0 |
| Healthz | 1.3.0 |
| BGP | 0.1.0 |
| Packet Link Qualification | 1.1.0 |

Refresh with `tools/sync_openconfig_protos.sh` (or `tools/sync_openconfig_protos.sh gnoi`), then `tools/build_openconfig_protos.sh`.
See the parent [`../README.md`](../README.md) for clone paths and compilation.

`google/rpc/status.proto` is vendored under `gnoi/google/rpc/` for Packet Link Qualification.
