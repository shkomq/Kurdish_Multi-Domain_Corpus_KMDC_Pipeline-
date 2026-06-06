import json
import re
import time
import os
from deep_translator import GoogleTranslator

# Paths
json_path = "/virtual_directory_path/merged_final.json"
temp_json_path = "/virtual_directory_path/merged_final_temp.json"
artifact_dir = "/home/swyanswartz/.gemini/antigravity/brain/be14721b-f8b5-46ce-936e-cadb903db38e/artifacts"
artifact_path = os.path.join(artifact_dir, "category_translations.md")

os.makedirs(artifact_dir, exist_ok=True)

# Regex to detect Kurdish/Arabic script
arabic_script_regex = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')

def clean_translation(original, translated):
    translated = translated.strip()
    
    # 1. Deduplicate slash terms (e.g. "Law/Law" -> "Law")
    if '/' in translated:
        parts = [p.strip() for p in translated.split('/')]
        parts = [p for p in parts if p]
        seen = []
        for p in parts:
            if p.lower() not in [s.lower() for s in seen]:
                seen.append(p)
        translated = ' / '.join(seen)
        
    # 2. Deduplicate parentheses (e.g. "Social Science (Social Science)" -> "Social Science")
    match = re.match(r'^([^(]+)\s*\(([^)]+)\)$', translated)
    if match:
        p1 = match.group(1).strip()
        p2 = match.group(2).strip()
        if p1.lower() == p2.lower():
            translated = p1
            
    # 3. Clean up any trailing/leading symbols
    translated = translated.strip(" /()[]{}")
    return translated

print("Loading merged_final.json...")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count frequencies and separate categories
categories_count = {}
for item in data:
    cat = item.get("category")
    if cat is not None:
        categories_count[cat] = categories_count.get(cat, 0) + 1

kurdish_cats = [cat for cat in categories_count.keys() if arabic_script_regex.search(cat)]
print(f"Total items in JSON: {len(data)}")
print(f"Total unique categories: {len(categories_count)}")
print(f"Kurdish categories to translate: {len(kurdish_cats)}")

# Translation using batching
translator = GoogleTranslator(source='ckb', target='en')
translation_mapping = {}

batch_size = 50
total_batches = (len(kurdish_cats) + batch_size - 1) // batch_size

print(f"Starting translation in {total_batches} batches of {batch_size}...")

for b_idx in range(total_batches):
    start = b_idx * batch_size
    end = min(start + batch_size, len(kurdish_cats))
    batch = kurdish_cats[start:end]
    
    print(f"Translating batch {b_idx+1}/{total_batches} ({len(batch)} items)...")
    text = '\n'.join(batch)
    
    translated_lines = []
    try:
        translated_text = translator.translate(text)
        translated_lines = [line.strip() for line in translated_text.split('\n')]
    except Exception as e:
        print(f"Batch {b_idx+1} translation error: {e}. Falling back to individual translation.")
        
    # Verify line count matches
    if len(translated_lines) == len(batch):
        for orig, trans in zip(batch, translated_lines):
            cleaned = clean_translation(orig, trans)
            translation_mapping[orig] = cleaned
    else:
        # Mismatch or error, do individual translations for this batch
        if len(translated_lines) != len(batch) and len(translated_lines) > 0:
            print(f"Line count mismatch (expected {len(batch)}, got {len(translated_lines)}). Doing individual translations.")
        for item in batch:
            try:
                trans = translator.translate(item)
                cleaned = clean_translation(item, trans)
                translation_mapping[item] = cleaned
            except Exception as ex:
                print(f"Error translating '{item}': {ex}")
                translation_mapping[item] = item  # Fallback to original
                
    time.sleep(0.5)  # Small delay to avoid rate limits

print("Translation completed. Updating dataset...")

# Update categories in data
updated_count = 0
for item in data:
    cat = item.get("category")
    if cat in translation_mapping:
        item["category"] = translation_mapping[cat]
        updated_count += 1

print(f"Updated {updated_count} items in the dataset.")

# Write updated JSON to temp file
print("Writing updated data to temp JSON file...")
with open(temp_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Replace original file with updated file
print("Overwriting merged_final.json with new data...")
os.replace(temp_json_path, json_path)
print("File updated successfully.")

# Create the markdown artifact report
print("Writing translation report artifact...")
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write("# Kurdish to English Category Translation Mapping\n\n")
    f.write(f"Processed file: `backup_data_complete/merged_final.json`\\\n")
    f.write(f"Total items in dataset: {len(data)}\\\n")
    f.write(f"Total unique Kurdish categories translated: {len(kurdish_cats)}\n\n")
    
    f.write("| Original Kurdish Category | Translated English Category | Occurrences |\n")
    f.write("| --- | --- | --- |\n")
    # Sort by frequency of occurrence descending
    sorted_kurdish = sorted(kurdish_cats, key=lambda x: categories_count[x], reverse=True)
    for orig in sorted_kurdish:
        trans = translation_mapping[orig]
        count = categories_count[orig]
        # Escape any pipe symbols in markdown table
        orig_escaped = orig.replace('|', '\\|')
        trans_escaped = trans.replace('|', '\\|')
        f.write(f"| {orig_escaped} | {trans_escaped} | {count} |\n")

print("Artifact written successfully to:", artifact_path)
