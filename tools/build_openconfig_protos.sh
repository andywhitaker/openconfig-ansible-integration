#!/usr/bin/env bash
#
#    build_openconfig_protos.sh — Compile OpenConfig gNMI, gNOI, and gNSI protos
#
#    Usage:
#      tools/build_openconfig_protos.sh [--python <interpreter>]
#
#    Generates *_pb2.py and *_pb2_grpc.py under plugins/module_utils/proto
#    (gNMI at the repo root of that tree, gNOI in gnoi/, gNSI in gnsi/) and
#    rewrites imports to the collection namespace. Refresh .proto sources with
#    tools/sync_openconfig_protos.sh before rebuilding when updating from upstream.
#
#    The code is generated with an old protoc (grpcio-tools 1.47.5, libprotoc
#    3.19.5) so that the published collection works with protobuf 3.20 up to
#    the latest runtime, and with any grpcio release. By default this pinned
#    toolchain runs in a cached uv environment (Python 3.10, wheels only).
#    --python uses an interpreter that already has grpcio-tools installed; it
#    must bundle the same protoc version.
#

set -euo pipefail

GRPCIO_TOOLS="grpcio-tools==1.47.5"
PROTOC_VERSION="3.19.5"
BUILD_PYTHON="3.10"

PYTHON=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --python) PYTHON="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -n "$PYTHON" ]]; then
  if [[ "$PYTHON" == */* ]]; then
    PYTHON="$(cd "$(dirname "$PYTHON")" && pwd)/$(basename "$PYTHON")"
  else
    PYTHON="$(command -v "$PYTHON")"
  fi
  RUN=("$PYTHON")
elif command -v uv >/dev/null; then
  # setuptools provides pkg_resources, which grpc_tools 1.47 imports.
  export PYTHONWARNINGS="ignore::DeprecationWarning"
  RUN=(uv run --quiet --no-project --no-build --python "$BUILD_PYTHON"
       --with "$GRPCIO_TOOLS" --with "setuptools<70" python)
else
  echo "uv is required to run the pinned protoc toolchain ($GRPCIO_TOOLS)." >&2
  echo "Install uv (https://docs.astral.sh/uv/) or pass --python <interpreter with $GRPCIO_TOOLS>." >&2
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO_DIR="$ROOT/plugins/module_utils/proto"

cd "$PROTO_DIR"

PROTOC="$("${RUN[@]}" -m grpc_tools.protoc --version)"
if [[ "$PROTOC" != "libprotoc $PROTOC_VERSION" ]]; then
  echo "Found $PROTOC, expected libprotoc $PROTOC_VERSION ($GRPCIO_TOOLS)." >&2
  echo "Newer protoc versions generate code that older protobuf runtimes cannot import." >&2
  exit 1
fi
echo "using $PROTOC"

rm -f ./*_pb2.py ./*_pb2_grpc.py

"${RUN[@]}" -m grpc_tools.protoc -I . \
  --python_out=. --grpc_python_out=. \
  gnmi.proto gnmi_ext.proto

# gnmi_ext.proto defines no services; its gRPC stub module is empty.
rm -f gnmi_ext_pb2_grpc.py

GNOI_DIR="$PROTO_DIR/gnoi"
if [[ -d "$GNOI_DIR" ]] && [[ -f "$GNOI_DIR/types.proto" ]]; then
  rm -f "$GNOI_DIR"/*_pb2.py "$GNOI_DIR"/*_pb2_grpc.py
  rm -f "$GNOI_DIR/google/rpc/"*_pb2.py "$GNOI_DIR/google/rpc/"*_pb2_grpc.py 2>/dev/null || true
  if [[ -f "$GNOI_DIR/google/rpc/status.proto" ]]; then
    "${RUN[@]}" -m grpc_tools.protoc -I "$GNOI_DIR" \
      --python_out="$GNOI_DIR" --grpc_python_out="$GNOI_DIR" \
      "$GNOI_DIR/google/rpc/status.proto"
  fi
  "${RUN[@]}" -m grpc_tools.protoc -I "$GNOI_DIR" \
    --python_out="$GNOI_DIR" --grpc_python_out="$GNOI_DIR" \
    "$GNOI_DIR/types.proto" \
    "$GNOI_DIR/common.proto" \
    "$GNOI_DIR/system.proto" \
    "$GNOI_DIR/file.proto" \
    "$GNOI_DIR/os.proto" \
    "$GNOI_DIR/factory_reset.proto" \
    "$GNOI_DIR/healthz.proto" \
    "$GNOI_DIR/bgp.proto" \
    "$GNOI_DIR/packet_link_qualification.proto"
  rm -f "$GNOI_DIR/types_pb2_grpc.py"
fi

GNSI_DIR="$PROTO_DIR/gnsi"
if [[ -d "$GNSI_DIR" ]] && [[ -f "$GNSI_DIR/authz.proto" ]]; then
  rm -f "$GNSI_DIR"/*_pb2.py "$GNSI_DIR"/*_pb2_grpc.py
  "${RUN[@]}" -m grpc_tools.protoc -I "$PROTO_DIR" -I "$GNSI_DIR" \
    --python_out="$GNSI_DIR" --grpc_python_out="$GNSI_DIR" \
    "$GNSI_DIR/authz.proto" \
    "$GNSI_DIR/certz.proto" \
    "$GNSI_DIR/pathz.proto" \
    "$GNSI_DIR/credentialz.proto"
  if [[ -d "$GNSI_DIR/gnsi" ]]; then
    mv "$GNSI_DIR/gnsi"/* "$GNSI_DIR/"
    rmdir "$GNSI_DIR/gnsi"
  fi
fi

"${RUN[@]}" - "$PROTO_DIR" << 'EOF'
import pathlib
import re
import sys

namespace = "ansible_collections.nokia.openconfig.plugins.module_utils.proto"
gnoi_namespace = namespace + ".gnoi"
gnsi_namespace = namespace + ".gnsi"
google_rpc_namespace = gnoi_namespace + ".google.rpc"
pattern = re.compile(r"^import (\w+_pb2) as ", re.MULTILINE)
gnmi_import_pattern = re.compile(r"^import gnmi_pb2 as ", re.MULTILINE)
gnsi_import_pattern = re.compile(r"^from gnsi import (\w+_pb2) as ", re.MULTILINE)
google_rpc_pattern = re.compile(r"^from google\.rpc import (\w+_pb2) as ", re.MULTILINE)

def rewrite(path, ns):
    text = path.read_text()
    text = google_rpc_pattern.sub(r"from %s import \1 as " % google_rpc_namespace, text)
    text = gnmi_import_pattern.sub(r"from %s import gnmi_pb2 as " % namespace, text)
    text = gnsi_import_pattern.sub(r"from %s import \1 as " % gnsi_namespace, text)
    path.write_text(pattern.sub(r"from %s import \1 as " % ns, text))
    print("generated %s" % path.name)

for path in sorted(pathlib.Path(sys.argv[1]).glob("*_pb2*.py")):
    rewrite(path, namespace)

gnoi_dir = pathlib.Path(sys.argv[1]) / "gnoi"
if gnoi_dir.is_dir():
    for path in sorted(gnoi_dir.glob("*_pb2*.py")):
        rewrite(path, gnoi_namespace)

google_rpc_dir = gnoi_dir / "google" / "rpc"
if google_rpc_dir.is_dir():
    for path in sorted(google_rpc_dir.glob("*_pb2*.py")):
        rewrite(path, google_rpc_namespace)

gnsi_dir = pathlib.Path(sys.argv[1]) / "gnsi"
if gnsi_dir.is_dir():
    for path in sorted(gnsi_dir.glob("*_pb2*.py")):
        rewrite(path, gnsi_namespace)
EOF

SHIM="$(mktemp -d)"
trap 'rm -rf "$SHIM"' EXIT
mkdir -p "$SHIM/ansible_collections/nokia"
ln -s "$ROOT" "$SHIM/ansible_collections/nokia/openconfig"

"${RUN[@]}" - "$SHIM" << 'EOF'
import sys

sys.path.insert(0, sys.argv[1])
from google.protobuf import __version__ as protobuf_version  # noqa: E402
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2, gnmi_pb2_grpc  # noqa: E402,F401

opts = gnmi_pb2.DESCRIPTOR.GetOptions()
print("gNMI service version %s (imported with protobuf %s)" % (opts.Extensions[gnmi_pb2.gnmi_service], protobuf_version))
EOF
