import json
import re
from copy import deepcopy

import ollama
import prompts
from generation_utils import currnet_prompt, save_questions_to_file
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
max_depth = 1
# model gives 3 to 4 answer options
total_questions = 4**max_depth + 1
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


def dfs(previous_question_answers, depth):
    question_id = len(all_questions_answers)

    if depth >= max_depth:
        character_pattern = r'\{"character":\s*"[^"]*"\}'
        final_character = get_answer_from_model(
            currnet_prompt(previous_question_answers, True), character_pattern
        )["character"]
        all_questions_answers.append((final_character, []))
        return question_id

    question_pattern = (
        r'\{"question":\s*"[^"]*",\s*"options":\s*\["[^"]*"(?:,\s*"[^"]*")*\]\}'
    )
    new_question = get_answer_from_model(
        currnet_prompt(previous_question_answers), question_pattern
    )
    all_questions_answers.append((new_question["question"], []))
    if len(all_questions_answers) % 5 == 0:
        save_questions_to_file(all_questions_answers)

    pbar.update(1)

    for option_answer in new_question["options"]:
        next_question_answers = deepcopy(previous_question_answers)
        next_question_answers.append((new_question["question"], option_answer))
        answer_question_id = dfs(next_question_answers, depth + 1)
        all_questions_answers[question_id][1].append(
            (option_answer, answer_question_id)
        )
    return question_id


dfs([], 0)
save_questions_to_file(all_questions_answers)
pbar.close()

final_character = None
