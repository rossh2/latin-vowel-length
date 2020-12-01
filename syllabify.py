from typing import List

CONSONANTS = 'bcdfghjlmnpqrstvxz'
STOPS_FRICATIVES = 'bcdfgpstv'  # Excluding h (not an oral fricative)
NASALS = 'mn'
ONSET_CLUSTERS = ['ch', 'ph', 'th', 'rh'] \
                 + ['chr', 'phr', 'thr', 'chl', 'phl', 'thl'] \
                 + [c + 'r' for c in STOPS_FRICATIVES] \
                 + [c + 'l' for c in STOPS_FRICATIVES] \
                 + ['s' + c for c in STOPS_FRICATIVES] \
                 + ['s' + n for n in NASALS] \
                 + ['s' + c + 'r' for c in STOPS_FRICATIVES]

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


def syllabify(word: str) -> List[str]:
    if word in diphthong_exceptions:
        return diphthong_exceptions[word]

    syllables = []
    curr_syl = ''
    coda_candidate = ''
    word_iter = iter(word)
    try:
        segment = next(word_iter)
        while True:
            # Onset
            # (onset might be provided by previous iteration -
            # check if curr_syl already contains something)
            if not curr_syl:
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

    return fixed_syllables
