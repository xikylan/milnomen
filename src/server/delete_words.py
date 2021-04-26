from app import Language, Word, TranslatedWord, Sentence, TranslatedSentence, db
from sys import argv


def main():
    language = Language.query.filter_by(name=argv[1]).first()
    words = Word.query.filter_by(language=language).all()

    for w in words:
        sentences = w.sentences
        for s in sentences:
            trans = TranslatedSentence.query.filter_by(sentence=s).all()
            for tr in trans:
                db.session.delete(tr)
                db.session.commit()
            db.session.delete(s)
            db.session.commit()

    for w in words:
        for tr in w.translations:
            db.session.delete(tr)
            db.session.commit()
        db.session.delete(w)
        db.session.commit()

    # delete primary words
    Word.query.filter_by(language=language).delete()

    db.session.commit()


if __name__ == '__main__':
    main()
