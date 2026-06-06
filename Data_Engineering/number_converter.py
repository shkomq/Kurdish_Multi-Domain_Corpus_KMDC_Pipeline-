import json
import os

def convert_to_ckb_numbers(text):
    if not isinstance(text, str):
        return text
        
    kurdish_digits = {
        '0': '٠',
        '1': '١',
        '2': '٢',
        '3': '٣',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '٩'
    }
    
    result = ""
    for char in text:
        if char in kurdish_digits:
            result += kurdish_digits[char]
        else:
            result += char
    return result

def main():
    file_path = '/virtual_directory_path/merged_final.json'
    temp_file_path = '/virtual_directory_path/merged_final_ckb.json'
    
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print("Converting numbers...")
    for item in data:
        if 'question' in item:
            item['question'] = convert_to_ckb_numbers(item['question'])
        if 'response' in item:
            item['response'] = convert_to_ckb_numbers(item['response'])
            
    print(f"Saving data to {file_path}...")
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    os.replace(temp_file_path, file_path)
    print("Done!")

if __name__ == '__main__':
    main()
