import json
import re
import os

input_file = '/virtual_directory_path/merged_final.json'
output_file = '/virtual_directory_path/merged_final_cleaned.json'

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove leading and trailing whitespace
    text = text.strip()
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_dataset():
    print(f"Loading dataset from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    initial_count = len(data)
    print(f"Initial record count: {initial_count}")
    
    cleaned_data = []
    seen = set()
    
    for item in data:
        # Check if question and response exist
        q = item.get('question', '')
        r = item.get('response', '')
        
        # Clean texts
        cleaned_q = clean_text(q)
        cleaned_r = clean_text(r)
        
        # Skip if either is empty
        if not cleaned_q or not cleaned_r:
            continue
            
        # Deduplication based on question and response
        pair_key = (cleaned_q, cleaned_r)
        if pair_key in seen:
            continue
        seen.add(pair_key)
        
        # Update item with cleaned texts
        item['question'] = cleaned_q
        item['response'] = cleaned_r
        
        cleaned_data.append(item)
        
    final_count = len(cleaned_data)
    print(f"Final record count: {final_count}")
    print(f"Removed records: {initial_count - final_count}")
    
    print(f"Saving cleaned dataset to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print("Done!")

if __name__ == "__main__":
    clean_dataset()
