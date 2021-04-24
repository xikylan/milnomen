from app import db, Language, Sentence, TranslatedSentence, Word, TranslatedWord
from sys import argv

lang = Language.query.filter_by(name=argv[1]).first()
rare = []


words = Word.query.filter_by(language=lang).all()

print("Currently", len(words), lang.name, "words")

for w in words:
    if len(w.sentences) < 15:
        rare.append(w)

print("Deleting", len(rare), "words")

for w in rare:
    sentences = w.sentences
    for s in sentences:
        trans = TranslatedSentence.query.filter_by(sentence=s).all()
        for tr in trans:
            db.session.delete(tr)
            db.session.commit()

        db.session.delete(s)
        db.session.commit()

for w in rare:
    for tr in w.translations:
        db.session.delete(tr)
        db.session.commit()

    db.session.delete(w)
    db.session.commit()

print(Word.query.count(), lang.name, "words remaining")
