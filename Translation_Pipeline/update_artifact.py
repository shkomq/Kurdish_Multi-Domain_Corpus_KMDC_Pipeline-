import os
import re

artifact_path = "/virtual_directory_path/artifacts/category_translations.md"

# Manual mapping dictionary
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

with open(artifact_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("|") and not line.startswith("| ---") and not "Original Kurdish Category" in line:
        parts = [p.strip() for p in line.split("|")]
        # parts is ['', original, translated, count, '']
        if len(parts) >= 4:
            orig = parts[1]
            trans = parts[2]
            count = parts[3]
            
            # Unescape markdown pipes in original for comparison
            orig_unescaped = orig.replace('\\|', '|')
            if orig_unescaped in category_map:
                trans = category_map[orig_unescaped]
            
            # Escape pipes back just in case
            orig_escaped = orig_unescaped.replace('|', '\\|')
            trans_escaped = trans.replace('|', '\\|')
            new_lines.append(f"| {orig_escaped} | {trans_escaped} | {count} |\n")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(artifact_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Artifact file updated successfully.")
