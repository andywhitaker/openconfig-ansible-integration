# OpenConfig proto files

---

Contains OpenConfig `*.proto` files (gNMI v0.14.1) and runtime protobuf/gRPC descriptor wrappers (`gnmi_ext_pb2.py`, `gnmi_pb2.py`, `gnmi_pb2_grpc.py`).

`gnmi_ext_pb2.py` and `gnmi_pb2.py` register the serialized `FileDescriptorProto` descriptors into the default protobuf `descriptor_pool` and construct message classes dynamically via `google.protobuf.message_factory`, avoiding `protoc` runtime version lock-in across `protobuf` and `grpcio` releases.
