import os

import deepl
import pandas as pd
from googletrans import Translator
from tqdm import tqdm, trange

auth_key = os.environ.get("DEEPL_KEY", "")  # Replace with your key
translator_deepl = deepl.Translator(auth_key)

# Initialize the translator
translator_google = Translator()


# Abstract translation function for a list of texts
def translate_google(texts_en, language):
    translations = []
    for text in tqdm(
        texts_en, desc=f"Google processing chunk en->{language} {len(texts_en)} lines"
    ):
        translations.append(
            translator_google.translate(text, src="en", dest=language.lower())
        )
    return [translation.text for translation in translations]


def translate_deepl(texts_en, language):
    translations = translator_deepl.translate_text(
        texts_en, source_lang="EN", target_lang=language.upper(), formality="less"
    )
    return [translation.text for translation in translations]


# Function to translate a DataFrame chunk
def translate_chunk(chunk, language):
    translate_func = translate_google
    prefix = chunk["key"].iloc[0].split("_")[0]
    if prefix == "Q" or prefix == "CH":
        translate_func = translate_deepl
    chunk_texts = chunk["en"].tolist()
    translated_texts = translate_func(chunk_texts, language)
    chunk[language] = translated_texts
    return chunk


# Load the CSV file
file_name = "translation/questions_translation.csv"
df = pd.read_csv(file_name)

# List of languages to translate to
languages = ["ru"]
checkpoint_file = f'{file_name.split(".")[0]}_en_{"_".join(languages)}_checkpoint.csv'

if os.path.exists(checkpoint_file):
    # Load from checkpoint
    df_translated = pd.read_csv(file_name)
    checkpoint_df = pd.read_csv(checkpoint_file)
    start_idx = len(checkpoint_df)

    df_translated = pd.concat(
        [checkpoint_df, df_translated.iloc[start_idx:]], ignore_index=True
    )
    print(f"Resuming from checkpoint at line {start_idx}")
else:
    # Load the full original file
    df_translated = pd.read_csv(file_name)
    start_idx = 0
    for lang in languages:
        if lang not in df_translated.columns:
            df_translated[lang] = None

# Process the DataFrame in batches
chunk_size = 100

for lang in languages:
    for i in trange(start_idx, len(df), chunk_size, desc=f"Translating to {lang}"):
        chunk = df_translated.iloc[
            i : i + chunk_size
        ].copy()  # Ensure we have a copy of the chunk
        translated_chunk = translate_chunk(chunk, lang)

        # Update the main DataFrame with the translated chunk
        df_translated.iloc[
            i : i + chunk_size, df_translated.columns.get_loc(lang)
        ] = translated_chunk[lang]

        # Crop the DataFrame to the last fully translated line before saving the checkpoint
        checkpoint_df = df_translated.iloc[: i + chunk_size]

        # Save the cropped checkpoint
        checkpoint_df.to_csv(checkpoint_file, index=False)
        print(f"Checkpoint {checkpoint_file} saved at line {i + chunk_size}")

# Save the translated DataFrame to a new CSV file
output_file = "final_files/questions_translation.csv"
df_translated.to_csv(output_file, index=False)

print(f"File saved as {output_file}")
