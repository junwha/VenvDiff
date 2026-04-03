# VenvDiff

## Make Diff

```bash
./make_diff.sh <new_image_tag> <torch_version>
```

- Base image is fixed to `junwha/ddiff-base:cu12.4.1-py3.10-torch-251214`.
- The script copies:
  - base: `/ddiff-base/py3.10-torch<torch_version>`
  - new: `/ddiff-base/py3.10-torch<torch_version>-new`
- `docker buildx build` 내부 단계에서 `src/make_diff.py` 실행 + `src/apply_diff.py` 검증 + `diff` 확인을 수행합니다. (`docker run` 사용 안 함)
- 변경 유형: 수정(`.delta`), 추가(`.new`), 삭제(`.delete`)
- 마지막에 아래 파일을 생성합니다:
  - `<new_image_tag with '/'->'--' and ':'->'-'>.tar.gz`

## Apply

```bash
cp -a ~/share/ddiff-base /ddiff-base
./apply.sh <torch_version> <tar.gz>
```
