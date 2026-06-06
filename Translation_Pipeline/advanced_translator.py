import os
import json
import re
import time
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

# Absolute paths
artifact_path = "/virtual_directory_path/artifacts/category_translations.md"
untranslated_json = "/virtual_directory_path/merged_final_untranslated.json"
output_json = "/virtual_directory_path/merged_final.json"
temp_output_json = "/virtual_directory_path/merged_final_temp.json"

def normalize_string(s):
    if not s:
        return ""
    s = s.replace("\u064a", "\u06cc").replace("\u0649", "\u06cc")
    s = s.replace("\u0643", "\u06a9")
    s = s.replace("\u200c", "").replace("\u200b", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def clean_term(t):
    t = normalize_string(t)
    t = re.sub(r"\(.*?\)", "", t).strip()
    return t

# 1. Parse existing translations and counts from the first dataset in category_translations.md
existing_mappings = {}
first_dataset_counts = {}

if os.path.exists(artifact_path):
    print("Loading existing translations from category_translations.md...")
    with open(artifact_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("|") and not line.startswith("| ---") and not "Original Kurdish Category" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    orig = parts[1].replace("\\|", "|")
                    trans = parts[2].replace("\\|", "|")
                    count_str = parts[3]
                    try:
                        count = int(count_str)
                    except ValueError:
                        count = 0
                    
                    orig_norm = normalize_string(orig)
                    existing_mappings[orig_norm] = trans
                    first_dataset_counts[orig_norm] = count
    print(f"Loaded {len(existing_mappings)} translations from first dataset.")
else:
    print("Warning: category_translations.md not found. Proceeding with clean mapping.")

# 2. Extract word-level mappings for offline decomposition
word_mapping = {}

# Process single word mappings first
for k, v in existing_mappings.items():
    co = clean_term(k)
    ct = clean_term(v)
    if co and ct and not any(ord(c) > 127 for c in ct):
        word_mapping[co] = ct

for k, v in existing_mappings.items():
    co = clean_term(k)
    ct = clean_term(v)
    if not co or not ct or any(ord(c) > 127 for c in ct):
        continue
    k_words = co.split()
    v_words = ct.split()
    if len(k_words) == 1 and len(v_words) == 1:
        word_mapping[co] = ct

# Process compound mappings (e.g. "A و B" -> "A and B")
for k, v in existing_mappings.items():
    co = clean_term(k)
    ct = clean_term(v)
    if not co or not ct or any(ord(c) > 127 for c in ct):
        continue
    if " و " in co and " and " in ct:
        k_parts = [p.strip() for p in co.split(" و ")]
        v_parts = [p.strip() for p in ct.split(" and ")]
        if len(k_parts) == len(v_parts):
            for kp, vp in zip(k_parts, v_parts):
                if kp and vp:
                    word_mapping[kp] = vp
    elif " / " in co and " / " in ct:
        k_parts = [p.strip() for p in co.split(" / ")]
        v_parts = [p.strip() for p in ct.split(" / ")]
        if len(k_parts) == len(v_parts):
            for kp, vp in zip(k_parts, v_parts):
                if kp and vp:
                    word_mapping[kp] = vp

# Manual roots to supplement
roots = {
    "ئابوری": "Economy",
    "ئابووری": "Economy",
    "ئابورى": "Economy",
    "تەندروستی": "Health",
    "سیاسەت": "Politics",
    "سیاسی": "Political",
    "dîn": "Religion",
    "dînî": "Religious",
    "دین": "Religion",
    "دینی": "Religious",
    "مێژوو": "History",
    "مێژووی": "Historical",
    "شەڕ": "War",
    "تاوان": "Crime",
    "یاسا": "Law",
    "کۆمەڵایەتی": "Social",
    "كۆمەڵایەتی": "Social",
    "فەرهەنگ": "Culture",
    "فەرهەنگی": "Cultural",
    "ئەدەب": "Literature",
    "ئەدەبی": "Literary",
    "هەواڵ": "News",
    "هەواڵەکان": "News",
    "پەروەردە": "Education",
    "زانست": "Science",
    "وەرزش": "Sports",
    "وەرزشی": "Sports",
    "هەڵبژاردن": "Elections",
    "پێكدادان": "Clashes",
    "پێکدادان": "Clashes",
    "توندوتیژی": "Violence",
    "ئاسایش": "Security",
    "ئەمنی": "Security",
    "سەربازی": "Military",
    "هونەر": "Art",
    "هونەری": "Artistic",
    "زمان": "Linguistics",
    "زمانی": "Linguistics",
    "خێزان": "Family",
    "گەشتوگوزار": "Tourism",
    "گەشت": "Travel",
    "جوگرافیا": "Geography",
    "جوگرافی": "Geographical",
    "ژینگە": "Environment",
    "ژینگەیی": "Environmental",
    "میدیا": "Media",
    "ڕۆژنامەگەری": "Journalism",
    "شەریعەت": "Sharia",
    "فقه": "Jurisprudence",
    "فەقهی": "Jurisprudential",
    "مەعریفی": "Knowledge",
    "هاوڵاتیان": "Citizens",
    "کۆچکەردن": "Migration",
    "كۆچكردنى": "Migration",
    "كۆچكردن": "Migration",
    "تۆپی پێ": "Football",
    "کەشناسی": "Meteorology",
    "ڕووداو": "Event",
    "ڕووداوەکان": "Events",
    "تاکەکەس": "Individual",
    "زانکۆ": "University",
    "ژیانی": "Life",
    "شار": "City",
    "شارستانی": "Civilization",
    "شێعر": "Poetry",
    "شیعر": "Poetry",
    "مافی مرۆڤ": "Human Rights",
    "مافەکانی مرۆڤ": "Human Rights",
    "هاتوچۆ": "Traffic",
    "بڵاوکراوەکان": "Publications",
    "چاپەمەنی": "Press",
    "کۆمەڵایەتی/کۆمەڵناسی": "Sociology"
}

for k, v in roots.items():
    word_mapping[normalize_string(k)] = v

print(f"Extracted {len(word_mapping)} word-level mappings for offline translation.")

# 3. Load English words for dictionary checks
english_words = set()
if os.path.exists("/usr/share/dict/words"):
    with open("/usr/share/dict/words", "r") as f:
        for line in f:
            english_words.add(line.strip().lower())
extra_words = {"politics", "economics", "economy", "sports", "news", "weather", "security", "world", "local", "health", "culture", "art", "science", "education", "international", "relations", "jurisprudential", "hadith", "sociology", "biography", "novel", "criticism", "literature", "linguistics"}
english_words.update(extra_words)

def is_pure_english(text):
    return bool(re.match(r"^[a-zA-Z0-9\s\/\(\)\-\.,&:\?!_'\''’]*$", text))

def is_already_english(cat):
    if not is_pure_english(cat):
        return False
    words = [w.strip("(),.?!-–—/|&").lower() for w in cat.split()]
    kurdish_words = {"aburi", "abori", "abury", "abûrî", "abûri", "bazrgani", "siyaset", "siyasət", "asayish", "asayîş", "komelayeti", "komelayetî", "komelayety", "komalayeti", "mêjû", "mêjûî", "mêjûyî", "meju", "ziman", "edeb", "dîn", "huner", "werzish", "yasa", "darai", "darayi", "darayî", "ceng", "şer", "hawa", "hevayî", "keshhewaha", "keshhewawa", "hewala", "hewal", "heval", "werezsh"}
    if any(w in kurdish_words for w in words):
        return False
    return True

def clean_final_english(translated):
    translated = translated.strip()
    match = re.match(r"^([^(]+)\s*\(([^)]+)\)$", translated)
    if match:
        p1 = match.group(1).strip()
        p2 = match.group(2).strip()
        if p1.lower() == p2.lower():
            translated = p1
    translated = translated.strip(" /()[]{}")
    translated = "".join(c for c in translated if ord(c) < 128)
    translated = translated.strip(" /()[]{}")
    return translated

def extract_english_from_category(cat):
    paren_matches = re.findall(r"\(([^)]+)\)", cat)
    for part in paren_matches:
        parts = re.split(r"[-–—/|]", part)
        if len(parts) > 1:
            best_part = None
            max_english_score = -1
            for p in parts:
                p_clean = p.strip()
                if not is_pure_english(p_clean):
                    continue
                words = [w.strip("(),.?!").lower() for w in p_clean.split()]
                if not words:
                    continue
                english_count = sum(1 for w in words if w in english_words)
                score = english_count / len(words)
                if score > max_english_score and english_count > 0:
                    max_english_score = score
                    best_part = p_clean
            if best_part and max_english_score >= 0.5:
                return clean_final_english(best_part)
        
        part_clean = part.strip()
        if is_pure_english(part_clean):
            words = [w.strip("(),.?!").lower() for w in part_clean.split()]
            if words:
                english_count = sum(1 for w in words if w in english_words)
                score = english_count / len(words)
                if score >= 0.5 and len(part_clean) > 2:
                    return clean_final_english(part_clean)

    cat_no_paren = re.sub(r"\(.*?\)", "", cat).strip()
    parts = re.split(r"[-–—/|]", cat_no_paren)
    if len(parts) > 1:
        best_part = None
        max_english_score = -1
        for part in parts:
            part_clean = part.strip()
            if is_pure_english(part_clean):
                words = [w.strip("(),.?!").lower() for w in part_clean.split()]
                if not words:
                    continue
                english_count = sum(1 for w in words if w in english_words)
                score = english_count / len(words)
                if score > max_english_score and english_count > 0:
                    max_english_score = score
                    best_part = part_clean
        if best_part and max_english_score >= 0.5:
            return clean_final_english(best_part)
                    
    return None

def decompose_translate(cat):
    cat_clean = cat.strip("<> ")
    cat_norm = normalize_string(cat_clean)
    
    if cat_norm in word_mapping:
        return word_mapping[cat_norm]
        
    for sep, eng_sep in [(" و ", " and "), (" / ", " / "), (" - ", " - "), ("/", " / "), ("-", " - "), (" ", " ")]:
        if sep in cat_clean:
            parts = cat_clean.split(sep)
            trans_parts = []
            for p in parts:
                p_norm = normalize_string(p.strip())
                if p_norm in word_mapping:
                    trans_parts.append(word_mapping[p_norm])
                elif is_already_english(p.strip()):
                    trans_parts.append(p.strip())
                else:
                    break
            if len(trans_parts) == len(parts):
                return eng_sep.join(trans_parts)
    return None

def get_translation_source(cat):
    stripped = re.sub(r"\(.*?\)", "", cat).strip()
    stripped_clean = stripped.strip("<> -/|")
    if len(stripped_clean) > 0 and not is_pure_english(stripped_clean):
        return stripped_clean
    paren_matches = re.findall(r"\(([^)]+)\)", cat)
    if paren_matches:
        for part in paren_matches:
            part_clean = part.strip().strip("<> -/|")
            if part_clean:
                return part_clean
    return cat.strip("<> ")

def standardize_english_category(cat):
    if not cat:
        return ""
    cat = cat.strip().strip("`'\"“”‘’")
    cat = re.sub(r"\s+", " ", cat)
    
    minor_words = {"and", "or", "of", "in", "the", "a", "an", "to", "for", "with", "by", "at", "from"}
    
    words = cat.split()
    capitalized_words = []
    for idx, w in enumerate(words):
        clean_w = w.lower().strip("(),.-/&")
        if clean_w in minor_words and idx > 0:
            capitalized_words.append(w.lower())
        else:
            if "/" in w:
                w_sub = "/".join(sub.capitalize() for sub in w.split("/"))
                capitalized_words.append(w_sub)
            elif "-" in w:
                w_sub = "-".join(sub.capitalize() for sub in w.split("-"))
                capitalized_words.append(w_sub)
            else:
                capitalized_words.append(w.capitalize())
    
    cat = " ".join(capitalized_words)
    cat = re.sub(r"\s*/\s*", " / ", cat)
    cat = re.sub(r"\s*-\s*", " - ", cat)
    cat = re.sub(r"\s*&\s*", " & ", cat)
    cat = cat.replace(" And ", " and ").replace(" Or ", " or ").replace(" Of ", " of ").replace(" In ", " in ")
    cat = cat.strip(" -/&")
    return cat

# 4. Load the untranslated second dataset
print(f"Loading untranslated dataset from {untranslated_json}...")
with open(untranslated_json, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total items in second dataset: {len(data)}")

# Count unique categories and occurrences in the second dataset
unique_cats_counts = {}
for item in data:
    cat = item.get("category", "")
    if cat:
        unique_cats_counts[cat] = unique_cats_counts.get(cat, 0) + 1

print(f"Found {len(unique_cats_counts)} unique categories in second dataset.")

# 5. Resolve categories offline using mapping, rules, and decomposition
resolved_mappings = {}
unresolved_cats = []

for cat in sorted(list(unique_cats_counts.keys())):
    cat_norm = normalize_string(cat)
    
    # Check 1: Already English?
    if is_already_english(cat):
        resolved_mappings[cat] = standardize_english_category(cat)
        continue
        
    # Check 2: Existing mapping
    if cat_norm in existing_mappings:
        resolved_mappings[cat] = standardize_english_category(existing_mappings[cat_norm])
        continue
        
    # Check 3: Rule-based extraction
    res_rule = extract_english_from_category(cat)
    if res_rule:
        resolved_mappings[cat] = standardize_english_category(res_rule)
        continue
        
    # Check 4: Decompose and translate
    res_decomp = decompose_translate(cat)
    if res_decomp:
        resolved_mappings[cat] = standardize_english_category(res_decomp)
        continue
        
    unresolved_cats.append(cat)

print(f"Offline resolution completed: {len(resolved_mappings)} / {len(unique_cats_counts)} ({len(resolved_mappings)/len(unique_cats_counts)*100:.2f}%)")
print(f"Remaining categories to translate via API: {len(unresolved_cats)}")

# 6. Translate unresolved categories in parallel using a ThreadPoolExecutor
translator = GoogleTranslator(source="auto", target="en")

def translate_item(orig):
    src = get_translation_source(orig)
    for retry in range(3):
        try:
            trans = translator.translate(src)
            return orig, standardize_english_category(trans)
        except Exception as e:
            time.sleep(1)
    return orig, standardize_english_category(orig)

if unresolved_cats:
    print(f"Translating {len(unresolved_cats)} unresolved categories using 20 parallel workers...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(translate_item, unresolved_cats))
        
    for orig, trans in results:
        resolved_mappings[orig] = trans
        
    end_time = time.time()
    print(f"Parallel translation completed in {end_time - start_time:.2f} seconds!")

# 7. Apply translations to the dataset records and save
print(f"Applying translations to dataset...")
for item in data:
    cat = item.get("category", "")
    if cat in resolved_mappings:
        item["category"] = resolved_mappings[cat]

# Write to temp file first to be safe
print(f"Saving translated records to {temp_output_json}...")
with open(temp_output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Overwrite output_json safely
if os.path.exists(output_json):
    os.remove(output_json)
os.rename(temp_output_json, output_json)
print(f"Successfully wrote clean translated dataset to {output_json}!")

# 8. Reconcile and build consolidated translation mapping report
combined_mappings = {}
combined_counts = {}

# Load counts for second dataset
for orig, count in unique_cats_counts.items():
    orig_norm = normalize_string(orig)
    combined_counts[orig_norm] = combined_counts.get(orig_norm, 0) + count

# Add counts for first dataset
for orig_norm, count in first_dataset_counts.items():
    combined_counts[orig_norm] = combined_counts.get(orig_norm, 0) + count

# Reconcile final translated values
for orig_norm in combined_counts.keys():
    found = False
    for cat in unique_cats_counts.keys():
        if normalize_string(cat) == orig_norm:
            combined_mappings[orig_norm] = resolved_mappings[cat]
            found = True
            break
    if not found and orig_norm in existing_mappings:
        combined_mappings[orig_norm] = standardize_english_category(existing_mappings[orig_norm])

# Sort translations by occurrences descending
sorted_translations = sorted(combined_mappings.items(), key=lambda x: combined_counts[x[0]], reverse=True)

# Generate category_translations.md content
md_content = []
md_content.append("# Kurdish to English Category Translation Mapping\n\n")
md_content.append(f"Processed file 1: `backup_data_complete/merged_final.json` (Total items: 40299)\n")
md_content.append(f"Processed file 2: `SKNAD_Split_Only_Output/merged_final.json` (Total items: 92871)\n")
md_content.append(f"Total unique Kurdish categories standardized: {len(combined_mappings)}\n\n")

md_content.append("| Original Kurdish Category | Translated English Category | Occurrences |\n")
md_content.append("| --- | --- | --- |\n")

printed_rows = set()
for orig_norm, trans in sorted_translations:
    orig_escaped = orig_norm.replace("|", "\\|")
    trans_escaped = trans.replace("|", "\\|")
    count = combined_counts[orig_norm]
    row = f"| {orig_escaped} | {trans_escaped} | {count} |\n"
    if row not in printed_rows:
        md_content.append(row)
        printed_rows.add(row)

# Save the updated report to the artifact path
print(f"Writing updated translation report to {artifact_path}...")
with open(artifact_path, "w", encoding="utf-8") as f:
    f.writelines(md_content)

print("Translation and synchronization complete!")
