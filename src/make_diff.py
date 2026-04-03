import argparse
import shutil
import filecmp # ★ 파일 내용 비교를 위해 추가
from io import BytesIO
from pathlib import Path
from pyrsync import get_signature_args, signature, delta

def generate_folder_diff(base_dir, new_dir, diff_dir):
    base_path = Path(base_dir)
    new_path = Path(new_dir)
    diff_path = Path(diff_dir)
    
    diff_path.mkdir(parents=True, exist_ok=True)

    for new_file in new_path.rglob('*'):
        if not new_file.is_file():
            continue

        rel_path = new_file.relative_to(new_path)
        base_file = base_path / rel_path
        
        diff_out_dir = (diff_path / rel_path).parent
        diff_out_dir.mkdir(parents=True, exist_ok=True)

        if base_file.exists():
            # ★ 추가된 부분: 파일 내용이 완전히 동일하면 건너뜁니다!
            if filecmp.cmp(base_file, new_file, shallow=False):
                print(f"[-] 변경 없음 (Skip): {rel_path}")
                continue

            # [수정된 파일] 내용이 다를 때만 signature 생성 후 delta 파일로 저장
            delta_file = diff_path / (str(rel_path) + '.delta')
            base_size = base_file.stat().st_size
            magic, block_len, strong_len = get_signature_args(base_size)

            with open(base_file, 'rb') as f_base, \
                 open(new_file, 'rb') as f_new, \
                 open(delta_file, 'wb') as f_delta:
                
                sig_stream = BytesIO()
                signature(f_base, sig_stream, strong_len, magic, block_len)
                
                sig_stream.seek(0)
                delta(f_new, sig_stream, f_delta)
                
            print(f"[*] Diff 생성됨 (수정): {rel_path}")
            
        else:
            # [새로운 파일]
            new_out_file = diff_path / (str(rel_path) + '.new')
            shutil.copy2(new_file, new_out_file)
            print(f"[+] Diff 생성됨 (추가): {rel_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="두 폴더를 비교하여 Diff(차이점) 폴더를 생성합니다.")
    parser.add_argument("-b", "--base", required=True, help="기준이 되는 원본 폴더 경로")
    parser.add_argument("-n", "--new", required=True, help="새로운 데이터가 있는 폴더 경로")
    parser.add_argument("-o", "--out", required=True, help="Diff 결과를 저장할 출력 폴더 경로")
    
    args = parser.parse_args()
    
    print("=== Diff 생성 시작 ===")
    generate_folder_diff(args.base, args.new, args.out)
    print("=== Diff 생성 완료 ===")