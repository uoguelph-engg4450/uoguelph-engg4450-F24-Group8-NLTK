from nltk.translate.nist_score import sentence_nist

hyp = ["a", "b", "c"]
refs = [["a", "b", "c"]]

print(sentence_nist(refs, hyp, n=5))
