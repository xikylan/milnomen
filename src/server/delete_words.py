from app import Language, Word, db
from sys import argv


def main():
    language = Language.query.filter_by(name=argv[1]).first()
    words = Word.query.filter_by(language=language).all()

    # delete dependent elements
    for word in words:
        trans = word.translations
        for t in trans:
            db.session.delete(t)

    # delete primary words
    Word.query.filter_by(language=language).delete()

    db.session.commit()


main()
