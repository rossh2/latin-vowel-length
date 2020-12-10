from collections import defaultdict
from typing import List, Dict, Iterable

from syllabify import identify_syllable_type, is_diphthong, extract_vowels, \
    extract_coda, get_coda_type

UNK = 'UNK'
UNK_VOCABULARY = [UNK]

VOCAB_FEATURE = 'whole syllable (vocab)'  # formerly known as 'vocab'
SYLLABLE_TYPE_FEATURE = 'syllable type'
ADJ_TYPE_FEATURE = 'adjacent syllable type'
CODA_TYPE_FEATURE = 'coda type'
ADJ_CODA_TYPE_FEATURE = 'adjacent coda type'
VOWEL_FEATURE = 'vowel'
CODA_FEATURE = 'coda'
RHYME_FEATURE = 'rhyme'
DIPHTHONG_FEATURE = 'diphthong'
VCC_FEATURE = 'VCC'
CONSONANTAL_I_FEATURE = 'consonantal \'i\''
POSTINIT_FEATURE = '(post)initial'
ANTEPEN_FEATURE = '((ante)pen)ultimate'
QUE_FEATURE = '((ante)pen)ultimate + que'
EVEN_ODD_FEATURE = 'even/odd index'

ALL_FEATURES = frozenset({
    VOCAB_FEATURE,
    SYLLABLE_TYPE_FEATURE, DIPHTHONG_FEATURE, CODA_TYPE_FEATURE,
    VOWEL_FEATURE, CODA_FEATURE, RHYME_FEATURE, VCC_FEATURE,
    POSTINIT_FEATURE, ANTEPEN_FEATURE, QUE_FEATURE, EVEN_ODD_FEATURE,
    ADJ_TYPE_FEATURE, ADJ_CODA_TYPE_FEATURE, CONSONANTAL_I_FEATURE
})
RHYME_AND_TYPE_FEATURES = frozenset({
    SYLLABLE_TYPE_FEATURE, DIPHTHONG_FEATURE, CODA_TYPE_FEATURE,
    VOWEL_FEATURE, CODA_FEATURE, RHYME_FEATURE, VCC_FEATURE,
    POSTINIT_FEATURE, ANTEPEN_FEATURE, QUE_FEATURE, EVEN_ODD_FEATURE,
    ADJ_TYPE_FEATURE, ADJ_CODA_TYPE_FEATURE, CONSONANTAL_I_FEATURE
})
RHYME_AND_CODA_TYPE_FEATURES = frozenset({
    DIPHTHONG_FEATURE, CODA_TYPE_FEATURE,
    VOWEL_FEATURE, CODA_FEATURE, RHYME_FEATURE, VCC_FEATURE,
    POSTINIT_FEATURE, ANTEPEN_FEATURE, QUE_FEATURE, EVEN_ODD_FEATURE,
    ADJ_CODA_TYPE_FEATURE, CONSONANTAL_I_FEATURE
})
TYPE_ONLY_FEATURES = frozenset({
    SYLLABLE_TYPE_FEATURE, DIPHTHONG_FEATURE, CODA_TYPE_FEATURE,
    VOWEL_FEATURE, CODA_FEATURE, VCC_FEATURE,
    POSTINIT_FEATURE, ANTEPEN_FEATURE, QUE_FEATURE, EVEN_ODD_FEATURE,
    ADJ_TYPE_FEATURE, ADJ_CODA_TYPE_FEATURE, CONSONANTAL_I_FEATURE
})
CODA_TYPE_ONLY_FEATURES = frozenset({
    DIPHTHONG_FEATURE, CODA_TYPE_FEATURE,
    VOWEL_FEATURE, CODA_FEATURE, VCC_FEATURE,
    POSTINIT_FEATURE, ANTEPEN_FEATURE, QUE_FEATURE, EVEN_ODD_FEATURE,
    ADJ_CODA_TYPE_FEATURE, CONSONANTAL_I_FEATURE
})


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
    if len(vocabulary) <= max_size:
        return list(vocabulary.keys())

    sorted_vocab = sorted(vocabulary.items(), key=lambda item: item[1],
                          reverse=True)
    capped_vocab = list(
        map(lambda item: item[0], sorted_vocab[:(max_size - 1)]))

    if UNK not in capped_vocab:
        capped_vocab.insert(0, UNK)

    return capped_vocab


def extract_features(syllables: List[str], vocabulary: Iterable[str],
                     use_features=ALL_FEATURES) \
        -> List[Dict[str, float]]:
    features: List[Dict[str, float]] = []
    syl_length = len(syllables)
    ult_i = syl_length - 1
    penult_i = syl_length - 2
    antepenult_i = syl_length - 3

    cleaned_syllables = [clean_syllable(syllable) for syllable in syllables]
    syllable_types = [identify_syllable_type(syllable)
                      for syllable in cleaned_syllables]

    for i in range(syl_length):
        # Use for-i so that adjacent syllables can be accessed if needed
        feature_dict = defaultdict(float)

        cleaned_syllable = cleaned_syllables[i]
        vowels = extract_vowels(cleaned_syllable)
        coda = extract_coda(cleaned_syllable)

        if VOCAB_FEATURE in use_features:
            # Add basic feature for each syllable in vocabulary
            if cleaned_syllable in vocabulary:
                feature_dict[cleaned_syllable] = 1.0
            else:
                feature_dict[UNK] = 1.0

        if SYLLABLE_TYPE_FEATURE in use_features:
            syl_type = syllable_types[i]
            feature_dict['TYPE=' + syl_type] = 1.0

        if CODA_TYPE_FEATURE in use_features:
            coda_type = get_coda_type(syllable_types[i])
            if coda_type:
                feature_dict['CODA_TYPE=' + coda_type] = 1.0
            else:
                feature_dict['NO_CODA'] = 1.0

        if ADJ_TYPE_FEATURE in use_features:
            if i != 0:
                pre_type = syllable_types[i - 1]
                feature_dict['PRE_TYPE=' + pre_type] = 1.0
            if i != ult_i:
                post_type = syllable_types[i + 1]
                feature_dict['POST_TYPE=' + post_type] = 1.0

        if ADJ_CODA_TYPE_FEATURE in use_features:
            if i != 0:
                pre_coda_type = get_coda_type(syllable_types[i - 1])
                if pre_coda_type:
                    feature_dict['PRE_CODA_TYPE=' + pre_coda_type] = 1.0
                else:
                    feature_dict['NO_PRE_CODA'] = 1.0
            if i != ult_i:
                post_coda_type = get_coda_type(syllable_types[i + 1])
                if post_coda_type:
                    feature_dict['POST_CODA_TYPE=' + post_coda_type] = 1.0
                else:
                    feature_dict['NO_POST_CODA'] = 1.0

        if VOWEL_FEATURE in use_features:
            if not (DIPHTHONG_FEATURE in use_features and len(vowels) > 1):
                # No need to mark diphthongs twice,
                # DIPHTHONG is a better feature
                feature_dict['VOWEL=' + vowels] = 1.0

        if DIPHTHONG_FEATURE in use_features:
            # All diphthongs are long
            if len(vowels) > 1:
                feature_dict['DIPHTHONG'] = 1.0

        if CODA_FEATURE in use_features:
            if coda:
                feature_dict['CODA=' + coda] = 1.0
            else:
                feature_dict['NO_CODA'] = 1.0

        if RHYME_FEATURE in use_features:
            # TODO use vocabulary of rhymes or allow all?
            rhyme = vowels + coda
            feature_dict['RHYME=' + rhyme] = 1.0

        if VCC_FEATURE in use_features:
            # A vowel followed by two consonants (except muta cum liquida)
            # is always short, even if they're split across coda/onset
            # of this and the following syllable
            syl_type = syllable_types[i]
            post_syl_type = syllable_types[i + 1] if i != ult_i else ''
            if syl_type.endswith('C*') or (syl_type.endswith('C')
                                           and post_syl_type.startswith('CV')):
                feature_dict['VCC'] = 1.0

        if CONSONANTAL_I_FEATURE in use_features:
            if syllable_types[i].startswith('V') \
                    and i != 0 and syllables[i - 1] == 'i':
                # Guess that 'i' in previous syllable might actually be
                # consonantal i (i.e. the onset of this syllable)
                feature_dict['PRE_I'] = 1.0
            if 'i' not in syllables[i] \
                    and i != ult_i and syllables[i + 1] == 'i':
                # Guess that the 'i' in the next syllable might actually be
                # consonantal i, making this syllable short
                feature_dict['POST_I'] = 1.0

        if POSTINIT_FEATURE in use_features:
            if i == 0:
                feature_dict['INIT'] = 1.0
            elif i == 1:
                feature_dict['POSTINIT'] = 1.0

        if ANTEPEN_FEATURE in use_features:
            # Ultimate, penultimate and antepenultimate
            if i == ult_i:
                feature_dict['ULT'] = 1.0
            elif i == penult_i:
                feature_dict['PENULT'] = 1.0
            elif i == antepenult_i:
                feature_dict['ANTEPENULT'] = 1.0

        if QUE_FEATURE in use_features and ANTEPEN_FEATURE in use_features:
            next_syl = cleaned_syllables[i + 1] if i != ult_i else None
            if next_syl == 'que':
                if i == ult_i - 1:
                    feature_dict['ULT+QUE'] = 1.0
                elif i == penult_i - 1:
                    feature_dict['PENULT+QUE'] = 1.0
                elif i == antepenult_i - 1:
                    feature_dict['ANTEPENULT+QUE'] = 1.0

        if EVEN_ODD_FEATURE in use_features:
            if i % 2 == 0:
                feature_dict['EVEN'] = 1.0
            else:
                feature_dict['ODD'] = 1.0

        features.append(feature_dict)

    return features


def clean_syllable(syllable: str) -> str:
    return syllable.replace('-', '')


def is_long_syllable(syllable: str) -> bool:
    return '-' in syllable or is_diphthong(syllable)
