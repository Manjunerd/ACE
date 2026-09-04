from ace_agent.voice import LanguageDetector

def test_languages():
    d=LanguageDetector(); assert d.detect("Open Chrome")=='en'; assert d.detect("క్రోమ్ తెరువు")=='te'; assert d.detect("क्रोम खोलो")=='hi'
