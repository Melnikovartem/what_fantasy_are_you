import json

import prompts

prompt_template = """
{prompt_default}
{prompt_questions}

Possible Characters:
{character_list}

Previous Questions and Answers:
{previous_questions_answers}

{prompt_ending}
"""


def current_prompt(
    previous_questions_answers,
    questions_left: int,
    character_count: dict,
) -> str:
    formatted_previous_questions = "\n\n".join(
        f"question: {question[0]}\nanswer: {question[1]}"
        for question in previous_questions_answers
    )
    character_list = sorted(
        prompts.character_list, key=lambda ch: character_count.get(ch[0], 0)
    )
    if questions_left <= 0:
        character_list = character_list[: round(len(character_list) * 0.25)]
    elif questions_left <= 1:
        character_list = character_list[: round(len(character_list) * 0.5)]
    elif questions_left <= 2:
        character_list = character_list[: round(len(character_list) * 0.75)]
    formatted_character_list = "\n".join(
        map(
            lambda creature: f"* {creature[0]}\n * * {creature[1]}",
            character_list,
        )
    )

    if questions_left <= 0:
        prompt_questions = ""
        prompt_ending = prompts.ending
    else:
        prompt_questions = prompts.questions
        prompt_ending = (
            f"There are {questions_left} questions left before we will know the result"
        )

    prompt = prompt_template.format(
        prompt_default=prompts.default,
        prompt_questions=prompt_questions,
        character_list=formatted_character_list,
        previous_questions_answers=formatted_previous_questions,
        prompt_ending=prompt_ending,
    )

    return prompt


def save_questions_to_file(questions_list) -> str:
    filename = f"generation_logs/questions_{len(questions_list)}.json"
    with open(filename, "w") as f:
        json.dump(questions_list, f, indent=4)
    return filename
