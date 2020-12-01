from string import ascii_letters
from typing import List

RAW_DATA_PATH = 'data/Ryan_Latin_master.txt'
LETTERS_MACRON = ascii_letters + '-'


def read_corpus_words(path: str) -> List[str]:
    words: List[str] = []
    with open(path, mode='r', encoding='utf-8') as raw_data:
        for line in raw_data:
            if not line.isspace() and not line.startswith('#'):
                line_words = line.split()
                words.extend(line_words)

    return [clean_punctuation(word) for word in words]


def clean_punctuation(word: str) -> str:
    """Strip any characters which aren't letters or macrons"""
    clean_word = ''.join(filter(lambda i: i in LETTERS_MACRON, word))
    return clean_word


if __name__ == '__main__':
    words = read_corpus_words(RAW_DATA_PATH)
    for word in words[:100]:
        print(word)
