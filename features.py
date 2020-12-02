from collections import defaultdict
from typing import List, Dict, Iterable

from syllabify import identify_syllable_type

UNK = 'UNK'


def build_syllable_vocabulary(words: List[List[str]]) -> Dict[str, int]:
    vocab: Dict[str, int] = defaultdict(int)

    for word in words:
        for syllable in word:
            # Remove macrons
            cleaned_syllable = clean_syllable(syllable)
            vocab[cleaned_syllable] += 1

    vocab[UNK] = 1
    return vocab


def cap_vocabulary(vocabulary: Dict[str, int], max_size: int) -> List[str]:
    sorted_vocab = sorted(vocabulary.items(), key=lambda item: item[1],
                          reverse=True)
    capped_vocab = list(map(lambda item: item[0], sorted_vocab[:(max_size-1)]))

    capped_vocab.insert(0, UNK)
    return capped_vocab


def extract_features(syllables: List[str], vocabulary: Iterable[str]) \
        -> List[Dict[str, float]]:
    features: List[Dict[str, float]] = []
    syl_length = len(syllables)
    ult_i = syl_length - 1
    penult_i = syl_length - 2
    antepenult_i = syl_length - 3

    for i in range(syl_length):
        # Use for-i so that adjacent syllables can be accessed if needed
        feature_dict = defaultdict(float)

        # Add basic feature for each syllable in vocabulary
        cleaned_syllable = clean_syllable(syllables[i])
        if cleaned_syllable in vocabulary:
            feature_dict[cleaned_syllable] = 1.0
        else:
            feature_dict[UNK] = 1.0

        # Add syllable type
        syl_type = identify_syllable_type(cleaned_syllable)
        feature_dict['TYPE=' + syl_type] = 1.0

        # Ultimate, penultimate and antepenultimate
        if i == ult_i:
            feature_dict['ULT'] = 1.0
        elif i == penult_i:
            feature_dict['PENULT'] = 1.0
        elif i == antepenult_i:
            feature_dict['ANTEPENULT'] = 1.0

        features.append(feature_dict)

    return features


def clean_syllable(syllable: str) -> str:
    return syllable.replace('-', '')