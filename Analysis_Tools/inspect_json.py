import json

file_path = "/virtual_directory_path/merged_final.json"

with open(file_path, 'r', encoding='utf-8') as f:
    try:
        data = json.load(f)
        print("Type of data:", type(data))
        if isinstance(data, list):
            print("Length of list:", len(data))
            if len(data) > 0:
                print("First item keys:", data[0].keys())
                print("First item sample:", json.dumps(data[0], indent=2, ensure_ascii=False))
                
                # Check all unique categories in the data
                categories = set()
                for item in data:
                    cat = item.get("category")
                    if cat is not None:
                        categories.add(str(cat))
                print("\nUnique categories found:", categories)
        elif isinstance(data, dict):
            print("Keys:", list(data.keys()))
            # print first 5 elements
            for k in list(data.keys())[:5]:
                print(f"Key: {k}, type of val: {type(data[k])}")
                if isinstance(data[k], dict):
                    print("Val keys:", data[k].keys())
    except Exception as e:
        print("Error reading json:", e)
