# VenvDiff

Create and apply venv-level diffs between Docker images.

## Make a Diff

```bash
./make_diff.sh <new_image_tag> <torch_version>
```

Example:

```bash
./make_diff.sh myrepo/my-image:latest 2.5.1
```

This creates:

```bash
myrepo--my-image-latest.tar.gz
```

## Apply a Diff

Prepare base files, then apply:

```bash
cp -a ~/share/ddiff-base /ddiff-base
./apply.sh <torch_version> <tar.gz>
```

Example:

```bash
./apply.sh 2.5.1 myrepo--my-image-latest.tar.gz
```

## Current Behavior

- Base image is fixed to `junwha/ddiff-base:cu12.4.1-py3.10-torch-251214`.
- Diff generation is executed inside `docker buildx build` stages only (no `docker run`).
- Build stage installs `pyrsync` from local wheels in `pyrsync-py3.10/`.
- Virtualenv paths:
  - Base: `/ddiff-base/py3.10-torch<torch_version>`
  - New: `/ddiff-base/py3.10-torch<torch_version>-new`
- Supported diff artifacts:
  - Modified file: `.delta`
  - Added file: `.new`
  - Deleted file: `.delete`
- Output archive name format:
  - Replace `/` with `--`
  - Replace `:` with `-`
  - Final file: `<sanitized_new_image_tag>.tar.gz`
