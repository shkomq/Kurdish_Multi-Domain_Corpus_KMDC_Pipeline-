import json
import os
import re

artifact_path = "/virtual_directory_path/artifacts/category_translations.md"
json_paths = [
    "/virtual_directory_path/merged_final.json",
    "/virtual_directory_path/merged_final.json"
]

# Exact cleanup map for identified issues
manual_fixes = {
    'Geography / Géographie': 'Geography',
    'Pოლიtik and Daily Affairs': 'Politics and Daily Affairs',
    'ʿibādah': 'Religious Practice (Ibadah)',
    'Religious Practice (ʿIbādah)': 'Religious Practice (Ibadah)'
}

def clean_value(val):
    if not val:
        return ""
    # Standardize spaces
    val = re.sub(r'\s+', ' ', val).strip()
    # Check exact match first
    if val in manual_fixes:
        val = manual_fixes[val]
    # Replace typographic apostrophes/quotes
    val = val.replace('’', "'").replace('‘', "'").replace('`', "'").replace('´', "'")
    val = val.replace('“', '"').replace('”', '"')
    # Clean double separators
    val = re.sub(r'\s*/\s*', ' / ', val)
    val = re.sub(r'\s*-\s*', ' - ', val)
    return val

# 1. Clean the JSON datasets
for path in json_paths:
    if os.path.exists(path):
        print(f"Cleaning JSON dataset: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified_count = 0
        for item in data:
            orig = item.get("category", "")
            cleaned = clean_value(orig)
            if orig != cleaned:
                item["category"] = cleaned
                modified_count += 1
                
        print(f"  Standardized {modified_count} records in {os.path.basename(path)}.")
        
        # Write back cleanly
        temp_path = path + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        os.replace(temp_path, path)

# 2. Clean and synchronize category_translations.md
if os.path.exists(artifact_path):
    print(f"Cleaning translation report: {artifact_path}")
    with open(artifact_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith("|") and not line.startswith("| ---") and not "Original Kurdish Category" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                orig = parts[1]
                trans = parts[2]
                count = parts[3]
                
                # Clean translated value
                cleaned_trans = clean_value(trans)
                
                # Reconstruct line
                new_lines.append(f"| {orig} | {cleaned_trans} | {count} |\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("  Report file cleaned successfully.")

print("Sanitization process completed successfully!")
