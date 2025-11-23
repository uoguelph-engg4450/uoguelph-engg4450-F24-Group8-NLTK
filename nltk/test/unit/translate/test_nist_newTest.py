import unittest
from nltk.translate.nist_score import (
    corpus_nist,
    sentence_nist,
    _validate_nist_inputs,
)
from nltk.translate.nist_score import nist_length_penalty


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
    
    def test_nist_precision_edge_case_zero_denominator(self):
        # Case where hypothesis has no overlapping n-grams → denominator = 0
        refs = [["a", "b", "c"]]
        hyp = ["x", "y", "z"]  # completely different tokens
        score = sentence_nist(refs, hyp, n=1)
        self.assertIsInstance(score, float)

    def test_nist_length_penalty_ratio_greater_equal_one(self):
        # hyp_len >= ref_len triggers alternative LP path
        refs = [["a", "b"]]
        hyp = ["a", "b", "c"]  # longer hypothesis → ratio > 1
        score = sentence_nist(refs, hyp, n=1)
        self.assertIsInstance(score, float)

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

    def test_information_weights_mgram_branch(self):
        # Create references that produce bigrams and unigrams so that
        # the _mgram (n-1 gram) appears in ngram_freq and triggers
        # the numerator = ngram_freq[_mgram] branch in information_weights.
        refs = [["a", "a", "a"]]
        hyp = ["a", "a", "a"]
        score = sentence_nist(refs, hyp, n=2)
        self.assertIsInstance(score, float)

    def test_nist_length_penalty_ratio_between_zero_and_one(self):
        # Directly test the special length-penalty branch where 0 < ratio < 1
        ref_len = 10
        hyp_len = 5
        penalty = nist_length_penalty(ref_len, hyp_len)
        self.assertIsInstance(penalty, float)
        self.assertGreater(penalty, 0.0)
        self.assertLess(penalty, 1.0)

    def test_corpus_nist_all_pairs_invalid_returns_zero(self):
        # Both pairs invalid (empty hypotheses) → function should warn and return 0.0
        refs1, hyp1 = self.refs, []
        refs2, hyp2 = self.refs, []
        with self.assertWarns(UserWarning):
            score = corpus_nist([refs1, refs2], [hyp1, hyp2], n=2)
        self.assertEqual(score, 0.0)

