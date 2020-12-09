import re
from typing import List

CONSONANTS = 'bcdfghjlmnpqrstvxz'

# Muta cum liquida
STOPS_FRICATIVES = 'bcdfgpst'
APPROX = 'lr'  # v is an approximant ([w]) but does not do muta cum liquida
ONSET_CLUSTERS = [muta + liquida
                  for muta in STOPS_FRICATIVES for liquida in APPROX]
DOUBLE_CONSONANTS = 'xz'

VOWELS = 'aeiouy'
DIPHTHONGS = ['ae', 'au', 'oe']  # + ['ei', 'eu']
MACRON = '-'
diphthong_exceptions = {
    'huius': ['hui', 'ius'],
    'cuius': ['cui', 'ius'],
    'huic': ['huic'],
    'cui': ['cui'],
    'hui': ['hui']
}

VOWEL_REGEX = re.compile(f'(qu)*([{VOWELS}]+)')

# Use C* for two or more consonants. Use CL for muta cum liquida (L as liquid)
# VV for diphthongs
# These are the types returned by identify_syllable_type
SYLLABLE_TYPES = ['V', 'VV',
                  'CV', 'CLV', 'C*V', 'CVV', 'CLVV', 'C*VV',
                  'VC', 'VC*', 'VVC', 'VVC*',
                  'CVC', 'CLVC', 'C*VC', 'CVVC', 'CLVVC', 'C*VVC',
                  'CVC*', 'CLVC*', 'C*VC*', 'CVVC*', 'CLVVC*', 'C*VVC*']


def syllabify(word: str) -> List[str]:
    if word in diphthong_exceptions:
        return diphthong_exceptions[word]

    h_indices = [i for i, s in enumerate(word) if s == 'h']
    word = word.replace('h', '')

    syllables = []
    curr_syl = ''
    coda_candidate = ''
    word_iter = iter(word)
    try:
        segment = next(word_iter)
        while True:
            # Onset
            if not curr_syl:
                # First onset of word
                while segment in CONSONANTS:
                    curr_syl += segment
                    segment = next(word_iter)
            if curr_syl == 'q' and segment == 'u':
                # Special case 'qu' [kw]
                curr_syl += segment
                segment = next(word_iter)

            # Nucleus
            if segment not in VOWELS:
                raise ValueError('Syllabification error: could not find vowel '
                                 'for syllable nucleus in word "{}"'
                                 .format(word))
            curr_syl += segment
            segment = next(word_iter)

            if segment in VOWELS:
                if (curr_syl[-1] + segment) in DIPHTHONGS:
                    curr_syl += segment
                    segment = next(word_iter)
                elif curr_syl == 'i' and segment != 'i':
                    # Treat i as j (as onset)
                    curr_syl += segment
                    segment = next(word_iter)
                else:
                    # Start a new syllable beginning with this vowel
                    syllables.append(curr_syl)
                    curr_syl = ''
                    coda_candidate = ''
                    continue
            if segment == MACRON:
                curr_syl += segment
                segment = next(word_iter)

            # Coda - we have at least one consonant
            while segment in CONSONANTS:
                coda_candidate += segment
                segment = next(word_iter)

            if coda_candidate:
                # We now have the nucleus of the next syllable ready
                # so we need to give it back its onset
                if len(coda_candidate) >= 3 \
                        and coda_candidate[-3:] in ONSET_CLUSTERS:
                    # We captured the onset and it's a special triple
                    curr_syl += coda_candidate[:-3]
                    syllables.append(curr_syl)
                    curr_syl = coda_candidate[-3:]
                    coda_candidate = ''
                elif len(coda_candidate) >= 2 \
                        and coda_candidate[-2:] in ONSET_CLUSTERS:
                    # We captured the onset and it's a special pair
                    curr_syl += coda_candidate[:-2]
                    syllables.append(curr_syl)
                    curr_syl = coda_candidate[-2:]
                    coda_candidate = ''
                else:
                    # We captured a single-consonant onset
                    curr_syl += coda_candidate[:-1]
                    syllables.append(curr_syl)
                    curr_syl = coda_candidate[-1]
                    coda_candidate = ''
            else:
                # Syllable ended in a vowel with a macron
                syllables.append(curr_syl)
                curr_syl = ''
                coda_candidate = ''

    except StopIteration:
        # Done!
        curr_syl += coda_candidate
        syllables.append(curr_syl)

    # Fix diphthongs with macrons
    # ("hack" based on the way the annotation works; won't do anything for
    # unannotated data but at least we're not training on incorrectly
    # syllabified data)
    fixed_syllables = []
    for syllable in syllables:
        if syllable.endswith(MACRON) and syllable[-3:-1] in DIPHTHONGS:
            # VV- should be V.V-
            fixed_syllables.append(syllable[:-2])
            fixed_syllables.append(syllable[-2:])
        else:
            fixed_syllables.append(syllable)

    # Insert h's that were removed/ignored (respect the orthography)
    i = 0
    final_syllables = []
    for syllable in fixed_syllables:
        new_syllable = ''
        for segment in syllable:
            if i in h_indices:
                new_syllable += 'h'
                i += 1
            new_syllable += segment
            i += 1
        final_syllables.append(new_syllable)

    return final_syllables


def identify_syllable_type(syllable: str) -> str:
    syllable = syllable.replace('h', '')
    if syllable[0] in VOWELS:
        return identify_syllable_type_V(syllable)
    else:
        # Syllable starts with consonant
        if len(syllable) == 1:
            raise ValueError(
                f'Invalid syllable structure "C" for syllable {syllable}')
        else:
            # Figure out what the onset is
            if syllable[:2] == 'qu':
                return identify_syllable_type_CL(syllable)
            elif syllable[1] in VOWELS:
                # CV...
                return identify_syllable_type_CV(syllable)
            elif syllable[1] in APPROX:
                # CL...
                return identify_syllable_type_CL(syllable)
            else:
                # C*...
                return identify_syllable_type_Cstar(syllable)


def identify_syllable_type_V(syllable: str) -> str:
    if len(syllable) == 1:
        return 'V'
    elif syllable[1] in VOWELS:
        # VV...
        coda = syllable[2:]
        if len(coda) == 0:
            return 'VV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'VVC'
        else:
            return 'VVC*'
    else:
        # VC...
        coda = syllable[1:]
        if len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'VC'
        else:
            return 'VC*'


def identify_syllable_type_CV(syllable: str) -> str:
    if len(syllable) > 2 and syllable[2] in VOWELS:
        # CVV...
        coda = syllable[3:]
        if coda and coda[0] in VOWELS:
            raise ValueError(f'Invalid nucleus "VVV" for syllable {syllable}')
        if len(coda) == 0:
            return 'CVV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'CVVC'
        else:
            return 'CVVC*'
    else:
        # CV(C)...
        coda = syllable[3:] if syllable[:2] == 'qu' else syllable[2:]
        if len(coda) == 0:
            return 'CV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'CVC'
        else:
            return 'CVC*'


def identify_syllable_type_CL(syllable: str) -> str:
    if len(syllable) == 2:
        raise ValueError(
            f'Invalid syllable structure "CL" for syllable {syllable}')
    if len(syllable) > 3 and syllable[3] in VOWELS:
        # CLVV...
        coda = syllable[4:]
        if coda and coda[0] in VOWELS:
            raise ValueError(f'Invalid nucleus "VVV" for syllable {syllable}')
        if len(coda) == 0:
            return 'CLVV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'CLVVC'
        else:
            return 'CLVVC*'
    else:
        # CLV(C)...
        coda = syllable[3:]
        if len(coda) == 0:
            return 'CLV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'CLVC'
        else:
            return 'CLVC*'


def identify_syllable_type_Cstar(syllable: str) -> str:
    vowel_indices = [i for i, s in enumerate(syllable)
                     if s in VOWELS]
    if len(vowel_indices) == 0:
        raise ValueError(
            f'Invalid syllable structure: C* for syllable {syllable}')
    coda = syllable[(vowel_indices[-1] + 1):]
    if len(vowel_indices) == 1:
        # C*V(C)...
        if len(coda) == 0:
            return 'C*V'
        if len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'C*VC'
        else:
            return 'C*VC*'
    elif len(vowel_indices) == 2 and vowel_indices[0] + 1 == vowel_indices[1]:
        # C*VV(C)...
        if len(coda) == 0:
            return 'C*VV'
        elif len(coda) == 1 and coda not in DOUBLE_CONSONANTS:
            return 'C*VVC'
        else:
            return 'C*VVC*'
    else:
        raise ValueError(
            f'Invalid nucleus "VVV" or non-adjacent Vs for syllable {syllable}')


def get_coda_type(syllable_type: str) -> str:
    if syllable_type.endswith('C*'):
        return 'C*'
    elif syllable_type.endswith('C'):
        return 'C'
    else:
        return ''


def is_diphthong(syllable: str) -> bool:
    for diphthong in DIPHTHONGS:
        if diphthong in syllable:
            return True
    return False


def extract_vowels(syllable: str) -> str:
    match = VOWEL_REGEX.search(syllable)
    if not match:
        raise ValueError(f'Invalid syllable {syllable} contains no vowels')
    return match.group(2)


def extract_coda(syllable: str) -> str:
    vowel_indices = [i for i, s in enumerate(syllable)
                     if s in VOWELS]
    if len(vowel_indices) == 0:
        raise ValueError(f'Invalid syllable {syllable} contains no vowels')
    coda = syllable[(vowel_indices[-1] + 1):]
    return coda
