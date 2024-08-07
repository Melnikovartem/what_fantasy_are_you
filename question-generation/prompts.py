modelfile = """
FROM llama3
# sets the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1
# sets the context window size to 4096, this controls how many tokens the LLM can use as context to generate the next token
# PARAMETER num_ctx 8096
"""

default = """
You are a professional game designer with several years of experience in creating engaging and immersive interactive experiences. Your task is to design questions for a "Who are you in a fantasy setting?" personality test game. This game aims to match players with one of several pre-defined fantasy characters based on their answers to a series of questions.
Here are the details of your task:
Write questions that will help determine which fantasy character a player most closely aligns with.
You have been provided with the following information:

* A list of previous questions with the player's answers (provided below)
* A list of characters that the player may become (provided below)
"""

questions = """
Using your expertise in game design and your understanding of fantasy storytelling, craft a new question with options for the player to choose from. This question should be designed to further reveal the player's character and guide them towards one of the predetermined characters.

Write a new question with options for the player to choose from. This question should be:

* Relevant to the fantasy setting
* Engaging and thought-provoking
* Useful for determining the player's character
* Consistent with the tone and style of the game

**Please respond with a new question in the exact format below:**

{"question": "question_text", "options": ["option_text1", "option_text2", "option_text3", "option_text4"]}

**DO NOT SEND ANYTHING ELSE**

**Make sure to always generate 3-4 options**
"""

ending = """
**Please respond with a character from the list in the exact format below:**

{"character": "character_name"}

**DO NOT SEND ANYTHING ELSE**
"""

character_list = creatures = [
    ("Elf", "Tall, graceful beings with pointed ears, known for their longevity and magic."),
    ("Dwarf", "Short, sturdy, and often bearded, they are master craftsmen and miners."),
    ("Dragon", "Large, powerful reptiles that can fly and breathe fire."),
    ("Orc", "Green-skinned, brutish warriors with a savage nature."),
    ("Troll", "Large, slow-witted creatures, often living under bridges or in caves."),
    ("Fairy", "Small, winged beings with magical abilities, often depicted as mischievous."),
    ("Vampire", "Undead creatures that feed on the blood of the living."),
    ("Werewolf", "Humans who can transform into wolves or wolf-like creatures, often during a full moon."),
    ("Mermaid", "Aquatic beings with the upper body of a human and the tail of a fish."),
    ("Goblin", "Small, cunning creatures often associated with thievery and mischief."),
    ("Gnome", "Small, earth-dwelling beings known for their connection to nature and gardening."),
    ("Centaur", "Creatures with the upper body of a human and the lower body of a horse."),
    ("Phoenix", "Mythical birds that can burst into flames and are reborn from their ashes."),
    ("Griffin", "Creatures with the body of a lion and the head and wings of an eagle."),
    ("Unicorn", "Magical horses with a single horn on their forehead, often symbolizing purity."),
    ("Minotaur", "Beings with the body of a human and the head of a bull."),
    ("Zombie", "Reanimated corpses with a hunger for human flesh."),
    ("Giant", "Enormous humanoid beings, often very strong and sometimes simple-minded."),
    ("Nymph", "Nature spirits often associated with particular natural features like trees, rivers, and mountains."),
    ("Demon", "Malevolent supernatural beings often associated with evil and chaos."),
    ("Ghost", "Spirits of the dead that can haunt the living and places."),
    ("Banshee", "A wailing spirit that heralds the death of a family member."),
    ("Harpy", "Creatures with the body of a bird and the face of a woman, known for their vicious nature."),
    ("Kraken", "Enormous sea monsters capable of dragging ships underwater."),
    ("Cyclops", "Giant beings with a single eye in the middle of their forehead."),
    ("Hydra", "Multi-headed serpentine creatures, where cutting off one head causes two more to grow back."),
    ("Chimera", "Monsters with the body of a lion, the head of a goat, and the tail of a serpent."),
    ("Sphinx", "Creatures with the body of a lion and the head of a human, known for their riddles."),
    ("Leprechaun", "Small, bearded men, often associated with Irish folklore and known for their trickery and hidden pots of gold."),
    ("Basilisk", "A serpent king that can cause death with a single glance."),
    ("Satyr", "Half-human, half-goat beings known for their love of music and revelry."),
    ("Kelpie", "Shape-shifting water spirits that often appear as horses and are known for drowning unwary travelers."),
    ("Djinn", "Supernatural beings from Arabian folklore, capable of granting wishes but often with a twist."),
    ("Wendigo", "Cannibalistic spirits from Native American folklore, associated with insatiable hunger and cold environments."),
    ("Pegasus", "Winged horses known for their beauty and ability to fly."),
    ("Chupacabra", "Cryptid known for attacking livestock, particularly goats, and draining their blood."),
    ("Gargoyle", "Stone creatures that come to life, often serving as protectors of buildings."),
    ("Lich", "Powerful undead sorcerers who have achieved immortality through necromancy."),
    ("Boggart", "Shape-shifting creatures that take the form of one's worst fears.")
]

