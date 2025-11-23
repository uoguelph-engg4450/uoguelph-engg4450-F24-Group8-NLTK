from nltk.translate.nist_score import sentence_nist

hyp = ["a", "b", "c"]
refs = [["a", "b", "c"]]

print("Case 1: n > len(hyp)")
print(sentence_nist(refs, hyp, n=5))   # should WARN + return float, no crash

print("Case 2: n < 1 (expect ValueError)")
try:
    print(sentence_nist(refs, hyp, n=0))
except Exception as e:
    print("Caught:", repr(e))