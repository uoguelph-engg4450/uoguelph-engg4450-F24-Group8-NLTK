# Test for nltk issue #3047: English stopwords should include smart-quote and colloquial forms
from nltk.corpus import stopwords

def test_english_stopwords_have_contractions_and_slang():
    sw = set(stopwords.words("english"))
    expected = [
        # smart-quote vs straight-quote (a few representatives)
        "i’m","i'm","you’re","you're","it’s","it's","don’t","don't","can’t","can't",
        "won’t","won't","shouldn’t","shouldn't","wasn’t","wasn't","weren’t","weren't",
        # colloquial forms
        "ain’t","ain't","gonna","wanna","gotta","lemme","gimme","coulda","shoulda","woulda",
    ]
    missing = [w for w in expected if w not in sw]
    assert not missing, f"Missing expected stopwords: {missing}"