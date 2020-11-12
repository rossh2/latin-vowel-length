from string import ascii_letters
from typing import List

RAW_DATA_PATH = 'data/Ryan_Latin_master.txt'
LETTERS_MACRON = ascii_letters + '-'


def read_raw_data() -> List[str]:
    words: List[str] = []
    with open(RAW_DATA_PATH, mode='r', encoding='utf-8') as raw_data:
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
    words = read_raw_data()
    for word in words[:100]:
        print(word)
