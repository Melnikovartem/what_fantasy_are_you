import json
import random
import re

import ollama
import prompts
from generation_utils import current_prompt, save_questions_to_file
from tqdm import tqdm

MODEL_NAME = "fantasy-question-creator"
try:
    ollama.show(MODEL_NAME)
except ollama._types.ResponseError:
    ollama.create(
        model=MODEL_NAME,
        modelfile=prompts.modelfile,
    )

all_questions_answers = []
count_bottom_nodes = {}
max_depth = 7
duplicate_question_probabilty = 0.5
# model gives 3 to 4 answer options
total_questions = sum(4**depth for depth in range(max_depth + 1))
pbar = tqdm(total=total_questions)


def get_answer_from_model(prompt, pattern):
    # while True is not ok, but i need a valid pattern json
    while True:
        response = ollama.generate(model=MODEL_NAME, prompt=prompt)["response"]
        match = re.search(pattern, response)
        if match:
            return json.loads(match.group(0))
        print(
            f"\n--------------\nError parsing: {pattern}\n{response}\n--------------\n"
        )


def dfs(previous_question_answers, parent_question_id=None):
    question_id = len(all_questions_answers)
    questions_left = max_depth - len(previous_question_answers)

    if questions_left <= 0:
        prompt = current_prompt(
            previous_question_answers, questions_left, count_bottom_nodes
        )
        pattern = r'\{\s*"character"\s*:\s*"[^"]*"\s*\}'
        result_from_model = get_answer_from_model(prompt, pattern)
        character = result_from_model["character"]
        all_questions_answers.append((character, []))

        if character not in count_bottom_nodes:
            count_bottom_nodes[character] = 0
        count_bottom_nodes[character] += 1

        if len(all_questions_answers) % 200 == 0:
            save_questions_to_file(all_questions_answers)
        pbar.update(1)
        return question_id

    use_duplicate_quesiton = (
        parent_question_id
        and random.random() < duplicate_question_probabilty
        and len(all_questions_answers[parent_question_id][1])
        and questions_left > 1
    )

    result_from_model = None
    if use_duplicate_quesiton:
        parent_random_option = random.choice(
            all_questions_answers[parent_question_id][1]
        )
        parent_random_child = all_questions_answers[parent_random_option[1]]
        result_from_model = {
            "question": parent_random_child[0],
            "options": [option[0] for option in parent_random_child[1]],
        }

    if not result_from_model:
        prompt = current_prompt(
            previous_question_answers, questions_left, count_bottom_nodes
        )
        pattern = r'\{\s*"question"\s*:\s*"[^"]*"\s*,\s*"options"\s*:\s*\["[^"]*"(?:,\s*"[^"]*")*\s*\]\s*\}'
        result_from_model = get_answer_from_model(prompt, pattern)

    all_questions_answers.append((result_from_model["question"], []))
    if len(all_questions_answers) % 200 == 0:
        save_questions_to_file(all_questions_answers)
    pbar.update(1)

    for option_answer in result_from_model["options"]:
        next_question_answers = previous_question_answers + [
            (result_from_model["question"], option_answer)
        ]
        answer_question_id = dfs(
            next_question_answers,
            question_id,
        )
        all_questions_answers[question_id][1].append(
            (option_answer, answer_question_id)
        )
    return question_id


dfs([])
filename = save_questions_to_file(all_questions_answers)
pbar.close()

print(f"Saved {len(all_questions_answers)} questions/answers to {filename}")
print(f"Total of {len(count_bottom_nodes)} unique endings")
for bottom_node, value in reversed(
    sorted(count_bottom_nodes.items(), key=lambda s: s[1])
):
    print(f"* {value}\t{bottom_node}")
