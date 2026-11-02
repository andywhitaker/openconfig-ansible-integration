# OpenConfig gNMI proto files

---

`gnmi.proto` and `gnmi_ext.proto` are taken unmodified from
[openconfig/gnmi](https://github.com/openconfig/gnmi) tag `v0.14.1`
(extracted November 4th, 2025). They declare gNMI service version **0.10.0**
(`option (gnmi_service) = "0.10.0"`), which includes the Depth, Commit
(commit confirmed) and ConfigSubscription extensions.

The only change to `gnmi.proto` is the import path of `gnmi_ext.proto`, which
is flattened so both files compile from this directory.

## Compilation

The generated `*_pb2.py` and `*_pb2_grpc.py` files are not stored in git.
Build them with:

```shell
pip install -r requirements-dev.txt
tools/build_protos.sh
```

The script compiles both protos, rewrites the generated imports to
`ansible_collections.nokia.openconfig.plugins.module_utils.proto`, and prints
the gNMI service version as a check.

Generated code refuses to load with a protobuf runtime older than the protoc
that produced it, and `gnmi_pb2_grpc.py` refuses a grpcio older than the
grpcio-tools that produced it. Release builds therefore use the oldest pinned
`grpcio-tools` from `requirements-dev.txt`, which matches the floors in
`requirements.txt`.
