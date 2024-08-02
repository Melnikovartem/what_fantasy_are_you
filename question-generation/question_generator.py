import ollama
from tqdm import trange

MODEL_NAME = "fantasy-question-creator"
try:
    ollama.show(MODEL_NAME)
except ollama._types.ResponseError:
    with open("prompt_questions", "r", encoding="utf-8") as prompt_questions_file:
        with open("Modelfile", "r", encoding="utf-8") as modefile_file:
            modefile = (
                f'{modefile_file.read()}\nSYSTEM="""{prompt_questions_file.read()}"""\n'
            )
            ollama.create(
                model=MODEL_NAME,
                modelfile=modefile,
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
Previous Questions and Answers:
{previous_questions_answers}

Possible Characters:
{character_list}
"""

for _ in trange(10):
    prompt = prompt_template.format(
        previous_questions_answers=previous_questions_answers,
        character_list=character_list,
    )

    print(prompt)

    new_question = ollama.generate(model=MODEL_NAME, prompt=prompt)["response"]

    import random

    player_answer = random.choice(["a", "b", "c", "d"])

    previous_questions_answers.append(
        {"question": new_question, "player_answer": player_answer}
    )

prompt = prompt_template.format(
    previous_questions_answers=previous_questions_answers,
    character_list=character_list,
)

with open("prompt_ending", "r", encoding="utf-8") as prompt_ending_file:
    prompt = f"{prompt}\n{prompt_ending_file.read()}"

final = ollama.generate(model=MODEL_NAME, prompt=prompt)["response"]


print(final)
