import json
import os

json_path = "/virtual_directory_path/merged_final.json"
temp_json_path = "/virtual_directory_path/merged_final_temp.json"

# Manual mapping dictionary for all remaining non-English categories
category_map = {
    'دین (Religion': 'Religion',
    'دینی (Religion': 'Religion',
    'تاریخ (History': 'History',
    'دینی (Religious': 'Religious',
    'Politics (Siyasət': 'Politics',
    'شعر (Poetry': 'Poetry',
    'Dîn (Religion)': 'Religion',
    'ڕووداو': 'Event',
    'Politics (Siyasət - Politics': 'Politics',
    'زمان (Linguistics': 'Linguistics',
    'قانون (Law': 'Law',
    'Linguistics (Zimananasî': 'Linguistics',
    'بیۆگرافی': 'Biography',
    'گەردوونناسی': 'Astronomy',
    'Fərhəngnigarî (Lexicography)': 'Lexicography',
    'Linguistics (Zimanzanî - Linguistics': 'Linguistics',
    'Linguistics (Zimanşinasi - Linguistics': 'Linguistics',
    'Dînî (Religion)': 'Religion',
    'Dîrok (History)': 'History',
    'Health (Têndrostî - Health': 'Health',
    'Linguistics (Zamanaşinî - Linguistics': 'Linguistics',
    'فەلسەفە / سووفیزم': 'Philosophy / Sufism',
    'تاریخ و فرهنگ': 'History and Culture',
    'تاریخ (Mێژوو': 'History',
    'ئه\u200cده\u200cب و ڕه\u200cخنه': 'Literature and Criticism',
    'Zimanşînasi (Linguistics)': 'Linguistics',
    'ئەخلاق (Ethics': 'Ethics',
    'سیاسەت (Siyasat': 'Politics',
    'مێژوو (Mêjîstû': 'History',
    'سۆفیگەری': 'Sufism',
    'مێژووی ئێران': 'History of Iran',
    'History (Mêjû - History': 'History',
    'Linguistics / اللغويات': 'Linguistics',
    'Felsefe/Zimanşînasi': 'Philosophy / Linguistics',
    'History (Mêjû) / History': 'History',
    'جناح (Cenah': 'Faction',
    'ئەدەب و شیعری': 'Literature and Poetry',
    'اجتماعی': 'Social',
    'History (Mêjû': 'History',
    'Social (Komelayetî': 'Social',
    'Economy (Abûrî': 'Economy',
    'Economy (Abûrî - Economy': 'Economy',
    'History / التاریخ': 'History',
    'Philosophy (Felsəfə': 'Philosophy',
    'Zimanşînasi': 'Linguistics',
    'Zimanşînasi/Felsefe': 'Linguistics / Philosophy',
    'Zimanşinasî (Linguistics)': 'Linguistics',
    'پزیشکی / Medical': 'Medical',
    'سیاسی / Political': 'Political',
    'یاسا و دادوەری (Law and Justice': 'Law and Justice',
    'وەرزش (Sport': 'Sports',
    'ادبی': 'Literature',
    'مێژووی (History': 'History',
    'حەدیس (Hadith': 'Hadith',
    'زمانی (زمان': 'Linguistics',
    'ئاداب و ئەدەب': 'Literature',
    'کۆمه\u200cڵایهتی': 'Social',
    'Adab (Edəb - Literature': 'Literature',
    'Literature (Edəb': 'Literature',
    'Personal Experience (Azmûni Şexsî - Personal Experience': 'Personal Experience',
    'History (Mēzhū - History': 'History',
    'Economy (Abūrī - Economy': 'Economy',
    'Literature (Edêb - Literature': 'Literature',
    'History (Mêjhu - History': 'History',
    'War and War (Ceng u Şer': 'War and War',
    'International Relations (Peywendiyên Nêwdewletiyan': 'International Relations',
    'History and Society (Mêjû u Komelayetî': 'History and Society',
    'Kultūr (Culture)': 'Culture',
    'فەرھەنگی دەستەواژەکان (Idioms and Expressions': 'Idioms and Expressions',
    'Hunər (Art)': 'Art',
    'Colтура / Culture': 'Culture'
}

print("Loading merged_final.json...")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for item in data:
    cat = item.get("category")
    if cat in category_map:
        item["category"] = category_map[cat]
        updated_count += 1

print(f"Successfully updated {updated_count} records in the dataset.")

# Verify that no non-English/non-ASCII categories remain (excluding allowed English punctuation like apostrophes)
import re
english_pattern = re.compile(r"^[a-zA-Z0-9\s\/\(\)\-\.,&:\?!_']*$")

remaining_non_english = []
for item in data:
    cat = item.get("category", "")
    if cat and not english_pattern.match(cat):
        remaining_non_english.append(cat)

print(f"Remaining non-English categories after clean: {len(set(remaining_non_english))}")
if remaining_non_english:
    print("Values:", set(remaining_non_english))

# Write back to file
with open(temp_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

os.replace(temp_json_path, json_path)
print("merged_final.json overwritten and updated successfully.")
