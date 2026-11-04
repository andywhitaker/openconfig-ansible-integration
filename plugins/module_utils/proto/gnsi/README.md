# OpenConfig gNSI proto files

Services Authz, Certz, Pathz and Credentialz, copied from [openconfig/gnsi](https://github.com/openconfig/gnsi) (commit `6c31586`).

Refresh with `tools/sync_openconfig_protos.sh` (or `tools/sync_openconfig_protos.sh gnsi`), then `tools/build_openconfig_protos.sh`.
See the parent [`../README.md`](../README.md) for clone paths and compilation.

`pathz.proto` imports `gnmi.proto` from the parent proto directory (rewritten from the upstream Go import path during sync).
