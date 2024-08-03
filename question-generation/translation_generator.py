import csv
import json

QUESTIONS_FILE = "locked_generations/questions_depth_3.json"
QUESTIONS_TRANSLATION_FILE = "translation/questions_encoded.json"
TRANSLATION_FILE = "translation/translation.csv"


with open(QUESTIONS_FILE, "r") as json_file:
    data = json.load(json_file)


text_ids = {}
id_counter = {
    "Q": 0,
    "AN": 0,
    "CH": 0,
}


def encode(text, prefix):
    encoded = f"{prefix}_{id_counter[prefix]}"
    text_ids[text] = encoded
    id_counter[prefix] += 1


all_strings = {
    "Q": [],
    "AN": [],
    "CH": [],
}
for i, question in enumerate(data):
    prefix = "CH" if len(question[1]) == 0 else "Q"
    all_strings[prefix].append(question[0])

    for j, answer in enumerate(question[1]):
        prefix = "AN"
        all_strings[prefix].append(answer[0])

for key in all_strings:
    all_strings[key] = sorted(all_strings[key])
    for text in all_strings[key]:
        encode(text, key)

for i, question in enumerate(data):
    data[i][0] = text_ids[question[0]]
    for j, answer in enumerate(question[1]):
        data[i][1][j][0] = text_ids[answer[0]]


with open(QUESTIONS_TRANSLATION_FILE, "w") as new_json_file:
    json.dump(data, new_json_file)


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

    for text_field, encoded in sorted(text_ids.items(), key=sort_key_encode):
        writer.writerow([encoded, text_field])
