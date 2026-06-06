import os
import json

def merge_and_clean(source_dir, output_file):
    merged_data = []
    
    # List all JSON files in the directory
    files = sorted([f for f in os.listdir(source_dir) if f.endswith('.json')])
    total_files = len(files)
    
    print(f"Found {total_files} JSON files in '{source_dir}'. Merging...")
    
    for idx, filename in enumerate(files, 1):
        file_path = os.path.join(source_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Process content, handling lists and individual dictionaries
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item.pop('document', None)
                    merged_data.append(item)
            elif isinstance(data, dict):
                data.pop('document', None)
                merged_data.append(data)
            else:
                print(f"Warning: Unexpected data structure in {filename}: {type(data)}")
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
        if idx % 500 == 0 or idx == total_files:
            print(f"Processed {idx}/{total_files} files...")
            
    print(f"Writing merged data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully merged {total_files} files into {output_file}. Total items in merged file: {len(merged_data)}")

import sys

if __name__ == '__main__':
    source_dir = sys.argv[1] if len(sys.argv) > 1 else '/virtual_directory_path/All_Final_Json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else '/virtual_directory_path/merged_final.json'
    merge_and_clean(source_dir, output_file)
