from unittest import TestCase
from parse_data import read_corpus_words
from syllabify import syllabify


class TestSyllabifyCorpus(TestCase):
    def test_corpus_syllabified(self):
        corpus_words = read_corpus_words('../data/Ryan_Latin_master.txt')
        print(f'Testing {len(corpus_words)} words...')
        for word in corpus_words:
            syllables = syllabify(word)
            self.assertGreaterEqual(len(syllables), 1)
