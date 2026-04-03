import argparse
import shutil
from pathlib import Path
from pyrsync import patch

def apply_folder_diff(base_dir, diff_dir):
    base_path = Path(base_dir)
    diff_path = Path(diff_dir)

    if not base_path.exists():
        raise FileNotFoundError(f"기준 폴더가 없습니다: {base_path}")

    if not diff_path.exists():
        raise FileNotFoundError(f"Diff 폴더가 없습니다: {diff_path}")

    for diff_item in diff_path.rglob('*'):
        if not diff_item.is_file():
            continue

        rel_path_str = str(diff_item.relative_to(diff_path))

        if rel_path_str.endswith('.delta'):
            # [수정된 파일] -> 기존 파일에 Patch 적용
            rel_path = Path(rel_path_str[:-6])  # '.delta' 확장자 제거
            base_file = base_path / rel_path
            
            if base_file.exists():
                # 임시 파일에 패치 결과를 저장한 뒤 원래 파일 덮어쓰기
                temp_file = base_file.with_name(base_file.name + '.temp')
                
                with open(base_file, 'rb') as f_base, \
                     open(diff_item, 'rb') as f_delta, \
                     open(temp_file, 'wb') as f_out:
                    patch(f_base, f_delta, f_out)
                
                temp_file.replace(base_file)
                print(f"[*] Patch 완료 (수정됨): {rel_path}")

        elif rel_path_str.endswith('.new'):
            # [새로운 파일] -> 기존 폴더로 복사
            rel_path = Path(rel_path_str[:-4])  # '.new' 확장자 제거
            dest_file = base_path / rel_path
            
            # 목적지 폴더가 없으면 생성
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(diff_item, dest_file)
            print(f"[+] Patch 완료 (추가됨): {rel_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diff 폴더를 기준 폴더에 적용합니다.")
    parser.add_argument("-b", "--base", required=True, help="패치를 적용할 기준 폴더 경로")
    parser.add_argument("-d", "--diff", required=True, help="Diff 폴더 경로")

    args = parser.parse_args()

    print("=== Diff 적용 시작 ===")
    apply_folder_diff(args.base, args.diff)
    print("=== Diff 적용 완료 ===")
