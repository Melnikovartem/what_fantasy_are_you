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


def currnet_prompt(
    previous_questions_answers,
    ending: bool = False,
) -> str:
    formatted_previous_questions = "\n".join(
        f"question: {question[0]}\nanswer: {question[1]}"
        for question in previous_questions_answers
    )
    formatted_character_list = "\n".join(
        map(
            lambda creature: f"* {creature[0]}\n * * {creature[1]}",
            prompts.character_list,
        )
    )
    prompt = prompt_template.format(
        prompt_default=prompts.default,
        prompt_questions=prompts.questions if not ending else "",
        character_list=formatted_character_list,
        previous_questions_answers=formatted_previous_questions,
        prompt_ending=prompts.ending if ending else "",
    )

    return prompt


def save_questions_to_file(questions_list) -> None:
    filename = f"generation_logs/questions_{len(questions_list)}.json"
    with open(filename, "w") as f:
        json.dump(questions_list, f, indent=4)
    print(f"Saved {len(questions_list)} questions to {filename}")
