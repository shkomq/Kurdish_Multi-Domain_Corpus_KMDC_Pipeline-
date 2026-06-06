import os
import shutil
import filecmp

def collect_files(source_dir, target_dir):
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Resolve absolute paths to compare them properly
    source_dir = os.path.abspath(source_dir)
    target_dir = os.path.abspath(target_dir)
    
    copied_count = 0
    collision_count = 0
    skipped_count = 0
    
    print(f"Scanning '{source_dir}' for JSON files ending with '_FINAL.json'...")
    
    for root, dirs, files in os.walk(source_dir):
        # Exclude the target directory from search to avoid double processing or copying to itself
        if os.path.abspath(root).startswith(target_dir):
            continue
            
        for file in files:
            if file.endswith('_FINAL.json'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(target_dir, file)
                
                already_copied = False
                is_collision = False
                
                if os.path.exists(dest_path):
                    # Check if the existing file has identical content
                    if filecmp.cmp(src_path, dest_path, shallow=False):
                        already_copied = True
                    else:
                        # Naming collision with different content, check numbered files
                        name, ext = os.path.splitext(file)
                        counter = 1
                        while True:
                            check_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                            if os.path.exists(check_path):
                                if filecmp.cmp(src_path, check_path, shallow=False):
                                    already_copied = True
                                    break
                            else:
                                dest_path = check_path
                                is_collision = True
                                break
                            counter += 1
                
                if already_copied:
                    skipped_count += 1
                    continue
                
                if is_collision:
                    collision_count += 1
                
                # Copy the file
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")
                copied_count += 1
                
    print("\nSummary:")
    print(f"Total files copied: {copied_count}")
    print(f"Total duplicate files skipped: {skipped_count}")
    if collision_count > 0:
        print(f"Naming collisions resolved: {collision_count}")

import sys

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else '/virtual_directory_path'
    dst = sys.argv[2] if len(sys.argv) > 2 else '/virtual_directory_path'
    collect_files(src, dst)
