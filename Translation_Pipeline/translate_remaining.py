import json
import re
import time
from deep_translator import GoogleTranslator

json_path = "/virtual_directory_path/merged_final.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect category frequencies
cat_counts = {}
for item in data:
    cat = item.get("category", "")
    if cat:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

# Identify non-English categories (filtering out those that are already clean English like "Children's Literature")
english_pattern = re.compile(r"^[a-zA-Z0-9\s\/\(\)\-\.,&:\?!_']*$")

non_english_cats = []
for cat in cat_counts.keys():
    if not english_pattern.match(cat):
        non_english_cats.append(cat)

print(f"Found {len(non_english_cats)} categories to translate/clean.")

# Clean up helper
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

# Let's perform individual translation using GoogleTranslator
translator = GoogleTranslator(source='auto', target='en')
mapping = {}

for cat in non_english_cats:
    try:
        translated = translator.translate(cat)
        cleaned = clean_translation(cat, translated)
        mapping[cat] = cleaned
        print(f"{cat!r} -> {cleaned!r}")
        time.sleep(0.2)
    except Exception as e:
        print(f"Error for {cat!r}: {e}")
        mapping[cat] = cat
