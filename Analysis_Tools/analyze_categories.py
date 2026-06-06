import json
import re

file_path = "/virtual_directory_path/merged_final.json"

# Arabic/Kurdish script character range
arabic_script_regex = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count and unique categories
categories_count = {}
for item in data:
    cat = item.get("category")
    if cat is not None:
        categories_count[cat] = categories_count.get(cat, 0) + 1

kurdish_categories = []
english_categories = []

for cat, count in categories_count.items():
    if arabic_script_regex.search(cat):
        kurdish_categories.append((cat, count))
    else:
        english_categories.append((cat, count))

print(f"Total items in JSON: {len(data)}")
print(f"Total unique categories: {len(categories_count)}")
print(f"Kurdish/mixed categories count: {len(kurdish_categories)}")
print(f"English-only categories count: {len(english_categories)}")

print("\n--- SAMPLE ENGLISH CATEGORIES ---")
for cat, count in sorted(english_categories, key=lambda x: x[1], reverse=True)[:20]:
    print(f"  {cat}: {count}")

print("\n--- ALL KURDISH/MIXED CATEGORIES ---")
for cat, count in sorted(kurdish_categories, key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count}")
