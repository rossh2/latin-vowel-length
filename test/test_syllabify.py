from unittest import TestCase, skip

from syllabify import syllabify, identify_syllable_type


class TestSyllabify(TestCase):
    # Basic syllables
    def test_v(self):
        word = 'a'
        syllables = syllabify(word)
        self.assertEqual(['a'], syllables)

    def test_vc(self):
        word = 'in'
        syllables = syllabify(word)
        self.assertEqual(['in'], syllables)

    def test_cv(self):
        word = 'tu'
        syllables = syllabify(word)
        self.assertEqual(['tu'], syllables)

    def test_cvc(self):
        word = 'sum'
        syllables = syllabify(word)
        self.assertEqual(['sum'], syllables)

    def test_vcc(self):
        word = 'est'
        syllables = syllabify(word)
        self.assertEqual(['est'], syllables)

    def test_cvcv(self):
        word = 'tibi'
        syllables = syllabify(word)
        self.assertEqual(['ti', 'bi'], syllables)

    def test_cvcvc(self):
        word = 'bonum'
        syllables = syllabify(word)
        self.assertEqual(['bo', 'num'], syllables)

    def test_cvccvc(self):
        word = 'tantum'
        syllables = syllabify(word)
        self.assertEqual(['tan', 'tum'], syllables)

    def test_cvrcvc(self):
        word = 'partes'
        syllables = syllabify(word)
        self.assertEqual(['par', 'tes'], syllables)

    def test_vccvc(self):
        word = 'omnes'
        syllables = syllabify(word)
        self.assertEqual(['om', 'nes'], syllables)

    def test_cvccvv(self):
        word = 'gallia'
        syllables = syllabify(word)
        self.assertEqual(['gal', 'li', 'a'], syllables)

    def test_cvvc_eu(self):
        word = 'deum'
        syllables = syllabify(word)
        self.assertEqual(['de', 'um'], syllables)

    def test_cvv_ei(self):
        word = 'dei'
        syllables = syllabify(word)
        self.assertEqual(['de', 'i'], syllables)

    def test_vcvvc_iu(self):
        word = 'alium'
        syllables = syllabify(word)
        self.assertEqual(['a', 'li', 'um'], syllables)

    def test_vcvv_ia(self):
        word = 'alia'
        syllables = syllabify(word)
        self.assertEqual(['a', 'li', 'a'], syllables)

    # Liquids/glides
    def test_crvc(self):
        word = 'tres'
        syllables = syllabify(word)
        self.assertEqual(['tres'], syllables)

    def test_clvcvcc(self):
        word = 'placent'
        syllables = syllabify(word)
        self.assertEqual(['pla', 'cent'], syllables)

    def test_cviv(self):
        word = 'caia'
        syllables = syllabify(word)
        self.assertEqual(['ca', 'ia'], syllables)

    def test_vivc(self):
        word = 'eius'
        syllables = syllabify(word)
        self.assertEqual(['e', 'ius'], syllables)

    def test_quiv(self):
        word = 'quia'
        syllables = syllabify(word)
        self.assertEqual(['qui', 'a'], syllables)

    def test_j(self):
        word = 'ejjus'
        syllables = syllabify(word)
        self.assertEqual(['ej', 'jus'], syllables)

    # y as vowel
    def test_y(self):
        word = 'tyrannus'
        syllables = syllabify(word)
        self.assertEqual(['ty', 'ran', 'nus'], syllables)

    # Onset consonant clusters
    def test_sp(self):
        word = 'spectant'
        syllables = syllabify(word)
        self.assertEqual(['spec', 'tant'], syllables)

    def test_st_initial(self):
        word = 'stabat'
        syllables = syllabify(word)
        self.assertEqual(['sta', 'bat'], syllables)

    def test_st_medial(self):
        word = 'instare'
        syllables = syllabify(word)
        self.assertEqual(['ins', 'ta', 're'], syllables)

    def test_sc(self):
        word = 'scelere'
        syllables = syllabify(word)
        self.assertEqual(['sce', 'le', 're'], syllables)

    def test_str(self):
        word = 'stratum'
        syllables = syllabify(word)
        self.assertEqual(['stra', 'tum'], syllables)

    def test_qu_initial(self):
        word = 'qua'
        syllables = syllabify(word)
        self.assertEqual(['qua'], syllables)

    def test_qu_medial(self):
        word = 'aqua'
        syllables = syllabify(word)
        self.assertEqual(['a', 'qua'], syllables)

    def test_th(self):
        word = 'theseus'
        syllables = syllabify(word)
        self.assertEqual(['the', 'se', 'us'], syllables)

    def test_ph(self):
        word = 'pharmacum'
        syllables = syllabify(word)
        self.assertEqual(['phar', 'ma', 'cum'], syllables)

    def test_phl(self):
        word = 'phlox'
        syllables = syllabify(word)
        self.assertEqual(['phlox'], syllables)

    def test_ch(self):
        word = 'pulcher'
        syllables = syllabify(word)
        self.assertEqual(['pul', 'cher'], syllables)

    def test_chr(self):
        word = 'pulchra'
        syllables = syllabify(word)
        self.assertEqual(['pul', 'chra'], syllables)

    def test_rh(self):
        word = 'rhenum'
        syllables = syllabify(word)
        self.assertEqual(['rhe', 'num'], syllables)

    def test_pt_initial(self):
        word = 'ptianii'  # Name of a people (loanword)
        syllables = syllabify(word)
        self.assertEqual(['pti', 'a', 'ni', 'i'], syllables)

    def test_pt_medial(self):
        word = 'captus'
        syllables = syllabify(word)
        self.assertEqual(['cap', 'tus'], syllables)

    # Diphthongs
    def test_ae(self):
        word = 'bonae'
        syllables = syllabify(word)
        self.assertEqual(['bo', 'nae'], syllables)

    def test_au(self):
        word = 'aurum'
        syllables = syllabify(word)
        self.assertEqual(['au', 'rum'], syllables)

    def test_oe(self):
        word = 'coeli'
        syllables = syllabify(word)
        self.assertEqual(['coe', 'li'], syllables)

    @skip('Can\'t distinguish between ei with long e/i (dei) '
          'and ei as diphthong')
    def test_ei_diphth(self):
        word = 'deinde'
        syllables = syllabify(word)
        self.assertEqual(['dei', 'nde'], syllables)

    @skip('Can\'t distinguish between eu with long e (deus) '
          'and eu as diphthong')
    def test_eu_diphth(self):
        word = 'seu'
        syllables = syllabify(word)
        self.assertEqual(['seu'], syllables)

    @skip('Can\'t distinguish between oe with long e (coegit) '
          'and oe as diphthong')
    def test_oe_not_diphth(self):
        word = 'coegit'  # coe-git
        syllables = syllabify(word)
        self.assertEqual(['co', 'e', 'git'], syllables)

    # Diphthong exceptions
    def test_ui(self):
        word = 'fuit'
        syllables = syllabify(word)
        self.assertEqual(['fu', 'it'], syllables)

    def test_huius(self):
        word = 'huius'
        syllables = syllabify(word)
        self.assertEqual(['hui', 'ius'], syllables)

    def test_cui(self):
        word = 'cui'
        syllables = syllabify(word)
        self.assertEqual(['cui'], syllables)

    # Macrons (n.B. not all these examples are realistic for vowel length)
    # TODO replace with real Latin words where possible
    def test_vm(self):
        word = 'a-'
        syllables = syllabify(word)
        self.assertEqual(['a-'], syllables)

    def test_vmc(self):
        word = 'i-n'
        syllables = syllabify(word)
        self.assertEqual(['i-n'], syllables)

    def test_cvm(self):
        word = 'se-'
        syllables = syllabify(word)
        self.assertEqual(['se-'], syllables)

    def test_cvmc(self):
        word = 'ha-c'
        syllables = syllabify(word)
        self.assertEqual(['ha-c'], syllables)

    def test_ccvmcc(self):
        word = 'ple-bs'
        syllables = syllabify(word)
        self.assertEqual(['ple-bs'], syllables)

    def test_cvmcvmcv(self):
        word = 're-gna-re'
        syllables = syllabify(word)
        self.assertEqual(['re-g', 'na-', 're'], syllables)

    def test_cvmvc(self):
        word = 'de-us'
        syllables = syllabify(word)
        self.assertEqual(['de-', 'us'], syllables)

    def test_dipthm(self):
        word = 'coe-git'
        syllables = syllabify(word)
        self.assertEqual(['co', 'e-', 'git'], syllables)


class TestIdentifySyllableType(TestCase):
    def test_v(self):
        syllable = 'a'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('V', syl_type)

    def test_vv(self):
        syllable = 'ei'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('VV', syl_type)

    def test_cv(self):
        syllable = 'de'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CV', syl_type)

    def test_chv(self):
        syllable = 'rhe'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CV', syl_type)

    def test_quv(self):
        syllable = 'qui'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLV', syl_type)

    def test_clv(self):
        syllable = 'pre'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLV', syl_type)

    def test_chlv(self):
        syllable = 'chra'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLV', syl_type)

    def test_c2v(self):
        syllable = 'sta'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*V', syl_type)

    def test_c3v(self):
        syllable = 'stra'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*V', syl_type)

    def test_cvv(self):
        syllable = 'cui'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVV', syl_type)

    def test_chvv(self):
        syllable = 'chae'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVV', syl_type)

    def test_quvv(self):
        syllable = 'quae'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVV', syl_type)

    def test_clvv(self):
        syllable = 'plae'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVV', syl_type)

    def test_chlvv(self):
        syllable = 'chrae'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVV', syl_type)

    def test_cstarvv(self):
        syllable = 'stae'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*VV', syl_type)

    def test_vc(self):
        syllable = 'at'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('VC', syl_type)

    def test_vcstar(self):
        syllable = 'ast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('VC*', syl_type)

    def test_vvc(self):
        syllable = 'aes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('VVC', syl_type)

    def test_vvcstar(self):
        syllable = 'aest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('VVC*', syl_type)

    def test_cvc(self):
        syllable = 'non'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVC', syl_type)

    def test_chvc(self):
        syllable = 'phis'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVC', syl_type)

    def test_quvc(self):
        syllable = 'quis'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC', syl_type)

    def test_clvc(self):
        syllable = 'plis'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC', syl_type)

    def test_chlvc(self):
        syllable = 'phris'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC', syl_type)

    def test_cstarvc(self):
        syllable = 'stis'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*VC', syl_type)

    def test_cvvc(self):
        syllable = 'taes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVVC', syl_type)

    def test_chvvc(self):
        syllable = 'chaes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVVC', syl_type)

    def test_quvvc(self):
        syllable = 'quaes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC', syl_type)

    def test_clvvc(self):
        syllable = 'plaes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC', syl_type)

    def test_chlvvc(self):
        syllable = 'phraes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC', syl_type)

    def test_cstarvvc(self):
        syllable = 'staes'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*VVC', syl_type)

    def test_cvcstar(self):
        syllable = 'cast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVC*', syl_type)

    def test_chvcstar(self):
        syllable = 'chast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVC*', syl_type)

    def test_quvcstar(self):
        syllable = 'quast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC*', syl_type)

    def test_clvcstar(self):
        syllable = 'clast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC*', syl_type)

    def test_chlvcstar(self):
        syllable = 'chlast'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVC*', syl_type)

    def test_cstarvcstar(self):
        syllable = 'scest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*VC*', syl_type)

    def test_cvvcstar(self):
        syllable = 'caest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVVC*', syl_type)

    def test_chvvcstar(self):
        syllable = 'phaest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CVVC*', syl_type)

    def test_quvvcstar(self):
        syllable = 'quaest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC*', syl_type)

    def test_clvvcstar(self):
        syllable = 'plaest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC*', syl_type)

    def test_chlvvcstar(self):
        syllable = 'phlaest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('CLVVC*', syl_type)

    def test_cstarvvcstar(self):
        syllable = 'scaest'
        syl_type = identify_syllable_type(syllable)
        self.assertEqual('C*VVC*', syl_type)