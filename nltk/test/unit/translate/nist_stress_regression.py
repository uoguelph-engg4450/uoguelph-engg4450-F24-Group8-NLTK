"""
Stress / regression script for nltk.translate.nist_score

This script is designed to:
- Reproduce the scenarios from NLTK Issue #3444
- Exercise additional edge cases that *would* have broken the old code
  (ZeroDivisionError, unhandled invalid inputs)
- Confirm that the new validation logic behaves as expected:
    * ValueError for invalid n (< 1)
    * ValueError for empty hypothesis / references
    * Warnings + capping when n > len(hypothesis)
    * corpus_nist skips invalid sentence pairs instead of crashing
"""

import warnings
from nltk.translate.nist_score import sentence_nist, corpus_nist


def run_case(name, func, *args, **kwargs):
    print("\n" + "=" * 60)
    print(f"CASE: {name}")
    print("=" * 60)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            result = func(*args, **kwargs)
            print("Result:", result)
        except Exception as e:
            print("Raised exception:", repr(e))

        if w:
            print("\nWarnings:")
            for warn in w:
                print(f"  {warn.category.__name__}: {warn.message}")
        else:
            print("\nWarnings: (none)")


def case_issue_3444_n_too_large():
    """
    Directly from the GitHub issue #3444.
    Previously: sentence_nist(..., n=19) -> ZeroDivisionError.
    Now: should either cap/warn or otherwise complete without ZeroDivisionError.
    """
    references = [
        ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
         'ensures', 'that', 'the', 'military', 'will', 'forever',
         'heed', 'Party', 'commands'],
        ['It', 'is', 'the', 'guiding', 'principle', 'which',
         'guarantees', 'the', 'military', 'forces', 'always', 'being',
         'under', 'the', 'command', 'of', 'the', 'Party'],
        ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
         'army', 'always', 'to', 'heed', 'the', 'directions',
         'of', 'the', 'party']
    ]
    hypothesis = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
                  'ensures', 'that', 'the', 'military', 'always',
                  'obeys', 'the', 'commands', 'of', 'the', 'party']

    # len(hypothesis) == 18
    print(f"len(hypothesis) = {len(hypothesis)}")

    # n=19 previously triggered ZeroDivisionError
    return sentence_nist(references, hypothesis, n=19)


def case_issue_3444_n_zero():
    """
    From GitHub issue #3444.
    Previously: n=0 would go through and eventually break.
    Now: should raise ValueError("n must be >= 1").
    """
    references = [["a", "b", "c"]]
    hypothesis = ["a", "b", "c"]
    return sentence_nist(references, hypothesis, n=0)


def case_n_greater_than_len_hyp():
    """
    Simple toy example where n > len(hyp).
    Previously: could trigger ZeroDivisionError.
    Now: should warn and cap n to len(hyp).
    """
    refs = [["a", "b", "c"]]
    hyp = ["a", "b", "c"]
    # len(hyp) = 3, n=5 is too large
    return sentence_nist(refs, hyp, n=5)


def case_empty_hypothesis():
    """
    Previously: empty hypothesis might fall through and cause weird behavior.
    Now: should raise ValueError("hypothesis must be a non-empty ...").
    """
    refs = [["a", "b", "c"]]
    hyp = []
    return sentence_nist(refs, hyp, n=2)


def case_empty_references():
    """
    Previously: empty reference list might cause unexpected crashes.
    Now: should raise ValueError("references must be a non-empty ...").
    """
    refs = []
    hyp = ["a", "b", "c"]
    return sentence_nist(refs, hyp, n=2)


def case_empty_reference_sentence():
    """
    Previously: reference list containing an empty sentence could bubble up
    into ZeroDivisionError / undefined behavior.
    Now: should raise ValueError("references must not contain empty sentences").
    """
    refs = [[]]                  # one empty reference sentence
    hyp = ["a", "b", "c"]
    return sentence_nist(refs, hyp, n=2)


def case_corpus_skips_invalid_pairs():
    """
    corpus_nist should skip invalid pairs instead of crashing.
    Previously: would just crash inside sentence_nist / aggregation.

    Here:
    - first pair is valid
    - second pair has empty hypothesis (invalid)
    Expect:
    - Warning about skipping invalid pair
    - A valid float score returned (based only on the first pair)
    """
    refs1 = [["this", "is", "ok"]]
    hyp1 = ["this", "is", "ok"]

    refs2 = [["this", "is", "ignored"]]
    hyp2 = []  # invalid

    return corpus_nist([refs1, refs2], [hyp1, hyp2], n=2)


def case_corpus_all_invalid_pairs():
    """
    All sentence pairs are invalid.
    Previously: could crash or leave undefined state.
    Now (with our implementation):
    - All pairs skipped
    - Warning "No valid sentence pairs to score"
    - Returns 0.0
    """
    list_of_references = [[[]]]          # empty reference sentence
    hypotheses = [["still", "invalid"]]  # will never be used

    return corpus_nist(list_of_references, hypotheses, n=2)


def case_no_overlapping_ngrams():
    """
    Hypothesis shares no n-grams with references.
    This is a good stress case for denominator logic: numerators are 0,
    denominators may be > 0, NIST precision becomes 0 but MUST NOT crash.
    """
    refs = [["one", "two", "three"]]
    hyp = ["red", "green", "blue"]

    return sentence_nist(refs, hyp, n=2)


if __name__ == "__main__":
    # Each run_case will print:
    # - result OR raised exception
    # - any warnings emitted

    run_case("Issue #3444: n larger than len(hypothesis)", case_issue_3444_n_too_large)
    run_case("Issue #3444: n = 0", case_issue_3444_n_zero)

    run_case("n > len(hypothesis) simple toy", case_n_greater_than_len_hyp)
    run_case("Empty hypothesis", case_empty_hypothesis)
    run_case("Empty references list", case_empty_references)
    run_case("Empty reference sentence in list", case_empty_reference_sentence)

    run_case("corpus_nist: one valid, one invalid pair", case_corpus_skips_invalid_pairs)
    run_case("corpus_nist: all pairs invalid", case_corpus_all_invalid_pairs)

    run_case("No overlapping n-grams (denominator stress test)", case_no_overlapping_ngrams)

    print("\nAll stress tests executed. If you saw any ZeroDivisionError, "
          "the implementation is still broken.")
