import csv
import json
import random

QUESTIONS_FILE = "locked_generations/questions_depth_7.json"
QUESTIONS_TRANSLATION_FILE = "final_files/questions_encoded"
TRANSLATION_FILE = "translation/questions_translation.csv"


with open(QUESTIONS_FILE, "r") as json_file:
    data = json.load(json_file)


text_ids = {}
pairs_of_encoded = []
id_counter = {
    "Q": 0,
    "AN": 0,
    "CH": 0,
}


swap_mapping = {
    "Paladin": "Centaur",
    "Wizard": "Lich",
    "Healer (Unicorn)": "Unicorn",
    "Shapeshifter": "Boggart",
    "Shapeshifter/Boggart": "Boggart",
    "Ork": "Orc",
    "Orion": "Sphinx",
    "Sage Orc": "Fairy",
}


def encode(text, prefix):
    if text in text_ids:
        return
    encoded = f"{prefix}_{id_counter[prefix]}"
    if text in swap_mapping:
        mapped_text = swap_mapping[text]
        encode(mapped_text, prefix)
        text_ids[text] = text_ids[mapped_text]
        print(f"replace {text} -> {mapped_text}")
        return

    text_ids[text] = encoded
    pairs_of_encoded.append((text, encoded))
    id_counter[prefix] += 1


all_strings = {
    "Q": [],
    "AN": [],
    "CH": [],
}
for i, question_info in enumerate(data):
    prefix = "CH" if len(question_info[1]) == 0 else "Q"
    all_strings[prefix].append(question_info[0])

    for j, answer in enumerate(question_info[1]):
        prefix = "AN"
        all_strings[prefix].append(answer[0])

for key in all_strings:
    all_strings[key] = sorted(all_strings[key])
    for text in all_strings[key]:
        encode(text, key)

for i, question_info in enumerate(data):
    data[i][0] = text_ids[question_info[0]]
    store_in_dict = {}
    for j, answer in enumerate(question_info[1]):
        store_in_dict[text_ids[answer[0]]] = answer[1]
    data[i][1] = store_in_dict


with open(QUESTIONS_TRANSLATION_FILE, "w") as questions_file:
    rows = []
    for question_info in data:
        rows.append(json.dumps(question_info))
    questions_file.write("\n".join(rows))


def sort_key_encode(text_and_ecoded):
    encoded = text_and_ecoded[1].split("_")

    if encoded[0] == "CH":
        ss = 0
    elif encoded[0] == "Q":
        ss = 10_000
    elif encoded[0] == "AN":
        ss = 100_000
    else:
        ss = 1_000_000
    return ss + int(encoded[1])


with open(TRANSLATION_FILE, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(["key", "en"])

    for text_field, encoded in sorted(pairs_of_encoded, key=sort_key_encode):
        writer.writerow([encoded, text_field])


def aggregate_over(prefix, aggregate=max, **kwargs):
    ffilter = filter(lambda x: x[1].split("_")[0] == prefix, pairs_of_encoded)
    pair = aggregate(list(ffilter), **kwargs)
    return f"{pair[1]}        {pair[0]}"


print()
print(f"Random question:\n{aggregate_over("Q", random.choice)}\n")
print(f"Random answer:\n{aggregate_over("AN", random.choice)}\n")
print(f"Longest question:\n{aggregate_over("Q", key=lambda x: len(x[0]))}\n")
print(f"Longest answer:\n{aggregate_over("AN", key=lambda x: len(x[0]))}\n")
print(f"Shortest answer:\n{aggregate_over("AN", min, key=lambda x: len(x[0]))}\n")
