import json
import os

def main():
    p1 = '/virtual_directory_path/merged_final1.json'
    p2 = '/virtual_directory_path/merged_final2.json'
    out_path = '/virtual_directory_path/merged_final.json'

    print("Loading dataset 1...")
    with open(p1, 'r', encoding='utf-8') as f:
        d1 = json.load(f)
    print(f"Loaded {len(d1)} items from {p1}")

    print("Loading dataset 2...")
    with open(p2, 'r', encoding='utf-8') as f:
        d2 = json.load(f)
    print(f"Loaded {len(d2)} items from {p2}")

    merged_items = []
    skipped_missing = 0
    skipped_duplicates = 0
    seen_pairs = set()

    for idx, item in enumerate(d1 + d2):
        # Validate keys
        q = item.get('question')
        r = item.get('response')
        cat = item.get('category')

        if not q or not r or not cat:
            skipped_missing += 1
            continue

        q = q.strip()
        r = r.strip()
        cat = cat.strip()

        if not q or not r or not cat:
            skipped_missing += 1
            continue

        # Deduplicate
        pair = (q, r)
        if pair in seen_pairs:
            skipped_duplicates += 1
            continue

        seen_pairs.add(pair)

        # Create cleaned item with only core keys
        cleaned_item = {
            'id': str(len(merged_items) + 1),  # Sequential 1-based string ID
            'category': cat,
            'question': q,
            'response': r
        }
        merged_items.append(cleaned_item)

    print(f"Skipped {skipped_missing} items due to missing/empty question, response, or category.")
    print(f"Skipped {skipped_duplicates} items as exact duplicates (same question and response).")
    print(f"Total merged items: {len(merged_items)}")

    print(f"Writing merged dataset to {out_path}...")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(merged_items, f, ensure_ascii=False, indent=2)

    print("Successfully finished merging!")

if __name__ == '__main__':
    main()
