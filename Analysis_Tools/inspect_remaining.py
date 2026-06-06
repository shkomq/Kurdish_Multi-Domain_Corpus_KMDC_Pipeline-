import json
import re

json_path = "/virtual_directory_path/merged_final.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect category frequencies
cat_counts = {}
for item in data:
    cat = item.get("category", "")
    if cat:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

# Find any category that has non-ASCII characters or non-English script characters
# English characters: a-zA-Z, numbers, standard punctuation (spaces, slashes, dashes, dots, commas, parentheses)
english_pattern = re.compile(r'^[a-zA-Z0-9\s\/\(\)\-\.,&:\?!_]*$')

non_english_cats = {}
for cat, count in cat_counts.items():
    if not english_pattern.match(cat):
        non_english_cats[cat] = count

print(f"Total non-English categories found: {len(non_english_cats)}")
print("\nList of categories and counts:")
for cat, count in sorted(non_english_cats.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat!r}: {count}")
