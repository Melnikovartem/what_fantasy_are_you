import json
import random
import re

import ollama
import prompts

MODEL_NAME = "fantasy-question-creator"
try:
    ollama.show(MODEL_NAME)
except ollama._types.ResponseError:
    ollama.create(
        model=MODEL_NAME,
        modelfile=prompts.modelfile,
    )

previous_questions_answers = []
character_list = [
    "Noble Knight",
    "Cunning Thief",
    "Wise Wizard",
    "Fierce Warrior",
    "Mystical Elf",
]

prompt_template = """
{prompt_default}
{prompt_questions}

Possible Characters:
{character_list}

Previous Questions and Answers:
{previous_questions_answers}

{prompt_ending}
"""


def currnet_prompt(ending=False):
    formatted_previous_questions = "\n".join(
        f"question: {question['question']['question']}\nanswer: {question['player_answer']}"
        for question in previous_questions_answers
    )
    formatted_character_list = "* " + "\n* ".join(character_list)
    prompt = prompt_template.format(
        prompt_default=prompts.default,
        prompt_questions=prompts.questions if not ending else "",
        character_list=formatted_character_list,
        previous_questions_answers=formatted_previous_questions,
        prompt_ending=prompts.ending if ending else "",
    )

    return prompt


def error_parsing(context, prompt):
    print(f"\n--------------\nError parsing {context}\n{prompt}\n--------------\n")


j = 0
while j < 4:
    response = ollama.generate(model=MODEL_NAME, prompt=currnet_prompt())["response"]

    pattern = r'\{"question":\s*"[^"]*",\s*"options":\s*\["[^"]*"(?:,\s*"[^"]*")*\]\}'
    match = re.search(pattern, response)

    # Print the first match
    if not match:
        j -= 1
        error_parsing("question", response)
        continue

    new_question = json.loads(match.group(0))
    player_answer = random.choice(new_question["options"])

    print(f"\n{j}: {new_question['question']}")
    for i, option in enumerate(new_question["options"]):
        print(f"* {option}\t{"<--" if option == player_answer else ""}")

    previous_questions_answers.append(
        {"question": new_question, "player_answer": player_answer}
    )
    j += 1

final_character = None

while not final_character:
    response = ollama.generate(model=MODEL_NAME, prompt=currnet_prompt(True))[
        "response"
    ]
    pattern = r'\{"character":\s*"[^"]*"\}'
    match = re.search(pattern, response)
    if match:
        final_character = json.loads(match.group(0))["character"]
    else:
        error_parsing("character", response)
print(f"Your character is: {final_character}")
