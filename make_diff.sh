#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <new_image_tag> <torch_version>"
  exit 1
fi

NEW_IMAGE_TAG="$1"
TORCH_VERSION="$2"
BASE_IMAGE_TAG="junwha/ddiff-base:cu12.4.1-py3.10-torch-251214"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$WORK_DIR"
}
trap cleanup EXIT

SAFE_TAG="${NEW_IMAGE_TAG//\//-}"
SAFE_TAG="${SAFE_TAG//:/-}"
OUTPUT_TAR="${SCRIPT_DIR}/vdiff-${SAFE_TAG}.tar.gz"
OUTPUT_NAME="vdiff-${SAFE_TAG}.tar.gz"

echo "[1/2] Build diff artifact inside buildx"
docker buildx build \
  --build-arg BASE_IMAGE="$BASE_IMAGE_TAG" \
  --build-arg NEW_IMAGE="$NEW_IMAGE_TAG" \
  --build-arg TORCH_VERSION="$TORCH_VERSION" \
  --build-arg OUTPUT_TAR="$OUTPUT_NAME" \
  -f "${SCRIPT_DIR}/Dockerfile.venv-copy" \
  --target artifact \
  --output "type=local,dest=${WORK_DIR}/out" \
  "$SCRIPT_DIR"

ARTIFACT_TAR="${WORK_DIR}/out/${OUTPUT_NAME}"
if [[ ! -f "$ARTIFACT_TAR" ]]; then
  echo "Build succeeded but artifact not found: $ARTIFACT_TAR"
  exit 1
fi

echo "[2/2] Copy artifact"
cp -f "$ARTIFACT_TAR" "$OUTPUT_TAR"

echo "Done: $OUTPUT_TAR"
