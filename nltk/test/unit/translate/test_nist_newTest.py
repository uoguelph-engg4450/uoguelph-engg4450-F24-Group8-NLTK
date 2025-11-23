import unittest
from nltk.translate.nist_score import (
    corpus_nist,
    sentence_nist,
    _validate_nist_inputs,
)


class TestNistInputValidation(unittest.TestCase):
    """
    Automated tests for input validation and improved error handling.
    """

    def setUp(self):
        self.refs = [["this", "is", "a", "test"]]
        self.hyp = ["this", "is", "a", "test"]

    # ----------- _validate_nist_inputs Tests -----------

    def test_valid_inputs_pass(self):
        self.assertEqual(_validate_nist_inputs(self.refs, self.hyp, n=2), 2)

    def test_n_less_than_one_raises(self):
        with self.assertRaisesRegex(ValueError, "n must be >= 1"):
            _validate_nist_inputs(self.refs, self.hyp, n=0)

    def test_n_greater_than_hyp_len_warns_and_caps(self):
        with self.assertWarns(UserWarning):
            adjusted_n = _validate_nist_inputs(self.refs, self.hyp, n=10)
        self.assertEqual(adjusted_n, len(self.hyp))

    def test_empty_hypothesis_raises(self):
        with self.assertRaisesRegex(ValueError, "hypothesis must be a non-empty"):
            _validate_nist_inputs(self.refs, [], n=2)

    def test_empty_reference_list_raises(self):
        with self.assertRaisesRegex(ValueError, "references must be a non-empty"):
            _validate_nist_inputs([], self.hyp, n=2)

    def test_empty_reference_sentence_raises(self):
        with self.assertRaisesRegex(ValueError, "references must not contain empty"):
            _validate_nist_inputs([[]], self.hyp, n=2)

    def test_non_integer_n_raises_typeerror(self):
        with self.assertRaisesRegex(TypeError, "n must be an integer"):
            _validate_nist_inputs(self.refs, self.hyp, n=2.5)

    # ----------- sentence_nist Tests -----------

    def test_sentence_nist_runs_valid(self):
        score = sentence_nist(self.refs, self.hyp, n=2)
        self.assertIsInstance(score, float)

    def test_sentence_nist_n_less_than_one(self):
        with self.assertRaisesRegex(ValueError, "n must be >= 1"):
            sentence_nist(self.refs, self.hyp, n=0)

    def test_sentence_nist_warns_and_caps(self):
        with self.assertWarns(UserWarning):
            score = sentence_nist(self.refs, self.hyp, n=10)
        self.assertIsInstance(score, float)

    # ----------- corpus_nist Tests -----------

    def test_corpus_nist_skips_invalid_pairs(self):
        refs1, hyp1 = self.refs, self.hyp
        refs2, hyp2 = self.refs, []
        with self.assertWarns(UserWarning):
            score = corpus_nist([refs1, refs2], [hyp1, hyp2], n=2)
        self.assertIsInstance(score, float)
