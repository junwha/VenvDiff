#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <torch_version> <diff_tar_gz>"
  exit 1
fi

TORCH_VERSION="$1"
DIFF_TAR="$2"
TARGET_VENV="/ddiff-base/py3.10-torch${TORCH_VERSION}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

if [[ ! -f "$DIFF_TAR" ]]; then
  echo "Diff tar.gz not found: $DIFF_TAR"
  exit 1
fi

if [[ ! -d "$TARGET_VENV" ]]; then
  echo "Target venv not found: $TARGET_VENV"
  echo "먼저 아래를 실행해 주세요:"
  echo "  cp -a ~/share/ddiff-base /ddiff-base"
  exit 1
fi

mkdir -p "${WORK_DIR}/diff"
tar -xzf "$DIFF_TAR" -C "${WORK_DIR}/diff"

python3 "${SCRIPT_DIR}/src/apply_diff.py" \
  --base "$TARGET_VENV" \
  --diff "${WORK_DIR}/diff"

echo "Done: applied ${DIFF_TAR} to ${TARGET_VENV}"
