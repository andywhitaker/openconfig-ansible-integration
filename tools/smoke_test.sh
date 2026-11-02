#!/usr/bin/env bash
#
#    smoke_test.sh — Install a built collection tarball and check it loads
#
#    Usage:
#      tools/smoke_test.sh <nokia-openconfig-X.Y.Z.tar.gz>
#
#    Fails if the tarball is missing the generated protobuf modules, if they
#    do not import with the installed grpcio/protobuf, or if ansible-doc
#    cannot load the plugins.
#

set -euo pipefail

TARBALL="${1:?usage: smoke_test.sh <collection tarball>}"
DEST="$(mktemp -d)"
trap 'rm -rf "$DEST"' EXIT

ansible-galaxy collection install --force -p "$DEST" "$TARBALL"

for f in gnmi_pb2.py gnmi_pb2_grpc.py gnmi_ext_pb2.py; do
  if [[ ! -f "$DEST/ansible_collections/nokia/openconfig/plugins/module_utils/proto/$f" ]]; then
    echo "missing generated file $f in $TARBALL" >&2
    exit 1
  fi
done

PYTHONPATH="$DEST" python - << 'EOF'
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2, gnmi_pb2_grpc, gnmi_ext_pb2  # noqa: F401

version = gnmi_pb2.DESCRIPTOR.GetOptions().Extensions[gnmi_pb2.gnmi_service]
assert version == "0.10.0", version
print("generated protobuf modules import, gNMI service version %s" % version)

from ansible_collections.nokia.openconfig.plugins.connection import grpc
assert grpc.HAS_GRPC and grpc.HAS_PROTOBUF and grpc.HAS_GNMI_PB2, "connection plugin cannot import its dependencies"
print("connection plugin imports grpcio, protobuf and the generated modules")
EOF

export ANSIBLE_COLLECTIONS_PATH="$DEST"
ansible-doc -t connection nokia.openconfig.grpc > /dev/null
for m in gnmi_capabilities gnmi_get gnmi_set gnmi_subscribe; do
  ansible-doc "nokia.openconfig.$m" > /dev/null
done
echo "ansible-doc loads the connection plugin and all modules"
