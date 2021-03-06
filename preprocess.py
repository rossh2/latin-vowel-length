from typing import List

from features import clean_syllable
from parse import read_corpus_words, RAW_DATA_PATH
from syllabify import syllabify, identify_syllable_type

PREPROCESSED_DATA_PATH = './data/Latin_words_preprocessed.txt'
PREPROCESSED_UNIQUE_DATA_PATH = './data/Latin_words_preprocessed_unique.txt'


def preprocess_words(path: str) -> List[List[str]]:
    words = read_corpus_words(path)
    word_count = len(words)
    print(f'Read in {word_count} Latin words')
    syllabified_words = [syllabify(word) for word in words]
    real_syllabified_words = []
    skipped = []
    for word in syllabified_words:
        try:
            for syllable in word:
                cleaned_syllable = clean_syllable(syllable)
                syl_type = identify_syllable_type(cleaned_syllable)
            real_syllabified_words.append(word)
        except ValueError:
            skipped.append(''.join(word))
    print(f'Processed {len(real_syllabified_words)} out of {word_count} words')
    print(f'Skipped the following words: {str(skipped)}')

    return real_syllabified_words


def write_syllabified_words(syllabified_words: List[List[str]], path: str):
    with open(path, mode='w', encoding='utf-8') as out_file:
        for word in syllabified_words:
            line = ' '.join(word) + '\n'
            out_file.write(line)


def read_syllabified_words(path: str) -> List[List[str]]:
    syllabified_words = []
    with open(path, mode='r', encoding='utf-8') as file:
        for line in file:
            syllables = line.split()
            syllables = [syllable.strip() for syllable in syllables]
            syllabified_words.append(syllables)

    return syllabified_words


def write_unique_syllabified_words(in_path: str, out_path: str):
    syllabified_words = read_syllabified_words(in_path)
    unique_syllabified_words = list(
        set(' '.join(word) for word in syllabified_words))
    write_syllabified_words(
        [word.split() for word in unique_syllabified_words],
        out_path)


if __name__ == '__main__':
    syllabified_words = preprocess_words(RAW_DATA_PATH)
    write_syllabified_words(syllabified_words, PREPROCESSED_DATA_PATH)
    write_unique_syllabified_words(PREPROCESSED_DATA_PATH,
                                   PREPROCESSED_UNIQUE_DATA_PATH)
