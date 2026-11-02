#!/usr/bin/env bash
#
#    build_protos.sh — Compile gNMI protos into importable collection modules
#
#    Usage:
#      tools/build_protos.sh [--python <interpreter>]
#
#    Generates gnmi_pb2.py, gnmi_pb2_grpc.py and gnmi_ext_pb2.py next to the
#    .proto sources in plugins/module_utils/proto and rewrites the generated
#    imports to the collection namespace. Used by CI, release and developers.
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

"${RUN[@]}" - "$PROTO_DIR" << 'EOF'
import pathlib
import re
import sys

namespace = "ansible_collections.nokia.openconfig.plugins.module_utils.proto"
pattern = re.compile(r"^import (\w+_pb2) as ", re.MULTILINE)

for path in sorted(pathlib.Path(sys.argv[1]).glob("*_pb2*.py")):
    text = path.read_text()
    path.write_text(pattern.sub(r"from %s import \1 as " % namespace, text))
    print("generated %s" % path.name)
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
