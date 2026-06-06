import json
import re

file_path = "/virtual_directory_path/merged_final.json"
arabic_script_regex = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

unique_cats = set()
kurdish_cats = set()

for item in data:
    cat = item.get("category")
    if cat is not None:
        unique_cats.add(cat)
        if arabic_script_regex.search(cat):
            kurdish_cats.add(cat)

print(f"Total items: {len(data)}")
print(f"Unique categories: {len(unique_cats)}")
print(f"Kurdish categories to translate: {len(kurdish_cats)}")
