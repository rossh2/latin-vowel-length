from unittest import TestCase
from parse import read_corpus_words
from syllabify import syllabify, identify_syllable_type, SYLLABLE_TYPES


class TestSyllabifyCorpus(TestCase):
    def test_corpus_syllabified(self):
        corpus_words = read_corpus_words('../data/Ryan_Latin_master.txt')
        # print(f'Testing {len(corpus_words)} words...')
        for word in corpus_words:
            syllables = syllabify(word)
            self.assertGreaterEqual(len(syllables), 1)

    def test_corpus_valid_syllables(self):
        corpus_words = read_corpus_words('../data/Ryan_Latin_master.txt')
        for word in corpus_words:
            syllables = syllabify(word)
            for syllable in syllables:
                try:
                    syl_type = identify_syllable_type(syllable)
                    self.assertIn(syl_type, SYLLABLE_TYPES)
                except ValueError as e:
                    print('Word: ' + word)
                    print('Syllables: ' + str(syllables))
                    raise e