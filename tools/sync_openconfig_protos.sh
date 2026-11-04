#!/usr/bin/env bash
#
#    sync_openconfig_protos.sh — Refresh OpenConfig gNMI, gNOI, and gNSI .proto sources
#
#    Copies upstream protos into plugins/module_utils/proto with import paths
#    flattened for tools/build_openconfig_protos.sh.
#
#    Usage:
#      tools/sync_openconfig_protos.sh [gnmi|gnoi|gnsi|all]
#
#    Clone sources (once) into .tmp/ or set GNMI_SRC, GNOI_SRC, GNSI_SRC:
#      git clone https://github.com/openconfig/gnmi.git  .tmp/gnmi-src
#      git clone https://github.com/openconfig/gnoi.git  .tmp/gnoi-src
#      git clone https://github.com/openconfig/gnsi.git  .tmp/gnsi-src
#
#    Then run tools/build_openconfig_protos.sh to generate Python modules.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO="$ROOT/plugins/module_utils/proto"

GNMI_SRC="${GNMI_SRC:-$ROOT/.tmp/gnmi-src}"
GNOI_SRC="${GNOI_SRC:-$ROOT/.tmp/gnoi-src}"
GNSI_SRC="${GNSI_SRC:-$ROOT/.tmp/gnsi-src}"
GNMI_TAG="${GNMI_TAG:-v0.14.1}"
GNOI_OS_COMMIT="${GNOI_OS_COMMIT:-93cdd9ae9f35d8b4bc1599d0a727b294faeca352}"

TARGET="${1:-all}"

sync_gnmi() {
  if [[ ! -d "$GNMI_SRC/.git" ]]; then
    echo "Clone openconfig/gnmi into $GNMI_SRC first (tag $GNMI_TAG)." >&2
    exit 1
  fi
  git -C "$GNMI_SRC" show "${GNMI_TAG}:proto/gnmi_ext/gnmi_ext.proto" > "$PROTO/gnmi_ext.proto"
  git -C "$GNMI_SRC" show "${GNMI_TAG}:proto/gnmi/gnmi.proto" \
    | sed 's|import "github.com/openconfig/gnmi/proto/gnmi_ext/gnmi_ext.proto"|import "gnmi_ext.proto"|g' \
    > "$PROTO/gnmi.proto"
  echo "Synced gNMI protos ($GNMI_TAG) into $PROTO"
}

sync_gnoi() {
  local dest="$PROTO/gnoi"
  local google_rpc="$dest/google/rpc"
  if [[ ! -d "$GNOI_SRC/.git" ]]; then
    echo "Clone openconfig/gnoi into $GNOI_SRC first." >&2
    exit 1
  fi
  mkdir -p "$dest" "$google_rpc"

  copy_flat() {
    local file="$1"
    sed -e 's|import "github.com/openconfig/gnoi/types/types.proto"|import "types.proto"|g' \
        -e 's|import "github.com/openconfig/gnoi/common/common.proto"|import "common.proto"|g' \
        "$GNOI_SRC/$file" > "$dest/$(basename "$file")"
  }

  copy_flat types/types.proto
  copy_flat common/common.proto
  copy_flat system/system.proto
  copy_flat file/file.proto
  copy_flat factory_reset/factory_reset.proto
  copy_flat healthz/healthz.proto
  copy_flat bgp/bgp.proto
  copy_flat packet_link_qualification/packet_link_qualification.proto

  git -C "$GNOI_SRC" show "${GNOI_OS_COMMIT}:os/os.proto" \
    | sed 's|import "github.com/openconfig/gnoi/types/types.proto"|import "types.proto"|g' \
    > "$dest/os.proto"

  if [[ ! -f "$google_rpc/status.proto" ]]; then
    curl -fsSL 'https://raw.githubusercontent.com/googleapis/googleapis/master/google/rpc/status.proto' \
      -o "$google_rpc/status.proto"
  fi
  echo "Synced gNOI protos into $dest"
}

sync_gnsi() {
  local dest="$PROTO/gnsi"
  if [[ ! -d "$GNSI_SRC/.git" ]]; then
    echo "Clone openconfig/gnsi into $GNSI_SRC first." >&2
    exit 1
  fi
  mkdir -p "$dest"

  copy() {
    local file="$1"
    sed -e 's|import "github.com/openconfig/gnmi/proto/gnmi/gnmi.proto"|import "gnmi.proto"|g' \
        "$GNSI_SRC/$file" > "$dest/$(basename "$file")"
  }

  copy authz/authz.proto
  copy certz/certz.proto
  copy pathz/pathz.proto
  copy credentialz/credentialz.proto
  echo "Synced gNSI protos into $dest"
}

case "$TARGET" in
  gnmi) sync_gnmi ;;
  gnoi) sync_gnoi ;;
  gnsi) sync_gnsi ;;
  all)
    sync_gnmi
    sync_gnoi
    sync_gnsi
    ;;
  *)
    echo "usage: $0 [gnmi|gnoi|gnsi|all]" >&2
    exit 1
    ;;
esac

echo "Run tools/build_openconfig_protos.sh to regenerate *_pb2.py modules."
